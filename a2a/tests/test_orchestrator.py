"""
Unit tests for the presales multi-agent orchestrator.
"""

import pytest
from unittest.mock import AsyncMock, patch

from orchestration.orchestrator import PresalesOrchestrator
from orchestration.a2a_client import A2AClient, TaskFailedError


@pytest.fixture
def mock_client():
    client = AsyncMock(spec=A2AClient)
    return client


@pytest.fixture
def orchestrator(mock_client):
    return PresalesOrchestrator(client=mock_client)


@pytest.mark.asyncio
async def test_generate_full_proposal_all_succeed(orchestrator, mock_client):
    mock_client.delegate_task.side_effect = [
        {"architecture_summary": "EKS migration plan", "architecture_doc_url": "https://notion.test/arch"},
        {"options": [{"tier": "standard", "list_price": 950000}], "recommended_tier": "standard"},
        {"matches": [{"customer_id": "cust_1", "similarity_score": 0.92}]},
        {"roi_pct": 180, "payback_months": 8, "business_case_url": "https://notion.test/roi"},
    ]

    result = await orchestrator.generate_full_proposal(
        crm_deal_id="deal_12345",
        scope_summary="Migrate 40 microservices to AWS EKS",
        customer_profile={"segment": "enterprise", "current_stack": "VMware on-prem"},
        investment_estimate=950_000,
    )

    assert result["complete"] is True
    assert result["architecture"]["architecture_summary"] == "EKS migration plan"
    assert result["pricing"]["recommended_tier"] == "standard"
    assert result["finance"]["roi_pct"] == 180
    assert len(result["errors"]) == 0


@pytest.mark.asyncio
async def test_generate_full_proposal_partial_failure(orchestrator, mock_client):
    """Orchestrator should tolerate partial failures and return what succeeded."""
    mock_client.delegate_task.side_effect = [
        {"architecture_summary": "EKS plan"},               # architecture succeeds
        TaskFailedError("Pricing service unavailable"),       # pricing fails
        {"matches": []},                                      # references succeeds (empty)
        {"roi_pct": 150, "payback_months": 10},              # finance succeeds
    ]

    result = await orchestrator.generate_full_proposal(
        crm_deal_id="deal_12345",
        scope_summary="Cloud migration",
        customer_profile={},
        investment_estimate=500_000,
    )

    assert result["complete"] is False
    assert result["architecture"] is not None
    assert result["pricing"] is None
    assert len(result["errors"]) == 1
    assert "pricing-agent" in result["errors"][0]


@pytest.mark.asyncio
async def test_review_contract_delegates_correctly(orchestrator, mock_client):
    expected_output = {"risk_level": "high", "flagged_clauses": [{"clause": "IP ownership"}]}
    mock_client.delegate_task.return_value = expected_output

    result = await orchestrator.review_contract(
        document_url="https://example.com/msa.pdf",
        contract_type="msa",
        deal_value=1_200_000,
        jurisdiction="California, USA",
        crm_deal_id="deal_99",
    )

    assert result["risk_level"] == "high"
    mock_client.delegate_task.assert_called_once_with(
        agent_id="legal-agent",
        skill_id="contract-review",
        input_data={
            "document_url": "https://example.com/msa.pdf",
            "contract_type": "msa",
            "deal_value": 1_200_000,
            "customer_jurisdiction": "California, USA",
            "urgency": "urgent",
        },
        metadata={"crm_deal_id": "deal_99"},
    )


@pytest.mark.asyncio
async def test_build_competitive_response(orchestrator, mock_client):
    mock_client.delegate_task.side_effect = [
        {"battle_card_url": "https://notion.test/battle-card", "differentiation_points": ["Zero-downtime migration"]},
        {"matches": [{"customer_id": "cust_displaced_1"}]},
    ]

    result = await orchestrator.build_competitive_response(
        competitor_name="CompetitorX",
        crm_deal_id="deal_12345",
        deal_context="Cloud migration deal, EKS target",
    )

    assert result["competitor"] == "CompetitorX"
    assert result["competitive_intel"]["battle_card_url"] is not None
    assert len(result["errors"]) == 0


@pytest.mark.asyncio
async def test_build_roi_package(orchestrator, mock_client):
    mock_client.delegate_task.side_effect = [
        {"roi_pct": 200, "payback_months": 7, "business_case_url": "https://notion.test/roi"},
        {"savings": 480_000, "breakeven_months": 9, "tco_comparison_url": "https://notion.test/tco"},
    ]

    result = await orchestrator.build_roi_package(
        crm_deal_id="deal_12345",
        investment_amount=800_000,
        customer_metrics={"current_annual_cost": 1_200_000, "engineer_hours_per_week": 80},
    )

    assert result["business_case"]["roi_pct"] == 200
    assert result["tco_analysis"]["savings"] == 480_000
    assert len(result["errors"]) == 0
