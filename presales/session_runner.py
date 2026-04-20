"""
Generic session runner for Anthropic Claude Managed Agents.

Handles the full lifecycle of a single agent session:
  - Session creation
  - Stream-first event subscription (open stream before sending message)
  - Event processing with correct idle/terminated break gate
  - Output capture
  - Session cleanup
"""

from __future__ import annotations

import anthropic


def run_agent_session(
    client: anthropic.Anthropic,
    agent_id: str,
    agent_version: int | str,
    environment_id: str,
    message: str,
    session_title: str | None = None,
    verbose: bool = True,
) -> str:
    """
    Run a single managed-agent session end-to-end and return captured text output.

    Args:
        client:           Authenticated Anthropic client.
        agent_id:         ID of the pre-created agent (e.g. "agent_abc123").
        agent_version:    Version of the agent to pin (from agents.json).
        environment_id:   ID of the pre-created environment.
        message:          The user message / task to send to the agent.
        session_title:    Optional human-readable session title.
        verbose:          Stream agent output to stdout in real time.

    Returns:
        Full text output from the agent as a single string.
    """
    session = client.beta.sessions.create(
        agent={"type": "agent", "id": agent_id, "version": agent_version},
        environment_id=environment_id,
        title=session_title,
    )

    output_parts: list[str] = []

    # Stream-first pattern: open the stream BEFORE sending the message so no
    # early events are missed (see managed-agents-client-patterns.md §7).
    with client.beta.sessions.stream(session_id=session.id) as stream:
        client.beta.sessions.events.send(
            session_id=session.id,
            events=[
                {
                    "type": "user.message",
                    "content": [{"type": "text", "text": message}],
                }
            ],
        )

        for event in stream:
            # ── Agent output ──────────────────────────────────────────────
            if event.type == "agent.message":
                for block in event.content:
                    if block.type == "text":
                        if verbose:
                            print(block.text, end="", flush=True)
                        output_parts.append(block.text)

            # ── Extended thinking (log summary only) ──────────────────────
            elif event.type == "agent.thinking":
                if verbose:
                    for block in event.content:
                        thinking_text = getattr(block, "thinking", "")
                        if thinking_text:
                            preview = thinking_text[:120].replace("\n", " ")
                            print(f"\n[Thinking: {preview}…]\n", flush=True)

            # ── Tool activity (informational) ─────────────────────────────
            elif event.type == "agent.tool_use":
                if verbose:
                    tool_name = getattr(event, "name", "unknown")
                    print(f"\n[Tool: {tool_name}]\n", flush=True)

            # ── Token usage telemetry ─────────────────────────────────────
            elif event.type == "span.model_request_end":
                if verbose and hasattr(event, "model_usage"):
                    u = event.model_usage
                    cached = getattr(u, "cache_read_input_tokens", 0)
                    total_in = getattr(u, "input_tokens", 0)
                    out = getattr(u, "output_tokens", 0)
                    print(
                        f"\n[Usage — in: {total_in}, cached: {cached}, out: {out}]\n",
                        flush=True,
                    )

            # ── Session errors ────────────────────────────────────────────
            elif event.type == "session.error":
                print(f"\n[Session error: {event}]\n", flush=True)

            # ── Terminal conditions ───────────────────────────────────────
            elif event.type == "session.status_terminated":
                break

            elif event.type == "session.status_idle":
                # Only break on terminal stop reasons (end_turn, retries_exhausted).
                # requires_action means the agent is waiting for a custom tool result
                # or tool confirmation — we don't use custom tools here, so treat it
                # as terminal to avoid blocking forever.
                stop_reason = getattr(event, "stop_reason", None)
                stop_type = getattr(stop_reason, "type", None) if stop_reason else None
                if stop_type == "requires_action":
                    # No custom tool handler registered — log and exit gracefully.
                    print(
                        "\n[Session requires_action but no handler registered — exiting]\n",
                        flush=True,
                    )
                break

    return "\n".join(output_parts)
