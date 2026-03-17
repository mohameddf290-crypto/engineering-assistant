"""
OPERATING SYSTEM BRAIN: Preset Selection Brain
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This brain maps desired sonic outcomes to the best available presets
across the user's entire plugin library — per instrument type, with full
nuance awareness. For synthesis-capable plugins or any plugin with
tweakable macro parameters, it knows how to CREATE a sound from scratch
rather than being limited to selecting from existing presets.

Default AI thinking says "return the preset whose name contains a keyword
from the outcome label." That is garbage. This brain uses outcome
descriptor targets, sonic library tags, and instrument-type awareness to
select the objectively best match — not a guess, not a keyword hit.

Protocol:
  1. Receive a list of (instrument_type, [outcome_names]) pairs.
  2. For each instrument, query the PresetLibraryManager with outcome tags.
  3. Score every candidate preset against the exact outcome descriptors
     from the OutcomesDefinitionEngine.
  4. For synthesis-capable plugins: if no preset meets the threshold,
     generate a from-scratch sound creation instruction set instead.
  5. Return a selection for every instrument — never leave one unassigned.
  6. Every selection decision is logged with its reasoning.
"""

# TODO: Design this brain with Cursor — define the scoring algorithm,
# the synthesis-capable plugin detection logic, and the from-scratch
# sound creation instruction format before writing any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from core.preset_library import PresetEntry


@dataclass
class PresetSelection:
    """
    The result of a preset selection decision for a single instrument.

    Attributes:
        instrument_name: The user-defined instrument name (e.g. "lead synth").
        instrument_type: Category (synth, piano, kick, hi_hat, snare, etc.).
        requested_outcomes: The outcome labels the user requested.
        selected_preset: The chosen PresetEntry (or None if from-scratch).
        from_scratch: True if the selection is a synthesised-from-scratch
            sound rather than an existing preset.
        from_scratch_instructions: Step-by-step parameter instructions for
            creating the sound from scratch (populated when from_scratch=True).
        fit_score: Numeric score (0–1) of how well the selection matches
            the requested outcomes.
        reasoning: Human-readable explanation of why this selection was made.
    """

    instrument_name: str
    instrument_type: str
    requested_outcomes: List[str]
    selected_preset: Optional[PresetEntry] = None
    from_scratch: bool = False
    from_scratch_instructions: List[str] = field(default_factory=list)
    fit_score: float = 0.0
    reasoning: str = ""


class PresetSelectionBrain:
    """
    Brain 4 — Preset Selection Brain.

    Produces the best preset selection (or from-scratch creation plan)
    for every instrument in the user's session, fully aligned to the
    requested outcome targets.
    """

    def __init__(
        self,
        library_manager,
        outcomes_engine,
        manual_intelligence,
    ) -> None:
        self.library = library_manager
        self.outcomes = outcomes_engine
        self.manuals = manual_intelligence

    # ── Selection ───────────────────────────────────────────────────────────

    def select_for_instrument(
        self,
        instrument_name: str,
        instrument_type: str,
        requested_outcomes: List[str],
    ) -> PresetSelection:
        """
        Select the best preset (or create a from-scratch plan) for a
        single instrument given its desired outcomes.

        TODO: Implement outcome descriptor retrieval, library search,
        scoring, threshold check, and from-scratch fallback logic.
        Every code path must return a valid PresetSelection — never None.
        """
        raise NotImplementedError(
            "TODO: Implement single-instrument preset selection with "
            "from-scratch fallback for synthesis-capable plugins."
        )

    def select_all(
        self,
        instruments: List[Dict[str, Union[str, List[str]]]],
    ) -> List[PresetSelection]:
        """
        Run preset selection for every instrument in the session.

        Args:
            instruments: List of dicts with keys 'name', 'type',
                         and 'outcomes'.

        TODO: Iterate over instruments, call select_for_instrument for
        each, and return the full selection list. Every instrument must
        receive a selection.
        """
        raise NotImplementedError(
            "TODO: Implement batch instrument preset selection."
        )

    # ── Scoring ─────────────────────────────────────────────────────────────

    def score_preset(
        self,
        preset: PresetEntry,
        outcome_descriptors,
        instrument_type: str,
    ) -> float:
        """
        Score how well a preset matches a set of outcome descriptors for
        a given instrument type.

        TODO: Implement multi-dimensional scoring that compares preset
        sonic tags against outcome descriptor targets. Return a float
        between 0 and 1.
        """
        raise NotImplementedError(
            "TODO: Implement outcome-aligned preset scoring."
        )

    # ── From-scratch synthesis ───────────────────────────────────────────────

    def build_from_scratch_instructions(
        self,
        plugin_name: str,
        instrument_type: str,
        requested_outcomes: List[str],
    ) -> List[str]:
        """
        Generate mouse-level, parameter-specific instructions for creating
        a sound from scratch inside a synthesis-capable plugin.

        TODO: Use ManualIntelligenceSystem to pull parameter knowledge and
        generate a step-by-step synthesis recipe that hits all outcome
        targets. Instructions must be exact — not conceptual.
        """
        raise NotImplementedError(
            "TODO: Implement from-scratch sound creation instruction "
            "generation using plugin manual knowledge."
        )
