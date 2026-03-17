"""
Problem Detection Aggregator
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This module aggregates problem findings from all detection sources:
Essentia (via the EssentiaTranslator) and all registered plugin analysers
(Neutron 5, SmartEQ, etc.). It deduplicates, merges, and ranks them into
a single, comprehensive, prioritised problem list for the Engineering
Planner and the Problem → Solution Engine.

Protocol:
  1. Receive Problem lists from EssentiaTranslator.
  2. Receive PluginAnalysisResult lists from the PluginAnalyzerRegistry.
  3. Normalise all findings into a common Problem schema.
  4. Deduplicate problems that have been flagged by multiple sources.
  5. Rank by urgency and inter-instrument impact.
  6. Return the final merged, ranked problem list.
"""

# TODO: Design this brain with Cursor — define the deduplication logic,
# the cross-source normalisation schema, and the ranking algorithm
# before writing any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from analysis.essentia_translator import Problem


@dataclass
class AggregatedProblem:
    """
    A deduplicated, merged problem entry from all detection sources.

    Attributes:
        problem_id: Unique identifier.
        instrument_name: Affected instrument.
        problem_name: Human-readable problem name.
        description: Full production-language description.
        sources: Which detectors flagged this (e.g. ["Essentia", "Neutron 5"]).
        urgency: Normalised urgency level.
        category: Problem category.
        confidence: How confident the aggregator is in this problem
            (higher when multiple sources agree).
    """

    problem_id: str
    instrument_name: str
    problem_name: str
    description: str
    sources: List[str] = field(default_factory=list)
    urgency: str = "medium"
    category: str = "spectral"
    confidence: float = 1.0


class ProblemDetector:
    """
    Problem Detection Aggregator.

    Collects findings from all detection sources, normalises and
    deduplicates them, and produces the master problem list for the
    engineering workflow.
    """

    def __init__(
        self,
        essentia_translator,
        plugin_analyzer_registry,
    ) -> None:
        self.translator = essentia_translator
        self.plugin_registry = plugin_analyzer_registry

    # ── Aggregation ───────────────────────────────────────────────────────────

    def aggregate(
        self,
        essentia_problems: Dict[str, List[Problem]],
        plugin_findings: Dict[str, List],
    ) -> List[AggregatedProblem]:
        """
        Aggregate, deduplicate, and rank all problems from all sources.

        TODO: Merge Essentia problems and plugin analyser findings.
        Identify overlapping problems (same instrument, same category)
        and merge them into single AggregatedProblem entries with
        combined source lists and boosted confidence scores.
        Sort by urgency and confidence.
        """
        raise NotImplementedError(
            "TODO: Implement cross-source problem aggregation, "
            "deduplication, and ranking."
        )

    # ── Formatting ────────────────────────────────────────────────────────────

    def format_master_problem_list(
        self, problems: List[AggregatedProblem]
    ) -> str:
        """
        Format the master problem list as a human-readable document.

        TODO: Group by instrument, sort by urgency within each group,
        include source and confidence information. Output must be clear
        and actionable.
        """
        raise NotImplementedError(
            "TODO: Implement master problem list formatter."
        )
