"""
UVal-inspired Scorer for Medicare Inbound Leads.

Adapted from the user's llm-router-engine UVal composite scoring system.
Dimensions tuned for this business plan:
- Capability (fit for in-house enrollment vs sell)
- Compliance Risk (how clean the call was)
- Predicted LTV / Enrollment Probability
- Cost to Serve / Margin Potential (for sell stream)
- Regulatory Risk Penalty

Outputs a structured score to drive the dual-stream decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel


class LeadScore(BaseModel):
    overall_uval: float  # 0-1 composite
    enroll_fit: float    # Probability this should go to in-house enrollment stream
    sell_margin_potential: float  # Expected margin if sold at $25
    compliance_risk: float        # 0 = clean, 1 = high risk
    recommended_stream: Literal["enroll_in_house", "sell_call", "block"]
    rationale: str


@dataclass
class UValWeights:
    capability: float = 0.30
    compliance_risk: float = 0.25
    ltv_prediction: float = 0.25
    cost_efficiency: float = 0.15
    regulatory_penalty: float = 0.05


class MedicareLeadScorer:
    """
    Production scorer for Medicare inbound calls.
    In real deployment this would call the llm-router-engine for sophisticated UVal + LLM judge.
    """

    def __init__(self, weights: UValWeights | None = None):
        self.weights = weights or UValWeights()

    def score(self, context: dict) -> LeadScore:
        """
        context expected keys (from compliance result + call metadata):
        - compliance_score (0-100)
        - has_high_intent_signals (bool)
        - state_licensing_fit (0-1)
        - predicted_enrollment_prob (0-1, from historicals or model)
        - estimated_cost_to_serve (for sell stream)
        - regulatory_flags_count
        """
        compliance = min(1.0, context.get("compliance_score", 70) / 100)
        capability = (
            0.4 * context.get("state_licensing_fit", 0.7) +
            0.3 * context.get("has_high_intent_signals", False) +
            0.3 * context.get("predicted_enrollment_prob", 0.5)
        )
        ltv = context.get("predicted_enrollment_prob", 0.55)
        cost = max(0.0, 1.0 - (context.get("estimated_cost_to_serve", 18) / 30))  # lower cost = higher score
        reg_penalty = max(0.0, 1.0 - (context.get("regulatory_flags_count", 0) * 0.2))

        # Composite UVal (higher = better overall)
        uval = (
            self.weights.capability * capability +
            self.weights.compliance_risk * compliance +
            self.weights.ltv_prediction * ltv +
            self.weights.cost_efficiency * cost +
            self.weights.regulatory_penalty * reg_penalty
        )

        # Simple decision policy for dual stream (can be replaced by router later)
        enroll_fit = 0.6 * capability + 0.4 * ltv
        sell_potential = 0.7 * cost + 0.3 * (1 - compliance)  # sell lower-intent / lower compliance risk calls

        if uval < 0.45 or compliance < 0.75:
            stream = "block"
            rationale = "Fails minimum compliance or value threshold."
        elif enroll_fit > 0.72 and ltv > 0.65:
            stream = "enroll_in_house"
            rationale = f"Strong fit for in-house (enroll_fit={enroll_fit:.2f}, LTV={ltv:.2f})."
        else:
            stream = "sell_call"
            rationale = f"Better economics in sell stream (sell_potential={sell_potential:.2f})."

        return LeadScore(
            overall_uval=round(uval, 3),
            enroll_fit=round(enroll_fit, 3),
            sell_margin_potential=round(sell_potential, 3),
            compliance_risk=round(1 - compliance, 3),
            recommended_stream=stream,
            rationale=rationale,
        )
