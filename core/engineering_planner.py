"""
OPERATING SYSTEM BRAIN: Engineering Planner
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This brain reads the full problem list for the entire song and produces
an intricate, phased, per-instrument engineering plan. It does this for
BOTH Phase 1 (clean mix) and Phase 2 (clean → ideal). It understands
the order of operations, the dependencies between instruments, and the
cumulative effect of processing decisions across the mix.

Default AI thinking says "fix these problems in this order." That is
garbage. This brain maps inter-instrument relationships (kick/bass
relationship, lead/reverb tail interaction, etc.), determines the optimal
processing sequence, separates the plan into named phases, and delivers
a per-instrument breakdown that a professional engineer would be proud to
execute.

Protocol:
  1. Receive the full problem list (from Problem Detection Aggregator).
  2. Group problems by instrument and by type (spectral, dynamic, spatial,
     timbral, temporal).
  3. Identify inter-instrument dependencies and note processing order
     requirements (e.g. kick must be addressed before bass sub tuning).
  4. Create a phased plan: Phase 1 is clean mix; Phase 2 is clean → ideal.
  5. For each phase, produce a per-instrument instruction plan with
     sequenced operations.
  6. Flag any operations that are contingent on another instrument
     being completed first.
"""

# TODO: Design this brain with Cursor — define the problem grouping
# taxonomy, the inter-instrument dependency graph, and the phase
# structure before writing any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class InstrumentPlan:
    """
    The engineering plan for a single instrument within a phase.

    Attributes:
        instrument_name: The instrument this plan targets.
        phase: "clean_mix" or "ideal_mix".
        problems_addressed: List of problem IDs from the problem list.
        operations: Ordered list of operation descriptions.
        dependencies: Names of other instruments that must be processed
            before this plan can be executed.
        priority: Processing priority (1 = highest).
    """

    instrument_name: str
    phase: str
    problems_addressed: List[str] = field(default_factory=list)
    operations: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    priority: int = 99


@dataclass
class EngineeringPlan:
    """
    The complete, phased engineering plan for the full song.

    Attributes:
        phase1_plans: Per-instrument plans for the clean mix phase.
        phase2_plans: Per-instrument plans for the clean → ideal phase.
        global_notes: Mix-wide observations and sequencing notes.
        total_problems: Total number of problems being addressed.
    """

    phase1_plans: List[InstrumentPlan] = field(default_factory=list)
    phase2_plans: List[InstrumentPlan] = field(default_factory=list)
    global_notes: List[str] = field(default_factory=list)
    total_problems: int = 0


class EngineeringPlanner:
    """
    Brain 10 — Engineering Planner.

    Reads the full problem and gap lists, understands inter-instrument
    relationships, and produces a phased, sequenced engineering plan for
    both clean mix and ideal mix phases.
    """

    def __init__(self, outcomes_engine, manual_intelligence) -> None:
        self.outcomes = outcomes_engine
        self.manuals = manual_intelligence

    # ── Plan creation ─────────────────────────────────────────────────────────

    def create_phase1_plan(self, problem_list: List[Dict]) -> List[InstrumentPlan]:
        """
        Create the Phase 1 (clean mix) engineering plan from the full
        problem list.

        TODO: Group problems by instrument, determine processing order
        based on inter-instrument dependencies, and generate sequenced
        InstrumentPlan objects for each instrument. The plan must be
        complete — no problem left unaddressed.
        """
        raise NotImplementedError(
            "TODO: Implement Phase 1 engineering plan creation from "
            "problem list with inter-instrument dependency awareness."
        )

    def create_phase2_plan(self, gap_list: List[Dict]) -> List[InstrumentPlan]:
        """
        Create the Phase 2 (clean → ideal) engineering plan from the
        gap list.

        TODO: Map each gap to operations that bridge it, accounting for
        the fact that the song is already cleanly mixed at this point.
        Phase 2 operations are creative and outcome-driven — not just
        problem-fixing.
        """
        raise NotImplementedError(
            "TODO: Implement Phase 2 engineering plan creation from "
            "gap list with creative outcome-bridging logic."
        )

    def build_full_plan(
        self, problem_list: List[Dict], gap_list: List[Dict]
    ) -> EngineeringPlan:
        """
        Build the complete EngineeringPlan covering both phases.

        TODO: Call create_phase1_plan and create_phase2_plan, combine
        the results, identify global mix notes, and return the assembled
        EngineeringPlan.
        """
        raise NotImplementedError(
            "TODO: Implement full two-phase engineering plan assembly."
        )

    # ── Dependency resolution ─────────────────────────────────────────────────

    def resolve_dependencies(
        self, plans: List[InstrumentPlan]
    ) -> List[InstrumentPlan]:
        """
        Sort and annotate plans based on inter-instrument processing
        dependencies.

        TODO: Implement a topological sort over the dependency graph.
        Plans with dependencies must appear after their prerequisites in
        the returned list. Detect and raise on circular dependencies.
        """
        raise NotImplementedError(
            "TODO: Implement inter-instrument dependency resolution and "
            "topological ordering."
        )

    # ── Plan formatting ───────────────────────────────────────────────────────

    def format_plan(self, plan: EngineeringPlan) -> str:
        """
        Format the engineering plan as a human-readable, structured
        document ready to deliver to the user.

        TODO: Format each phase, each instrument plan, and all operations
        in a clear, numbered, scannable format. Include dependency notes
        and global mix notes.
        """
        raise NotImplementedError(
            "TODO: Implement engineering plan formatter."
        )
