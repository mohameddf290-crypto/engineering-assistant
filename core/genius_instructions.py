"""
OPERATING SYSTEM BRAIN: Genius Instructions Engine
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This brain thinks like a top-tier producer. It designs multi-plugin
effect chains where each plugin's contribution builds on the last,
and the combined result is something that rivals what a genius engineer
would create — not something a chatbot would suggest.

Default AI thinking says "add an EQ and compressor." That is garbage.
This brain says: "Run the synth into Soundtoys Decapitator on Style A
with Drive at 40% to add controlled harmonic saturation. Then into
FabFilter Pro-Q 3 — high-shelf boost at 8 kHz of +3 dB, Q = 0.7, to
bring the shimmer forward. Then into iZotope Neutron's Transient Shaper
with Attack at -4 dB and Sustain at +2 dB to define the note onset
against the shimmer. The result: the saturation gives it soul, the EQ
gives it air, the transient shaper gives it presence. Fire."

Protocol:
  1. Receive an instrument type, outcome targets, and the current
     problem/gap list for that instrument.
  2. Design a multi-plugin chain that addresses the targets.
  3. Each plugin in the chain has a specific, justified role.
  4. The combined effect of the chain must be describable and intentional.
  5. Instructions for each plugin in the chain are mouse-level exact.
  6. The overall result must be something genuinely excellent — not safe,
     not generic, not the first thing anyone would think of.
"""

# TODO: Design this brain with Cursor — define the chain design
# algorithm, the plugin role taxonomy, and the creativity evaluation
# criteria before writing any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from core.source_preparation import ParameterOperation


@dataclass
class PluginChainStep:
    """
    A single step in a genius effect chain.

    Attributes:
        step_number: Position in the chain (1-indexed).
        plugin_name: Plugin to use at this step.
        role: The creative/sonic role this plugin plays in the chain
            (e.g. "harmonic saturation", "transient definition",
            "spatial width").
        operations: Exact parameter operations to configure this plugin.
        sonic_contribution: Description of what this plugin adds to the
            overall chain result.
    """

    step_number: int
    plugin_name: str
    role: str
    operations: List[ParameterOperation] = field(default_factory=list)
    sonic_contribution: str = ""


@dataclass
class GeniusChain:
    """
    A complete genius effect chain for a single instrument.

    Attributes:
        instrument_name: Target instrument.
        outcome_targets: Outcomes this chain is designed to achieve.
        steps: Ordered list of plugin chain steps.
        combined_effect: Description of the total sonic result of the chain.
        why_its_fire: The creative reasoning behind this chain design.
    """

    instrument_name: str
    outcome_targets: List[str]
    steps: List[PluginChainStep] = field(default_factory=list)
    combined_effect: str = ""
    why_its_fire: str = ""


class GeniusInstructionsEngine:
    """
    Brain 6 — Genius Instructions Engine.

    Designs multi-plugin effect chains with the creativity and precision
    of a world-class producer/engineer. No single-plugin suggestions.
    No generic advice. Only chains where every step is justified and the
    combined result is genuinely excellent.
    """

    def __init__(self, manual_intelligence, outcomes_engine, plugin_registry) -> None:
        self.manuals = manual_intelligence
        self.outcomes = outcomes_engine
        self.registry = plugin_registry

    # ── Chain design ─────────────────────────────────────────────────────────

    def design_chain(
        self,
        instrument_name: str,
        instrument_type: str,
        outcome_targets: List[str],
        available_plugins: List[str],
    ) -> GeniusChain:
        """
        Design a genius effect chain for an instrument targeting specific
        outcomes, using only the plugins in available_plugins.

        TODO: Implement the chain design algorithm. Select plugins based
        on their specific strengths for each outcome target. Order them
        in the signal chain based on sonic logic (not alphabetical, not
        arbitrary). Justify every selection with sonic reasoning.
        The combined_effect must describe something that sounds genuinely
        excellent — if it doesn't, redesign the chain.
        """
        raise NotImplementedError(
            "TODO: Implement genius multi-plugin chain design algorithm."
        )

    def design_all_chains(
        self,
        instruments: list,
        available_plugins: List[str],
    ) -> List[GeniusChain]:
        """
        Design chains for every instrument in the session.

        TODO: Call design_chain for each instrument. Return a complete
        list — no instrument may be left without a chain.
        """
        raise NotImplementedError(
            "TODO: Implement batch genius chain design."
        )

    # ── Chain evaluation ─────────────────────────────────────────────────────

    def evaluate_chain(self, chain: GeniusChain) -> float:
        """
        Score a designed chain for creativity, specificity, and sonic
        soundness. Returns a float between 0 and 1.

        TODO: Implement a scoring rubric that penalises generic plugin
        choices, single-plugin chains, and vague instructions. Only chains
        with a score above a threshold qualify — below threshold triggers
        a redesign.
        """
        raise NotImplementedError(
            "TODO: Implement chain quality evaluation rubric."
        )

    # ── Instruction formatting ───────────────────────────────────────────────

    def format_chain_instructions(self, chain: GeniusChain) -> str:
        """
        Format a GeniusChain into a human-readable, step-by-step
        instruction block ready to deliver to the user.

        TODO: Format each step with its plugin name, role, exact parameter
        operations, and sonic contribution. Include the combined_effect
        and why_its_fire at the end. Output must be clear enough to follow
        without additional context.
        """
        raise NotImplementedError(
            "TODO: Implement genius chain instruction formatter."
        )
