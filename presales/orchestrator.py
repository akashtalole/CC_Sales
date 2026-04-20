"""
Pre-sales workflow orchestrator.

Runs three Claude Managed Agent sessions in sequence:
  1. Research Agent  — deep customer intelligence
  2. Planning Agent  — account plan & sales strategy
  3. NBA Agent       — next best actions & outreach playbook

Each session feeds its output as context into the next, building a
comprehensive pre-sales package from a single company name and optional hints.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import TypedDict

import anthropic

from .session_runner import run_agent_session

CONFIG_PATH = Path(__file__).parent.parent / "config" / "agents.json"


class PreSalesResult(TypedDict):
    company: str
    research: str
    account_plan: str
    next_best_actions: str


def _load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Agent config not found at {CONFIG_PATH}.\n"
            "Run  python setup_agents.py  first to create the agents."
        )
    with open(CONFIG_PATH) as f:
        return json.load(f)


def _section(title: str) -> None:
    bar = "─" * 60
    print(f"\n{bar}\n{title}\n{bar}\n", flush=True)


def _header(title: str) -> None:
    bar = "=" * 60
    print(f"\n{bar}\n{title}\n{bar}\n", flush=True)


def run_presales_workflow(
    company_name: str,
    company_website: str | None = None,
    contact_info: str | None = None,
    industry: str | None = None,
    use_case: str | None = None,
    additional_context: str | None = None,
    verbose: bool = True,
) -> PreSalesResult:
    """
    Execute the full pre-sales workflow for a prospect company.

    The three-phase pipeline runs sequentially; each phase receives the
    accumulated context from all previous phases so the output builds
    organically toward a complete pre-sales package.

    Args:
        company_name:        Prospect company name (required).
        company_website:     Company website or LinkedIn URL.
        contact_info:        Known contacts, e.g. "Jane Smith, CTO".
        industry:            Industry / vertical, e.g. "FinTech", "Healthcare".
        use_case:            Why we think they need our solution (optional).
        additional_context:  Any other intel — deal source, partner intro, etc.
        verbose:             Stream agent output to stdout in real time.

    Returns:
        PreSalesResult dict with keys: company, research, account_plan,
        next_best_actions.
    """
    client = anthropic.Anthropic()
    config = _load_config()

    environment_id: str = config["environment_id"]
    agents: dict = config["agents"]

    # ── Build prospect context block ──────────────────────────────────────
    lines = [f"**Company**: {company_name}"]
    if company_website:
        lines.append(f"**Website**: {company_website}")
    if industry:
        lines.append(f"**Industry**: {industry}")
    if contact_info:
        lines.append(f"**Known Contacts**: {contact_info}")
    if use_case:
        lines.append(f"**Suspected Use Case**: {use_case}")
    if additional_context:
        lines.append(f"**Additional Context**: {additional_context}")
    prospect_context = "\n".join(lines)

    _header(f"PRE-SALES WORKFLOW  ·  {company_name.upper()}")

    # ══════════════════════════════════════════════════════════════════════
    # PHASE 1 — CUSTOMER RESEARCH
    # ══════════════════════════════════════════════════════════════════════
    _section("PHASE 1 · CUSTOMER RESEARCH")

    research_message = textwrap.dedent(f"""\
        Please conduct comprehensive pre-sales research on the following prospect company.

        PROSPECT DETAILS:
        {prospect_context}

        Produce a full intelligence report following your structured template.
        Use web_search and web_fetch to gather current, accurate information.
        Be thorough — the sales team is relying on this to personalise every touchpoint.
    """)

    research_output = run_agent_session(
        client=client,
        agent_id=agents["research"]["id"],
        agent_version=agents["research"]["version"],
        environment_id=environment_id,
        message=research_message,
        session_title=f"Research · {company_name}",
        verbose=verbose,
    )

    # ══════════════════════════════════════════════════════════════════════
    # PHASE 2 — ACCOUNT PLANNING
    # ══════════════════════════════════════════════════════════════════════
    _section("PHASE 2 · ACCOUNT PLANNING")

    planning_message = textwrap.dedent(f"""\
        Based on the research below, create a comprehensive account plan for {company_name}.

        PROSPECT DETAILS:
        {prospect_context}

        RESEARCH INTELLIGENCE:
        {research_output}

        Build an actionable account plan the sales team can execute immediately.
        Where the research reveals specific names, technologies, or challenges,
        incorporate them directly into the plan — do not use generic placeholders.
    """)

    plan_output = run_agent_session(
        client=client,
        agent_id=agents["planning"]["id"],
        agent_version=agents["planning"]["version"],
        environment_id=environment_id,
        message=planning_message,
        session_title=f"Account Plan · {company_name}",
        verbose=verbose,
    )

    # ══════════════════════════════════════════════════════════════════════
    # PHASE 3 — NEXT BEST ACTIONS
    # ══════════════════════════════════════════════════════════════════════
    _section("PHASE 3 · NEXT BEST ACTIONS")

    nba_message = textwrap.dedent(f"""\
        You have the research and account plan for {company_name} below.
        Produce a prioritised, immediately executable next-best-action playbook
        for the pre-sales team.

        PROSPECT DETAILS:
        {prospect_context}

        RESEARCH INTELLIGENCE:
        {research_output}

        ACCOUNT PLAN:
        {plan_output}

        Every outreach message and action must reference real facts from the research.
        Do not use placeholder text — write copy the team can send today.
    """)

    nba_output = run_agent_session(
        client=client,
        agent_id=agents["nba"]["id"],
        agent_version=agents["nba"]["version"],
        environment_id=environment_id,
        message=nba_message,
        session_title=f"Next Best Actions · {company_name}",
        verbose=verbose,
    )

    _header("WORKFLOW COMPLETE")

    return PreSalesResult(
        company=company_name,
        research=research_output,
        account_plan=plan_output,
        next_best_actions=nba_output,
    )
