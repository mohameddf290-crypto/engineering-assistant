"""
OPERATING SYSTEM BRAIN: Preset Update System
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This brain listens to the fully arranged song in context — not just
individual presets in isolation — and determines which presets should be
kept, replaced, or layered. It does this twice: once at Checkpoint 1
(comprehensive) and once at Checkpoint 2 (lighter, focused on final
source polish). The decisions it makes are contextually justified and
explained.

Default AI thinking says "these presets match the outcomes, keep them."
That is garbage. This brain hears how the arrangement breathes as a whole.
It detects masking, frequency crowding, and character conflicts between
instruments in context. A preset that sounded perfect in isolation might
be completely wrong in the arrangement — and this brain knows it.

Protocol:
  1. Receive the full mix audio + individual stems + bus stems.
  2. Run Essentia analysis on the full mix and on each stem in context.
  3. Compare actual in-context sonic character against the outcome targets.
  4. Identify presets that are conflicting, masking, or underperforming.
  5. For each identified issue: propose keep / replace / layer decision
     with full reasoning.
  6. Checkpoint 1: comprehensive — any preset can be replaced.
     Checkpoint 2: lighter — focus on layering and safe final tweaks only.
"""

# TODO: Design this brain with Cursor — define the in-context analysis
# strategy, the conflict/masking detection logic, and the keep/replace/
# layer decision algorithm before writing any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class UpdateDecision(Enum):
    KEEP = "keep"
    REPLACE = "replace"
    LAYER = "layer"
    TWEAK = "tweak"


@dataclass
class PresetUpdateRecommendation:
    """
    A single preset update recommendation for one instrument.

    Attributes:
        instrument_name: The instrument being reviewed.
        current_preset: Name of the currently loaded preset.
        decision: Keep, replace, layer, or tweak.
        replacement_preset_id: ID of the recommended replacement preset
            (if decision is REPLACE).
        layer_preset_id: ID of the preset to layer on top
            (if decision is LAYER).
        reasoning: Full explanation of why this decision was made.
        priority: How urgent this update is (1 = must-do, 3 = optional).
        checkpoint: 1 or 2 — which checkpoint this recommendation applies to.
    """

    instrument_name: str
    current_preset: str
    decision: UpdateDecision
    replacement_preset_id: Optional[str] = None
    layer_preset_id: Optional[str] = None
    reasoning: str = ""
    priority: int = 1
    checkpoint: int = 1


class PresetUpdater:
    """
    Brain 11 — Preset Update System.

    Listens to the arranged song in context and generates contextually
    justified preset update recommendations at Checkpoint 1 and
    Checkpoint 2.
    """

    def __init__(
        self, essentia_integration, preset_library, outcomes_engine
    ) -> None:
        self.essentia = essentia_integration
        self.library = preset_library
        self.outcomes = outcomes_engine

    # ── Checkpoint 1: comprehensive update ──────────────────────────────────

    def run_checkpoint1(
        self,
        full_mix_path: str,
        stem_paths: List[str],
        bus_stem_paths: List[str],
        current_selections: list,
    ) -> List[PresetUpdateRecommendation]:
        """
        Run the comprehensive Checkpoint 1 preset update analysis.

        TODO: Load audio files, run in-context Essentia analysis, compare
        each instrument's sonic character to its outcome targets in the
        context of the full mix, and generate update recommendations.
        Any preset can be replaced at this stage.
        """
        raise NotImplementedError(
            "TODO: Implement Checkpoint 1 comprehensive preset update "
            "analysis with in-context Essentia evaluation."
        )

    # ── Checkpoint 2: lighter update ────────────────────────────────────────

    def run_checkpoint2(
        self,
        full_mix_path: str,
        stem_paths: List[str],
        bus_stem_paths: List[str],
        current_selections: list,
    ) -> List[PresetUpdateRecommendation]:
        """
        Run the lighter Checkpoint 2 preset update analysis.

        TODO: Focus on layering opportunities and safe final source
        decisions. No wholesale replacements at this stage — only
        additions and light tweaks. Recommendations at Checkpoint 2
        must be explicitly marked optional where appropriate.
        """
        raise NotImplementedError(
            "TODO: Implement Checkpoint 2 lighter preset update analysis."
        )

    # ── Conflict and masking detection ──────────────────────────────────────

    def detect_conflicts(
        self,
        full_mix_path: str,
        stem_paths: List[str],
    ) -> List[dict]:
        """
        Detect frequency masking, character conflicts, and crowding
        between instruments in the context of the full mix.

        TODO: Use Essentia spectral analysis across stems to identify
        frequency range overlaps that are causing masking. Flag instruments
        whose character is being buried or altered by neighbouring stems.
        """
        raise NotImplementedError(
            "TODO: Implement in-context conflict and masking detection."
        )
