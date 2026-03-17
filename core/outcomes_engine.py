"""
OPERATING SYSTEM BRAIN: Outcomes Definition Engine
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This brain holds strict, embedded definitions for every sonic outcome
(glassy, shimmery, plucky, full, spacey, warm, punchy, airy, etc.).
These are NOT vague descriptions — they are precise, actionable
specifications that drive every downstream decision in the app.

Default AI thinking says "shimmery = add high frequencies." That is
garbage. This brain knows that "shimmery" on a hi-hat means one set
of exact timbral targets; "shimmery" on a synth pad means an entirely
different set. Per-instrument nuance is non-negotiable.

When multiple outcomes are stacked on a single instrument, this brain
knows exactly how to weight, balance, and resolve conflicts between them
without producing mush. The result is always specific, always creative,
never compromised.

Protocol:
  1. Every outcome has an explicit definition stored as structured data.
  2. Every outcome definition is per-instrument-type — kicks, snares,
     hi-hats, synths, pianos, basses, guitars each have their own lens.
  3. Stacked outcomes are resolved via a priority + balance matrix, not
     a naive average.
  4. Every outcome maps to a set of measurable audio descriptor targets
     (spectral centroid range, transient shape, dynamic envelope, etc.)
     so that the Verification System can confirm whether the outcome
     has been achieved.
"""

# TODO: Design this brain with Cursor — define the full outcome
# taxonomy, per-instrument definition matrix, and stacking resolution
# logic before writing any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class OutcomeDescriptor:
    """
    A single, instrument-scoped sonic outcome definition.

    Attributes:
        name: The outcome label (e.g. "shimmery", "full", "punchy").
        instrument_type: The instrument category this definition applies to.
        description: Human-readable explanation of what this outcome means
            for this instrument — not generic, not vague.
        spectral_targets: Target ranges for Essentia spectral descriptors.
        dynamic_targets: Target shapes for envelope/dynamic behaviour.
        timbral_notes: Specific timbral characteristics to achieve.
        plugin_parameter_hints: Starting-point parameter directions inside
            common plugins (populated by ManualIntelligenceSystem).
    """

    name: str
    instrument_type: str
    description: str
    spectral_targets: Dict[str, tuple] = field(default_factory=dict)
    dynamic_targets: Dict[str, tuple] = field(default_factory=dict)
    timbral_notes: List[str] = field(default_factory=list)
    plugin_parameter_hints: Dict[str, str] = field(default_factory=dict)


class OutcomesDefinitionEngine:
    """
    Brain 1 — Outcomes Definition Engine.

    Holds the master library of per-instrument sonic outcome definitions
    and provides lookup, stacking, and conflict-resolution services to
    every other brain in the system.
    """

    def __init__(self) -> None:
        # TODO: Load the full outcome definition library from
        # config.OUTCOMES_DEFINITIONS_FILE (JSON) at startup.
        self._library: Dict[str, Dict[str, OutcomeDescriptor]] = {}

    # ── Library management ──────────────────────────────────────────────────

    def load_definitions(self, definitions_path: str) -> None:
        """
        Load all outcome definitions from a JSON definitions file.

        TODO: Parse the definitions file and populate self._library keyed
        by (instrument_type, outcome_name). Validate every entry for
        completeness — missing fields are not acceptable.
        """
        raise NotImplementedError(
            "TODO: Implement definition loading from JSON. "
            "Every outcome must be fully defined before this returns."
        )

    def get_definition(
        self, outcome: str, instrument_type: str
    ) -> OutcomeDescriptor:
        """
        Retrieve the precise definition for an outcome on a specific
        instrument type.

        TODO: Return the exact OutcomeDescriptor. If the combination does
        not exist, raise a descriptive error — do not fall back to a
        generic definition.
        """
        raise NotImplementedError(
            "TODO: Implement per-instrument outcome lookup."
        )

    # ── Stacking and balancing ───────────────────────────────────────────────

    def resolve_stacked_outcomes(
        self, outcomes: List[str], instrument_type: str
    ) -> List[OutcomeDescriptor]:
        """
        Given a list of stacked outcomes for one instrument, resolve any
        conflicts and return an ordered, balanced list of descriptors that
        can be applied together without producing contradictory instructions.

        TODO: Implement the priority + balance matrix. When "full" and
        "airy" are both requested for a synth pad, the system must know
        exactly how to honour both without one destroying the other.
        """
        raise NotImplementedError(
            "TODO: Implement stacked outcome conflict resolution and "
            "balance matrix for each instrument type."
        )

    # ── Descriptor-to-target mapping ─────────────────────────────────────────

    def get_essentia_targets(
        self, outcome: str, instrument_type: str
    ) -> Dict[str, tuple]:
        """
        Return the Essentia descriptor target ranges that correspond to
        this outcome on this instrument type. Used by the Verification
        System to confirm that an outcome has been achieved.

        TODO: Map every outcome/instrument combination to concrete Essentia
        descriptor ranges (e.g. spectral centroid 4 kHz–8 kHz for a
        "shimmery" hi-hat).
        """
        raise NotImplementedError(
            "TODO: Implement Essentia target mapping per outcome and "
            "instrument type."
        )
