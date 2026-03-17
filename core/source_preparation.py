"""
OPERATING SYSTEM BRAIN: Source Preparation Instructor
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This brain delivers mouse-level, parameter-specific instructions for
shaping every selected preset inside its native plugin before a single
note is arranged. Envelopes, oscillators, filters, modulation, effects
chains — all of it, all precise, all tied to the specific plugin UI and
the specific preset loaded.

Default AI thinking says "adjust the attack on your kick to tighten the
transient." That is garbage. This brain says: "In Kick 2, with the
'Heavy 808' preset loaded — go to the BODY section, click the ENVELOPE
tab, set ATTACK to 0 ms, set HOLD to 8 ms, set DECAY to 340 ms. Then
click the CLICK section and set the TONE dial to 9 o'clock."

Every instruction references the actual plugin UI element by name, the
exact value to set, and the exact location to find it. No ambiguity.
No "approximately." No "to taste."

Protocol:
  1. Receive a PresetSelection for each instrument.
  2. Look up the plugin's full parameter knowledge from ManualIntelligenceSystem.
  3. Cross-reference the outcome descriptors for this instrument.
  4. Generate an ordered list of parameter operations, each scoped to a
     named UI element in the actual plugin.
  5. Instructions cover: envelope shaping, oscillator tuning, filter
     configuration, modulation assignment, and effects chain setup.
  6. All values are exact — no ranges, no approximations, no "around."
"""

# TODO: Design this brain with Cursor — define the instruction schema,
# the plugin UI element naming convention, and the outcome-to-parameter
# mapping pipeline before writing any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from core.preset_selector import PresetSelection


@dataclass
class ParameterOperation:
    """
    A single, atomic, mouse-level parameter instruction.

    Attributes:
        plugin_name: The plugin this operation targets.
        section: The plugin UI section (e.g. "BODY > ENVELOPE").
        parameter_name: The exact parameter label as shown in the plugin.
        action: What to do ("set", "click", "drag", "enable", "disable").
        value: The exact value or position to set.
        unit: Unit of the value (ms, dB, Hz, %, etc.).
        notes: Any additional context needed to execute this correctly.
    """

    plugin_name: str
    section: str
    parameter_name: str
    action: str
    value: str
    unit: str = ""
    notes: str = ""


@dataclass
class SourcePrepInstructions:
    """
    The complete source preparation instruction set for a single instrument.

    Attributes:
        instrument_name: The user-defined instrument name.
        preset_name: The loaded preset name.
        plugin_name: The plugin the preset lives in.
        operations: Ordered list of parameter operations to execute.
        outcome_targets: The outcomes these instructions are designed to hit.
    """

    instrument_name: str
    preset_name: str
    plugin_name: str
    operations: List[ParameterOperation] = field(default_factory=list)
    outcome_targets: List[str] = field(default_factory=list)


class SourcePreparationInstructor:
    """
    Brain 5 — Source Preparation Instructor.

    Generates mouse-level, parameter-exact preparation instructions for
    every selected preset inside its native plugin, targeted precisely at
    the user's desired sonic outcomes.
    """

    def __init__(self, manual_intelligence, outcomes_engine) -> None:
        self.manuals = manual_intelligence
        self.outcomes = outcomes_engine

    # ── Instruction generation ───────────────────────────────────────────────

    def generate_instructions(
        self, selection: PresetSelection
    ) -> SourcePrepInstructions:
        """
        Generate the full source preparation instruction set for a single
        instrument's preset selection.

        TODO: Use the ManualIntelligenceSystem to look up every relevant
        parameter for this plugin, cross-reference the OutcomesDefinitionEngine
        targets, and produce an ordered, exact ParameterOperation list.
        Instructions must be complete — no missing steps, no vague values.
        """
        raise NotImplementedError(
            "TODO: Implement full source preparation instruction generation."
        )

    def generate_all(
        self, selections: list
    ) -> List[SourcePrepInstructions]:
        """
        Generate source preparation instructions for every instrument in
        the current session.

        TODO: Iterate over selections and call generate_instructions for
        each. Return a complete list — every instrument must have
        instructions before this method returns.
        """
        raise NotImplementedError(
            "TODO: Implement batch source preparation instruction generation."
        )

    # ── Per-section helpers ──────────────────────────────────────────────────

    def build_envelope_operations(
        self,
        plugin_name: str,
        instrument_type: str,
        outcome_targets: List[str],
    ) -> List[ParameterOperation]:
        """
        Build the envelope-shaping operations for a given plugin,
        instrument type, and target outcomes.

        TODO: Map envelope parameter targets (attack, hold, decay, sustain,
        release) to exact values based on the outcome descriptors. For
        kicks: tight transient = 0 ms attack. For pads: slow attack =
        outcome-driven ms value.
        """
        raise NotImplementedError(
            "TODO: Implement outcome-driven envelope operation generation."
        )

    def build_filter_operations(
        self,
        plugin_name: str,
        instrument_type: str,
        outcome_targets: List[str],
    ) -> List[ParameterOperation]:
        """
        Build the filter-shaping operations for a given plugin and targets.

        TODO: Map filter parameters (cutoff, resonance, type, slope) to
        exact values driven by the outcome timbral targets.
        """
        raise NotImplementedError(
            "TODO: Implement outcome-driven filter operation generation."
        )

    def build_modulation_operations(
        self,
        plugin_name: str,
        instrument_type: str,
        outcome_targets: List[str],
    ) -> List[ParameterOperation]:
        """
        Build modulation assignment operations (LFOs, envelopes routed to
        parameters) for a given plugin and outcome targets.

        TODO: Implement modulation routing logic based on the manual
        knowledge and the outcome targets for this instrument.
        """
        raise NotImplementedError(
            "TODO: Implement outcome-driven modulation operation generation."
        )
