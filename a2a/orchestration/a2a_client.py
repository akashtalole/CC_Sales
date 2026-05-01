"""
A2A Protocol client for the CC Sales Presales Agent.

Implements the Google A2A protocol to enable agent-to-agent communication
with other specialized agents in the organization.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class A2AError(Exception):
    """Base exception for A2A protocol errors."""


class AgentNotFoundError(A2AError):
    """Raised when a requested agent is not in the registry."""


class TaskFailedError(A2AError):
    """Raised when an agent task returns a failed status."""


class TaskTimeoutError(A2AError):
    """Raised when an agent task exceeds the timeout."""


class TaskInputRequiredError(A2AError):
    """Raised when an agent task requires human input to proceed."""


class A2AClient:
    """
    A2A protocol client. Handles agent discovery, task creation,
    and result polling for the presales orchestration layer.
    """

    def __init__(
        self,
        discovery_url: str,
        auth_token: str,
        timeout: int = 120,
        poll_interval: float = 2.0,
        max_polls: int = 60,
    ):
        self.discovery_url = discovery_url.rstrip("/")
        self.auth_token = auth_token
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.max_polls = max_polls
        self._agent_registry: dict[str, dict] = {}

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }

    async def discover_agents(self, force_refresh: bool = False) -> dict[str, dict]:
        """
        Query the discovery endpoint and cache agent cards.
        Returns a dict keyed by agent_id.
        """
        if self._agent_registry and not force_refresh:
            return self._agent_registry

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{self.discovery_url}/.well-known/agent-cards",
                headers=self._headers(),
            )
            response.raise_for_status()
            cards: list[dict] = response.json()

        self._agent_registry = {card["agent"]["id"]: card for card in cards}
        logger.info("Discovered %d agents: %s", len(self._agent_registry), list(self._agent_registry.keys()))
        return self._agent_registry

    async def get_agent_card(self, agent_id: str) -> dict:
        """Return the agent card for a given agent_id, refreshing registry if needed."""
        if agent_id not in self._agent_registry:
            await self.discover_agents(force_refresh=True)
        if agent_id not in self._agent_registry:
            raise AgentNotFoundError(f"Agent '{agent_id}' not found in registry")
        return self._agent_registry[agent_id]

    async def delegate_task(
        self,
        agent_id: str,
        skill_id: str,
        input_data: dict[str, Any],
        timeout: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Delegate a task to a specific agent skill.

        Args:
            agent_id: Target agent identifier (e.g. 'legal-agent')
            skill_id: Skill to invoke on target agent (e.g. 'contract-review')
            input_data: Skill input conforming to agent card input_schema
            timeout: Override default timeout for long-running tasks
            metadata: Optional metadata to include with task

        Returns:
            Agent skill output dict

        Raises:
            AgentNotFoundError, TaskFailedError, TaskTimeoutError, TaskInputRequiredError
        """
        card = await self.get_agent_card(agent_id)
        agent_url = card["agent"]["url"]
        effective_timeout = timeout or self.timeout

        payload = {
            "skill_id": skill_id,
            "input": input_data,
            "metadata": {
                "requested_by": "presales-agent",
                "timestamp": _now_iso(),
                **(metadata or {}),
            },
        }

        logger.info("Delegating '%s:%s' to %s", agent_id, skill_id, agent_url)

        async with httpx.AsyncClient(timeout=effective_timeout) as client:
            response = await client.post(
                f"{agent_url}/tasks",
                json=payload,
                headers=self._headers(),
            )
            response.raise_for_status()
            task = response.json()
            task_id = task["task_id"]

        return await self._poll_task(agent_url, task_id)

    async def _poll_task(self, agent_url: str, task_id: str) -> dict[str, Any]:
        """Poll task status until completed, failed, or input-required."""
        async with httpx.AsyncClient(timeout=30) as client:
            for attempt in range(self.max_polls):
                response = await client.get(
                    f"{agent_url}/tasks/{task_id}",
                    headers=self._headers(),
                )
                response.raise_for_status()
                task = response.json()
                status = task["status"]

                if status == "completed":
                    logger.info("Task %s completed", task_id)
                    return task["output"]

                if status == "failed":
                    error = task.get("error", "Unknown error")
                    logger.error("Task %s failed: %s", task_id, error)
                    raise TaskFailedError(f"Agent task {task_id} failed: {error}")

                if status == "input-required":
                    message = task.get("message", "Agent requires input")
                    logger.warning("Task %s requires human input: %s", task_id, message)
                    raise TaskInputRequiredError(message)

                logger.debug("Task %s status: %s (attempt %d)", task_id, status, attempt + 1)
                await asyncio.sleep(self.poll_interval)

        raise TaskTimeoutError(f"Task {task_id} did not complete after {self.max_polls} polls")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
