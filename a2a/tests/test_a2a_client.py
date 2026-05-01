"""
Unit tests for the A2A protocol client.
"""

import json
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch

from orchestration.a2a_client import (
    A2AClient,
    AgentNotFoundError,
    TaskFailedError,
    TaskTimeoutError,
    TaskInputRequiredError,
)


MOCK_AGENT_CARDS = [
    {
        "agent": {"id": "legal-agent", "url": "https://agents.test.com/legal"},
        "skills": [{"id": "contract-review"}],
    },
    {
        "agent": {"id": "pricing-agent", "url": "https://agents.test.com/pricing"},
        "skills": [{"id": "pricing-quote"}],
    },
]

MOCK_TASK_CREATED = {"task_id": "task_abc123", "status": "working"}
MOCK_TASK_COMPLETED = {
    "task_id": "task_abc123",
    "status": "completed",
    "output": {"risk_level": "medium", "flagged_clauses": []},
}
MOCK_TASK_FAILED = {
    "task_id": "task_abc123",
    "status": "failed",
    "error": "Document could not be parsed",
}
MOCK_TASK_INPUT_REQUIRED = {
    "task_id": "task_abc123",
    "status": "input-required",
    "message": "Please specify the governing law jurisdiction",
}


@pytest.fixture
def client():
    return A2AClient(
        discovery_url="https://agents.test.com",
        auth_token="test-token",
        poll_interval=0.01,
        max_polls=5,
    )


@pytest.mark.asyncio
async def test_discover_agents_populates_registry(client):
    with patch("httpx.AsyncClient") as mock_cls:
        mock_response = MagicMock()
        mock_response.json.return_value = MOCK_AGENT_CARDS
        mock_response.raise_for_status = MagicMock()

        mock_http = AsyncMock()
        mock_http.__aenter__ = AsyncMock(return_value=mock_http)
        mock_http.__aexit__ = AsyncMock(return_value=None)
        mock_http.get = AsyncMock(return_value=mock_response)
        mock_cls.return_value = mock_http

        registry = await client.discover_agents()

    assert "legal-agent" in registry
    assert "pricing-agent" in registry


@pytest.mark.asyncio
async def test_get_agent_card_unknown_raises(client):
    client._agent_registry = {"legal-agent": MOCK_AGENT_CARDS[0]}

    with patch.object(client, "discover_agents", return_value=client._agent_registry):
        with pytest.raises(AgentNotFoundError, match="pricing-agent"):
            await client.get_agent_card("pricing-agent")


@pytest.mark.asyncio
async def test_delegate_task_success(client):
    client._agent_registry = {
        "legal-agent": MOCK_AGENT_CARDS[0]
    }

    with patch("httpx.AsyncClient") as mock_cls:
        mock_http = AsyncMock()
        mock_http.__aenter__ = AsyncMock(return_value=mock_http)
        mock_http.__aexit__ = AsyncMock(return_value=None)

        post_response = MagicMock()
        post_response.json.return_value = MOCK_TASK_CREATED
        post_response.raise_for_status = MagicMock()

        get_response = MagicMock()
        get_response.json.return_value = MOCK_TASK_COMPLETED
        get_response.raise_for_status = MagicMock()

        mock_http.post = AsyncMock(return_value=post_response)
        mock_http.get = AsyncMock(return_value=get_response)
        mock_cls.return_value = mock_http

        result = await client.delegate_task(
            agent_id="legal-agent",
            skill_id="contract-review",
            input_data={"document_url": "https://example.com/doc.pdf", "contract_type": "msa"},
        )

    assert result["risk_level"] == "medium"


@pytest.mark.asyncio
async def test_poll_task_raises_on_failed(client):
    client._agent_registry = {"legal-agent": MOCK_AGENT_CARDS[0]}

    with patch("httpx.AsyncClient") as mock_cls:
        mock_http = AsyncMock()
        mock_http.__aenter__ = AsyncMock(return_value=mock_http)
        mock_http.__aexit__ = AsyncMock(return_value=None)

        post_response = MagicMock()
        post_response.json.return_value = MOCK_TASK_CREATED
        post_response.raise_for_status = MagicMock()

        get_response = MagicMock()
        get_response.json.return_value = MOCK_TASK_FAILED
        get_response.raise_for_status = MagicMock()

        mock_http.post = AsyncMock(return_value=post_response)
        mock_http.get = AsyncMock(return_value=get_response)
        mock_cls.return_value = mock_http

        with pytest.raises(TaskFailedError, match="Document could not be parsed"):
            await client.delegate_task(
                agent_id="legal-agent",
                skill_id="contract-review",
                input_data={"document_url": "bad-url", "contract_type": "msa"},
            )


@pytest.mark.asyncio
async def test_poll_task_raises_on_input_required(client):
    client._agent_registry = {"legal-agent": MOCK_AGENT_CARDS[0]}

    with patch("httpx.AsyncClient") as mock_cls:
        mock_http = AsyncMock()
        mock_http.__aenter__ = AsyncMock(return_value=mock_http)
        mock_http.__aexit__ = AsyncMock(return_value=None)

        post_response = MagicMock()
        post_response.json.return_value = MOCK_TASK_CREATED
        post_response.raise_for_status = MagicMock()

        get_response = MagicMock()
        get_response.json.return_value = MOCK_TASK_INPUT_REQUIRED
        get_response.raise_for_status = MagicMock()

        mock_http.post = AsyncMock(return_value=post_response)
        mock_http.get = AsyncMock(return_value=get_response)
        mock_cls.return_value = mock_http

        with pytest.raises(TaskInputRequiredError, match="jurisdiction"):
            await client.delegate_task(
                agent_id="legal-agent",
                skill_id="contract-review",
                input_data={"document_url": "https://example.com/doc.pdf", "contract_type": "msa"},
            )


@pytest.mark.asyncio
async def test_poll_task_raises_on_timeout(client):
    """Client should raise TaskTimeoutError when max_polls is exceeded."""
    client._agent_registry = {"legal-agent": MOCK_AGENT_CARDS[0]}
    client.max_polls = 2

    with patch("httpx.AsyncClient") as mock_cls:
        mock_http = AsyncMock()
        mock_http.__aenter__ = AsyncMock(return_value=mock_http)
        mock_http.__aexit__ = AsyncMock(return_value=None)

        post_response = MagicMock()
        post_response.json.return_value = MOCK_TASK_CREATED
        post_response.raise_for_status = MagicMock()

        # Always return "working" — never completes
        get_response = MagicMock()
        get_response.json.return_value = {"task_id": "task_abc123", "status": "working"}
        get_response.raise_for_status = MagicMock()

        mock_http.post = AsyncMock(return_value=post_response)
        mock_http.get = AsyncMock(return_value=get_response)
        mock_cls.return_value = mock_http

        with pytest.raises(TaskTimeoutError):
            await client.delegate_task(
                agent_id="legal-agent",
                skill_id="contract-review",
                input_data={"document_url": "https://example.com/doc.pdf", "contract_type": "msa"},
            )
