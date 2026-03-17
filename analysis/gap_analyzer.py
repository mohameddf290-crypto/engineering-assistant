"""
Gap Analyzer — Clean Mix vs. Ideal Mix delta analysis.
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This module is the analytical engine for Phase 2. It measures the
precise delta between the clean-mixed song's sonic state and the ideal
outcome targets, producing a structured gap list that the Clean → Ideal
Bridge uses to generate its Phase 2 operations.

This is not a vague "could be better" assessment. It is a quantitative,
descriptor-level delta computation for every instrument, with qualitative
translation into production language.

Protocol:
  1. Receive clean mix analysis results and outcome target profiles.
  2. Compute the delta between current state and targets per descriptor.
  3. Classify gaps by type (spectral, dynamic, spatial, timbral).
  4. Return a structured gap list, per instrument, sorted by gap magnitude.
"""

# TODO: Design this brain with Cursor — define the delta computation
# method, gap classification taxonomy, and output schema before writing
# any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from analysis.essentia_integration import AnalysisResult


@dataclass
class GapEntry:
    """
    A single gap between the current sonic state and the ideal target.

    Attributes:
        descriptor_name: The Essentia descriptor where the gap exists.
        current_value: Measured value from the clean mix.
        target_range: The ideal target range (min, max).
        gap_magnitude: How far outside the target range the current value is.
        gap_direction: "above_target" or "below_target".
        category: Gap category (spectral, dynamic, spatial, timbral).
        human_description: Production-language description of the gap.
    """

    descriptor_name: str
    current_value: float
    target_range: Tuple[float, float]
    gap_magnitude: float
    gap_direction: str
    category: str
    human_description: str = ""


@dataclass
class InstrumentGapReport:
    """
    The complete gap report for a single instrument.

    Attributes:
        instrument_name: The instrument being analysed.
        outcome_targets: The desired outcomes for this instrument.
        gaps: All identified gaps, sorted by magnitude.
        overall_gap_score: Aggregate gap score (0 = ideal, 1 = maximum gap).
        priority: How urgently Phase 2 needs to address this instrument.
    """

    instrument_name: str
    outcome_targets: List[str]
    gaps: List[GapEntry] = field(default_factory=list)
    overall_gap_score: float = 0.0
    priority: int = 99


class GapAnalyzer:
    """
    Computes the delta between the clean mix and the ideal outcome targets
    for every instrument and returns a structured gap list for Phase 2.
    """

    def __init__(self, outcomes_engine, essentia_integration) -> None:
        self.outcomes = outcomes_engine
        self.essentia = essentia_integration

    # ── Gap computation ───────────────────────────────────────────────────────

    def compute_gap(
        self,
        analysis_result: AnalysisResult,
        instrument_name: str,
        instrument_type: str,
        outcome_targets: List[str],
    ) -> InstrumentGapReport:
        """
        Compute the gap report for a single instrument.

        TODO: Retrieve outcome descriptor targets from OutcomesDefinitionEngine.
        Compare each descriptor value in analysis_result against its target.
        Compute gap_magnitude and gap_direction for every out-of-range
        descriptor. Translate each gap into a production-language description.
        """
        raise NotImplementedError(
            "TODO: Implement per-instrument gap computation with outcome "
            "target comparison."
        )

    def compute_all_gaps(
        self,
        analysis_results: Dict[str, AnalysisResult],
        instrument_outcomes: Dict[str, dict],
    ) -> List[InstrumentGapReport]:
        """
        Compute gap reports for all instruments.

        TODO: Call compute_gap for each instrument. Sort the returned list
        by overall_gap_score descending (biggest gaps first). Every
        instrument must be included.
        """
        raise NotImplementedError(
            "TODO: Implement batch gap computation across all instruments."
        )

    # ── Gap classification ────────────────────────────────────────────────────

    def classify_gap(
        self, descriptor_name: str, gap_magnitude: float
    ) -> Dict[str, str]:
        """
        Classify a gap entry by category and produce a human-readable
        description.

        TODO: Map descriptor names to categories (spectral, dynamic,
        spatial, timbral). Generate a human description using production
        language that explains what the gap sounds like.
        """
        raise NotImplementedError(
            "TODO: Implement gap classification and human description "
            "generation."
        )
