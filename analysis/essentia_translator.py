"""
OPERATING SYSTEM BRAIN: Essentia Translator
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This brain converts raw Essentia descriptor output into human-readable,
actionable problem statements. A spectral centroid value means nothing to
a producer. A statement like "The hi-hat's high-frequency energy is 14 dB
below where it needs to be for a shimmery character — it sounds dull and
buried" means everything.

Default AI thinking says "spectral_centroid = 2341 Hz." That is garbage.
This brain maps every descriptor value to a production-language problem
statement, scoped to the instrument and the target outcome, with a clear
description of what it sounds like and what the consequence is.

Protocol:
  1. Receive an AnalysisResult from the EssentiaIntegration brain.
  2. For each descriptor that falls outside acceptable ranges, generate
     a named, scoped problem statement.
  3. Problem statements are written in production language — the words a
     professional engineer uses, not math notation.
  4. Every problem statement includes: the descriptor name (internal),
     the human-readable problem name, what it sounds like, the
     instrument it affects, and an urgency level.
  5. Output is a structured list of Problem objects, not a prose paragraph.
  6. Problems are grouped by instrument and sorted by urgency.
"""

# TODO: Design this brain with Cursor — define the full descriptor-to-
# problem mapping table, the problem statement template, and the urgency
# classification system before writing any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List

from analysis.essentia_integration import AnalysisResult


class ProblemUrgency(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Problem:
    """
    A single, instrument-scoped audio problem statement.

    Attributes:
        problem_id: Unique identifier for this problem instance.
        instrument_name: The instrument this problem affects.
        descriptor_name: The internal Essentia descriptor that flagged this.
        problem_name: Human-readable problem name (e.g. "Dull high end").
        description: What this problem sounds like and why it matters.
        actual_value: The measured descriptor value.
        target_range: The acceptable target range for this descriptor.
        urgency: How critical this problem is to fix.
        category: Problem category (spectral, dynamic, spatial, timbral,
            temporal, harmonic).
    """

    problem_id: str
    instrument_name: str
    descriptor_name: str
    problem_name: str
    description: str
    actual_value: float
    target_range: tuple
    urgency: ProblemUrgency
    category: str = "spectral"


class EssentiaTranslator:
    """
    Brain 8 — Essentia Translator.

    Converts raw Essentia analysis results into a structured, human-
    readable problem list using a custom-coded descriptor-to-problem
    mapping system.
    """

    def __init__(self, outcomes_engine) -> None:
        self.outcomes = outcomes_engine
        # TODO: Load the full descriptor-to-problem mapping table from
        # a structured data file. Every Essentia descriptor must have
        # a corresponding problem mapping entry.
        self._descriptor_map: Dict[str, dict] = {}

    # ── Translation ──────────────────────────────────────────────────────────

    def translate(
        self,
        result: AnalysisResult,
        instrument_name: str,
        instrument_type: str,
        outcome_targets: List[str],
    ) -> List[Problem]:
        """
        Translate an AnalysisResult for a single instrument into a list
        of Problem objects.

        TODO: Iterate over every descriptor in result.descriptors. For
        each value outside the acceptable range for this instrument type
        and outcome targets, generate a Problem using the descriptor map.
        Sort by urgency.
        """
        raise NotImplementedError(
            "TODO: Implement descriptor-to-problem translation with "
            "instrument-type and outcome-aware target ranges."
        )

    def translate_batch(
        self,
        results: Dict[str, AnalysisResult],
        instrument_outcomes: Dict[str, dict],
    ) -> Dict[str, List[Problem]]:
        """
        Translate analysis results for multiple instruments.

        TODO: Call translate for each instrument's result. Return a dict
        of instrument_name → [Problem]. Every instrument must be included.
        """
        raise NotImplementedError(
            "TODO: Implement batch translation across all instruments."
        )

    # ── Descriptor mapping ───────────────────────────────────────────────────

    def load_descriptor_map(self, map_path: str) -> None:
        """
        Load the descriptor-to-problem mapping table from file.

        TODO: Parse the mapping file and populate self._descriptor_map.
        Validate that every expected Essentia descriptor has a mapping entry.
        Raise if any required mappings are missing.
        """
        raise NotImplementedError(
            "TODO: Implement descriptor mapping table loader."
        )

    def get_target_range(
        self,
        descriptor_name: str,
        instrument_type: str,
        outcome_targets: List[str],
    ) -> tuple:
        """
        Get the acceptable target range for a descriptor given an
        instrument type and its outcome targets.

        TODO: Look up the target range from the outcomes engine and
        the descriptor map. Return (min, max) tuple. Raise if no
        target range is defined for this combination.
        """
        raise NotImplementedError(
            "TODO: Implement per-instrument, per-outcome descriptor "
            "target range lookup."
        )

    # ── Output formatting ────────────────────────────────────────────────────

    def format_problem_list(
        self, problems_by_instrument: Dict[str, List[Problem]]
    ) -> str:
        """
        Format the full problem list as a human-readable document
        ready to deliver to the user.

        TODO: Group by instrument, sort by urgency within each group,
        and format each problem with its name, description, and urgency.
        Output must be clear, scannable, and actionable.
        """
        raise NotImplementedError(
            "TODO: Implement problem list formatter."
        )
