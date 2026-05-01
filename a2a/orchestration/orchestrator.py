"""
Presales multi-agent orchestrator.

Coordinates parallel delegation to specialized org agents for complex
presales workflows: proposal generation, contract review, competitive
response, and ROI calculation.
"""

import asyncio
import logging
from typing import Any

from .a2a_client import A2AClient, A2AError

logger = logging.getLogger(__name__)


class PresalesOrchestrator:
    """
    High-level orchestration layer for the presales agent.
    Each method represents a complete multi-agent workflow.
    """

    def __init__(self, client: A2AClient):
        self.client = client

    async def generate_full_proposal(
        self,
        crm_deal_id: str,
        scope_summary: str,
        customer_profile: dict[str, Any],
        investment_estimate: float,
    ) -> dict[str, Any]:
        """
        Orchestrates full proposal generation across 4 specialist agents in parallel:
        - technical-architecture-agent: solution design + effort estimate
        - pricing-agent: 3-tier pricing quote
        - customer-success-agent: reference customer matching
        - finance-agent: ROI / business case model

        Partial failures are tolerated — synthesizes what's available.
        """
        logger.info("Starting full proposal orchestration for deal %s", crm_deal_id)

        results = await asyncio.gather(
            self._safe_delegate(
                "technical-architecture-agent",
                "architecture-design",
                {
                    "requirements_summary": scope_summary,
                    "current_stack": customer_profile.get("current_stack", ""),
                    "target_platform": customer_profile.get("target_platform", "aws"),
                    "compliance_requirements": customer_profile.get("compliance", []),
                },
            ),
            self._safe_delegate(
                "pricing-agent",
                "pricing-quote",
                {
                    "service_type": customer_profile.get("service_type", "managed-cloud-services"),
                    "scope_summary": scope_summary,
                    "deal_size_estimate": investment_estimate,
                    "customer_segment": customer_profile.get("segment", "enterprise"),
                    "crm_deal_id": crm_deal_id,
                },
            ),
            self._safe_delegate(
                "customer-success-agent",
                "reference-match",
                {
                    "prospect_profile": customer_profile,
                    "reference_type": "case-study",
                    "max_results": 3,
                },
            ),
            self._safe_delegate(
                "finance-agent",
                "business-case",
                {
                    "crm_deal_id": crm_deal_id,
                    "investment_amount": investment_estimate,
                    "customer_metrics": customer_profile.get("metrics", {}),
                    "audience": "cfo",
                },
            ),
        )

        architecture, pricing, references, finance = results

        errors = [r["error"] for r in results if r.get("error")]
        if errors:
            logger.warning("Proposal generation had %d partial failures: %s", len(errors), errors)

        return {
            "crm_deal_id": crm_deal_id,
            "architecture": architecture.get("output"),
            "pricing": pricing.get("output"),
            "references": references.get("output"),
            "finance": finance.get("output"),
            "errors": errors,
            "complete": len(errors) == 0,
        }

    async def review_contract(
        self,
        document_url: str,
        contract_type: str,
        deal_value: float,
        jurisdiction: str,
        crm_deal_id: str,
    ) -> dict[str, Any]:
        """Delegates contract review to the legal agent."""
        logger.info("Delegating contract review to legal-agent for deal %s", crm_deal_id)
        return await self.client.delegate_task(
            agent_id="legal-agent",
            skill_id="contract-review",
            input_data={
                "document_url": document_url,
                "contract_type": contract_type,
                "deal_value": deal_value,
                "customer_jurisdiction": jurisdiction,
                "urgency": "urgent" if deal_value > 500_000 else "standard",
            },
            metadata={"crm_deal_id": crm_deal_id},
        )

    async def build_competitive_response(
        self,
        competitor_name: str,
        crm_deal_id: str,
        deal_context: str,
        prospect_profile: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Builds a competitive response package in parallel:
        - competitive-intelligence skill (presales agent, self-call)
        - customer-success-agent: displacement case studies
        """
        logger.info("Building competitive response vs '%s' for deal %s", competitor_name, crm_deal_id)

        intel_result, references_result = await asyncio.gather(
            self._safe_delegate(
                "presales-agent",
                "competitive-intelligence",
                {
                    "competitor_names": [competitor_name],
                    "deal_context": deal_context,
                    "output_type": "battle-card",
                },
            ),
            self._safe_delegate(
                "customer-success-agent",
                "reference-match",
                {
                    "prospect_profile": {
                        **(prospect_profile or {}),
                        "competitive_displacement": competitor_name,
                    },
                    "reference_type": "case-study",
                    "max_results": 2,
                },
            ),
        )

        return {
            "competitor": competitor_name,
            "crm_deal_id": crm_deal_id,
            "competitive_intel": intel_result.get("output"),
            "displacement_references": references_result.get("output"),
            "errors": [r["error"] for r in [intel_result, references_result] if r.get("error")],
        }

    async def build_roi_package(
        self,
        crm_deal_id: str,
        investment_amount: float,
        customer_metrics: dict[str, Any],
        audience: str = "cfo",
    ) -> dict[str, Any]:
        """
        Generates ROI + TCO package via parallel calls to finance-agent.
        Useful when a prospect's economic buyer asks for financial justification.
        """
        logger.info("Building ROI package for deal %s (audience: %s)", crm_deal_id, audience)

        business_case, tco = await asyncio.gather(
            self._safe_delegate(
                "finance-agent",
                "business-case",
                {
                    "crm_deal_id": crm_deal_id,
                    "investment_amount": investment_amount,
                    "customer_metrics": customer_metrics,
                    "audience": audience,
                },
            ),
            self._safe_delegate(
                "finance-agent",
                "tco-analysis",
                {
                    "current_state_costs": customer_metrics.get("current_costs", {}),
                    "proposed_solution_cost": investment_amount,
                    "implementation_cost": investment_amount * 0.15,
                    "analysis_years": 3,
                },
            ),
        )

        return {
            "crm_deal_id": crm_deal_id,
            "business_case": business_case.get("output"),
            "tco_analysis": tco.get("output"),
            "errors": [r["error"] for r in [business_case, tco] if r.get("error")],
        }

    async def prepare_technical_brief(
        self,
        crm_deal_id: str,
        scope_summary: str,
        customer_stack: str,
        target_platform: str = "aws",
    ) -> dict[str, Any]:
        """
        Generates a technical pre-call brief with architecture options and risk assessment.
        Runs architecture-design and technical-risk-assessment in parallel.
        """
        logger.info("Preparing technical brief for deal %s", crm_deal_id)

        architecture, risks = await asyncio.gather(
            self._safe_delegate(
                "technical-architecture-agent",
                "architecture-design",
                {
                    "requirements_summary": scope_summary,
                    "current_stack": customer_stack,
                    "target_platform": target_platform,
                },
            ),
            self._safe_delegate(
                "technical-architecture-agent",
                "technical-risk-assessment",
                {
                    "scope_summary": scope_summary,
                    "customer_environment": customer_stack,
                },
            ),
        )

        return {
            "crm_deal_id": crm_deal_id,
            "architecture_options": architecture.get("output"),
            "risk_assessment": risks.get("output"),
            "errors": [r["error"] for r in [architecture, risks] if r.get("error")],
        }

    async def _safe_delegate(
        self,
        agent_id: str,
        skill_id: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Wraps delegate_task with error handling.
        Returns {"output": ...} on success or {"error": "..."} on failure.
        Allows parallel orchestration to continue despite partial failures.
        """
        try:
            output = await self.client.delegate_task(agent_id, skill_id, input_data)
            return {"output": output}
        except A2AError as e:
            logger.error("Delegation to %s:%s failed: %s", agent_id, skill_id, e)
            return {"error": f"{agent_id}:{skill_id} — {e}"}
        except Exception as e:
            logger.exception("Unexpected error delegating to %s:%s", agent_id, skill_id)
            return {"error": f"{agent_id}:{skill_id} — Unexpected: {e}"}
