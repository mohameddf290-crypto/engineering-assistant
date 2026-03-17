"""
OPERATING SYSTEM BRAIN: Verification System
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This brain verifies that engineering instructions were followed correctly
and that problems are actually solved — not just attempted. It uses
Essentia to re-analyse the processed audio and delivers a clear binary
result: the problem is fixed, or it is not — and if not, exactly what
still needs to change.

Default AI thinking says "sounds better, nice work." That is garbage.
This brain takes the outcome descriptor targets, runs Essentia on the
re-submitted audio, checks every relevant descriptor against the target
range, and reports pass/fail with specifics. No hedging. No "it's pretty
close." Either it's fixed or it isn't.

Protocol:
  1. Receive the re-submitted audio for an instrument after instructions
     have been applied.
  2. Run the targeted Essentia analysis pipeline for the specific problems
     that were being addressed.
  3. Compare every relevant descriptor against its target range.
  4. Return a VerificationResult: PASS or FAIL with exact descriptor
     readings and remaining gaps.
  5. For FAIL results: generate specific corrective micro-instructions
     (not a repeat of the original instructions — targeted fixes for
     what is still wrong).
  6. This loop runs for every instrument, in both Phase 1 and Phase 2.
  7. Also verifies preset sounds at the very beginning, before arrangement.
"""

# TODO: Design this brain with Cursor — define the descriptor-to-target
# matching logic, the pass/fail threshold system, and the corrective
# micro-instruction generation before writing any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class VerificationStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"


@dataclass
class DescriptorCheck:
    """
    The result of checking a single Essentia descriptor against its target.

    Attributes:
        descriptor_name: Name of the Essentia descriptor.
        target_range: (min, max) target range.
        actual_value: Measured value from re-analysis.
        passed: Whether the actual value is within the target range.
        delta: How far off the actual value is from the nearest target boundary.
    """

    descriptor_name: str
    target_range: tuple
    actual_value: float
    passed: bool
    delta: float = 0.0


@dataclass
class VerificationResult:
    """
    The complete verification result for a single instrument after one
    round of engineering instructions.

    Attributes:
        instrument_name: The instrument being verified.
        phase: "source_prep", "clean_mix", or "ideal_mix".
        status: PASS, FAIL, or PARTIAL.
        descriptor_checks: Per-descriptor check results.
        corrective_instructions: Targeted fix instructions for any
            failing descriptors (empty if status is PASS).
        summary: Human-readable summary of the result.
    """

    instrument_name: str
    phase: str
    status: VerificationStatus
    descriptor_checks: List[DescriptorCheck] = field(default_factory=list)
    corrective_instructions: List[str] = field(default_factory=list)
    summary: str = ""


class VerificationSystem:
    """
    Brain 12 — Verification System.

    Uses Essentia to confirm whether engineering instructions were
    executed correctly and whether problems are genuinely solved.
    Delivers binary pass/fail results with targeted corrective feedback
    for any failing cases.
    """

    def __init__(self, essentia_integration, outcomes_engine) -> None:
        self.essentia = essentia_integration
        self.outcomes = outcomes_engine

    # ── Verification ─────────────────────────────────────────────────────────

    def verify_instrument(
        self,
        instrument_name: str,
        audio_path: str,
        instrument_type: str,
        phase: str,
        target_descriptors: Dict[str, tuple],
    ) -> VerificationResult:
        """
        Verify that a re-submitted instrument audio meets its target
        descriptor ranges.

        TODO: Run Essentia on audio_path for the relevant descriptor set,
        compare each result to target_descriptors, and produce a
        VerificationResult. For any failing descriptor, generate a
        corrective micro-instruction using the ManualIntelligenceSystem.
        """
        raise NotImplementedError(
            "TODO: Implement Essentia-based instrument verification with "
            "corrective instruction generation."
        )

    def verify_preset_sound(
        self,
        instrument_name: str,
        audio_path: str,
        instrument_type: str,
        outcome_targets: List[str],
    ) -> VerificationResult:
        """
        Verify a preset sound at the very beginning of the workflow
        (before arrangement) to confirm it's ready for use.

        TODO: Run the pre-arrangement verification pass. Check that the
        source sound already matches or is reasonably close to the outcome
        targets before the user starts arranging.
        """
        raise NotImplementedError(
            "TODO: Implement pre-arrangement preset sound verification."
        )

    def verify_all(
        self,
        instruments: list,
        audio_paths: Dict[str, str],
        phase: str,
    ) -> List[VerificationResult]:
        """
        Run verification for every instrument in the current phase.

        TODO: Iterate over instruments, call verify_instrument for each,
        and return the full results list. Log any FAIL or PARTIAL results
        prominently.
        """
        raise NotImplementedError(
            "TODO: Implement batch instrument verification."
        )

    # ── Corrective instruction generation ────────────────────────────────────

    def generate_corrective_instructions(
        self,
        descriptor_checks: List[DescriptorCheck],
        instrument_name: str,
        instrument_type: str,
        plugin_name: str,
    ) -> List[str]:
        """
        Generate targeted corrective instructions for all failing
        descriptor checks on an instrument.

        TODO: For each failing descriptor, determine the exact parameter
        adjustment needed and generate a precise, mouse-level corrective
        instruction using the ManualIntelligenceSystem.
        """
        raise NotImplementedError(
            "TODO: Implement corrective instruction generation from "
            "failing descriptor checks."
        )
