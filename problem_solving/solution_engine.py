"""
OPERATING SYSTEM BRAIN: Problem → Solution Engine
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This brain takes any problem from the master problem list and generates
a complete, genius-level solution: selecting the optimal plugins for the
specific issue, ordering them in the ideal signal chain, and delivering
mouse-level, parameter-exact instructions to fix it entirely.

Default AI thinking says "use a compressor to control dynamics." That is
garbage. This brain says: "For the kick's uncontrolled transient smear,
insert FabFilter Pro-C 2 before the bus. Set it to Punch mode. Attack:
0.5 ms. Release: 85 ms auto. Ratio: 4:1. Threshold at -8 dB. Enable
the lookahead at 1.2 ms. Then follow with iZotope Neutron's Transient
Shaper: Attack at -6 dB, Sustain at +1 dB. This two-stage chain kills
the smear while adding snap and presence."

Protocol:
  1. Receive a single AggregatedProblem or Problem.
  2. Classify the problem by type and severity.
  3. Select the optimal plugin(s) from the available registry — not the
     first option, the best option for this exact problem type.
  4. Design a solution chain: ordered plugins with specific roles.
  5. For each plugin in the chain, generate exact parameter operations.
  6. Return a structured SolutionPlan with full chain and instructions.
"""

# TODO: Design this brain with Cursor — define the problem classification
# taxonomy, the plugin selection scoring system, and the solution chain
# design algorithm before writing any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from core.source_preparation import ParameterOperation


@dataclass
class SolutionStep:
    """
    A single step in a problem solution chain.

    Attributes:
        step_number: Position in the solution chain (1-indexed).
        plugin_name: Plugin to use at this step.
        role: The specific role this plugin plays in solving the problem.
        operations: Exact parameter operations.
        expected_result: What this step should accomplish.
    """

    step_number: int
    plugin_name: str
    role: str
    operations: List[ParameterOperation] = field(default_factory=list)
    expected_result: str = ""


@dataclass
class SolutionPlan:
    """
    The complete solution plan for a single problem.

    Attributes:
        problem_id: ID of the problem being solved.
        instrument_name: The instrument this solution targets.
        problem_name: Human-readable problem name.
        steps: Ordered solution chain steps.
        verification_targets: Descriptor targets to verify the fix.
        total_expected_result: Description of the instrument after all
            steps are applied.
    """

    problem_id: str
    instrument_name: str
    problem_name: str
    steps: List[SolutionStep] = field(default_factory=list)
    verification_targets: Dict[str, tuple] = field(default_factory=dict)
    total_expected_result: str = ""


class SolutionEngine:
    """
    Brain 9 — Problem → Solution Engine.

    Takes any identified problem and generates a complete, genius-level
    solution plan with optimal plugin selection and mouse-level
    parameter instructions.
    """

    def __init__(
        self, manual_intelligence, plugin_registry, outcomes_engine
    ) -> None:
        self.manuals = manual_intelligence
        self.registry = plugin_registry
        self.outcomes = outcomes_engine

    # ── Solution generation ──────────────────────────────────────────────────

    def solve(
        self,
        problem,
        available_plugins: List[str],
        instrument_type: str,
    ) -> SolutionPlan:
        """
        Generate a complete solution plan for a single problem.

        TODO: Classify the problem, select optimal plugins based on the
        problem type and available_plugins, design the solution chain,
        and generate exact ParameterOperation instructions for each step.
        The solution must actually fix the problem — not just address it
        superficially.
        """
        raise NotImplementedError(
            "TODO: Implement genius problem → solution plan generation."
        )

    def solve_all(
        self,
        problems: list,
        available_plugins: List[str],
        instrument_types: Dict[str, str],
    ) -> List[SolutionPlan]:
        """
        Generate solution plans for all problems in the master list.

        TODO: Call solve for each problem. Return a complete list —
        every problem must have a solution plan.
        """
        raise NotImplementedError(
            "TODO: Implement batch problem solution generation."
        )

    # ── Plugin selection ─────────────────────────────────────────────────────

    def select_optimal_plugins(
        self,
        problem_type: str,
        problem_category: str,
        available_plugins: List[str],
    ) -> List[str]:
        """
        Select the optimal plugin(s) for a specific problem type from the
        available plugin list.

        TODO: Implement problem-type-to-plugin scoring. Some plugins are
        objectively better for specific problems. This selection must be
        justified — not arbitrary.
        """
        raise NotImplementedError(
            "TODO: Implement problem-type-aware optimal plugin selection."
        )

    # ── Solution quality evaluation ──────────────────────────────────────────

    def evaluate_solution(self, plan: SolutionPlan) -> float:
        """
        Score a solution plan for completeness, specificity, and
        likelihood of actually fixing the problem.

        TODO: Implement a quality rubric that penalises incomplete
        instructions, single-step solutions for complex problems,
        and vague parameter values. Score between 0 and 1.
        """
        raise NotImplementedError(
            "TODO: Implement solution quality evaluation rubric."
        )
