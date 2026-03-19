"""
OPERATING SYSTEM BRAIN: Melody Creation Brain
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

Purpose: The core skill. Creates professional, strong, deep, simple-yet-catchy,
human melodies. Works from any input. Creates both Normal and Hybrid
(chord-melody blend) forms.

Default AI thinking produces pattern-recalled melodic sequences — the same
pentatonic scale runs, the same stepwise scalar passages, the same predictable
rhythmic grids. None of that is a melody. This brain constructs melodies
deliberately, note by note, from creation plans: the contour is shaped
intentionally, the rhythmic pattern is chosen for feel, every note is selected
from the harmonic note pool with a specific purpose. The result is a melody
that feels human — one that surprises, that breathes, that has character.

Normal mode creates a pure melodic line: a single melody that stands on its
own as the primary musical idea. Hybrid mode weaves harmonic elements into the
melody — chord tones that create implied harmony within the melodic line itself,
inspired by how pianists and guitarists comp melodically.

The taste profile is not a post-processing step — it is embedded in every note
selection decision. When a taste profile says "prefer wider intervals," the
brain selects wider intervals from the pool. When it says "favour long sustained
notes," the rhythmic framework is weighted toward longer durations. Musical
coherence is never sacrificed for taste compliance.

Protocols:
  1. Every melody is built note by note from the creation plan. No pattern
     recall. No sequential scale runs. Every note has a purpose.
  2. Normal mode: pure melodic line. Hybrid mode: harmonic elements woven into
     the melodic line — chord tones imply harmony within the melody itself.
  3. Taste profile shapes every decision without sacrificing musical coherence.
     Conflicts between taste and coherence are resolved with musical intelligence.
"""

# TODO: Design this brain with Cursor — define the full note-by-note
# construction algorithm: how contour shapes map to interval choices, how
# the rhythmic framework drives note duration selection, how the note pool
# priority weighting influences selection probability, the hybrid melody
# construction rules, and the melodic quality validation criteria.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from melodies.translation import MelodyCreationPlan


@dataclass
class MelodyNote:
    """
    A single note in a melody with full annotation.

    Attributes:
        pitch_midi: MIDI note number (0–127).
        duration_beats: Duration of the note in beats.
        position_beats: Start position of the note in beats (from bar 1 beat 1).
        velocity: MIDI velocity (1–127).
        is_chord_tone: True if this note is a chord tone of the underlying harmony.
        role_annotation: Brief annotation of the note's melodic role (e.g. "peak", "approach", "passing").
    """

    pitch_midi: int
    duration_beats: float
    position_beats: float
    velocity: int = 80
    is_chord_tone: bool = False
    role_annotation: str = ""


@dataclass
class Melody:
    """
    A complete melody with notes and metadata.

    Attributes:
        notes: Ordered list of MelodyNote objects.
        key: Tonal centre (e.g. "C", "F#").
        scale: Scale/mode (e.g. "major", "dorian").
        length_bars: Total length in bars.
        role: Melodic role (e.g. "lead", "counter_melody", "ear_candy").
        complexity_level: Complexity on a 1–10 scale.
        mode: Generation mode ("normal" or "hybrid").
        creation_plan_ref: Reference to the MelodyCreationPlan used.
        taste_profile_ref: Reference to the taste profile applied.
    """

    notes: List[MelodyNote] = field(default_factory=list)
    key: str = ""
    scale: str = ""
    length_bars: int = 4
    role: str = "lead"
    complexity_level: int = 5
    mode: str = "normal"
    creation_plan_ref: Optional[str] = None
    taste_profile_ref: Optional[str] = None


class MelodyCreationBrain:
    """
    Brain M4 — Melody Creation Brain.

    The core melody generation engine. Constructs professional, human-quality
    melodies note by note from MelodyCreationPlans with taste profile influence.
    """

    def __init__(self) -> None:
        self._construction_rules: Dict[str, object] = {}

    def create_from_plan(
        self,
        creation_plan: MelodyCreationPlan,
        taste_profile: Dict[str, object],
    ) -> Melody:
        """
        Generate a complete Melody from a creation plan and taste profile.

        TODO: Implement the full generation pipeline: build_melodic_contour →
        select_notes_from_pool → apply_rhythmic_framework → apply taste profile
        → validate_melodic_quality. Return a fully annotated Melody.
        """
        raise NotImplementedError(
            "TODO: Implement full melody generation pipeline. Note-by-note "
            "construction from plan — no pattern recall."
        )

    def build_melodic_contour(
        self, plan: MelodyCreationPlan
    ) -> List[str]:
        """
        Build the melodic contour skeleton from the creation plan.

        Returns a list of directional movement instructions (e.g.
        ["up-step", "up-leap", "down-step", "hold"]).

        TODO: Implement contour construction from plan.contour_target and
        plan.phrasing_plan. The contour skeleton drives interval selection in
        the subsequent note selection step.
        """
        raise NotImplementedError(
            "TODO: Implement contour skeleton construction. Output is a "
            "directional movement sequence that drives note selection."
        )

    def select_notes_from_pool(
        self,
        contour: List[str],
        note_pool: List[int],
        harmonic_context: Dict[str, object],
    ) -> List[MelodyNote]:
        """
        Select specific MIDI notes from the note pool following the contour skeleton.

        TODO: Implement note selection: for each contour step, choose a MIDI
        note from note_pool that satisfies the direction and interval target.
        Apply priority weighting (chord tones preferred on strong beats).
        Respect avoid notes on strong beats.
        """
        raise NotImplementedError(
            "TODO: Implement note selection from pool. Contour drives direction; "
            "priority weighting drives specific note choice. Avoid notes enforced."
        )

    def apply_rhythmic_framework(
        self,
        notes: List[MelodyNote],
        rhythmic_framework: Dict[str, float],
    ) -> List[MelodyNote]:
        """
        Apply the rhythmic framework to a sequence of pitched notes.

        TODO: Assign durations and positions to the pitched notes based on
        the rhythmic framework (onset density, syncopation level, grid alignment).
        The result must feel rhythmically human — not a mechanical grid.
        """
        raise NotImplementedError(
            "TODO: Implement rhythmic framework application. Assign durations "
            "and positions that feel human and match the framework targets."
        )

    def create_hybrid_melody(
        self,
        plan: MelodyCreationPlan,
        chord_progression: object,
        taste_profile: Dict[str, object],
    ) -> Melody:
        """
        Create a hybrid melody that weaves chord tones into the melodic line.

        TODO: Implement hybrid construction: select chord tones at structurally
        important moments (phrase starts, peaks, cadences) and weave non-chord
        melodic elements around them. The result implies harmony within the
        single melodic line.
        """
        raise NotImplementedError(
            "TODO: Implement hybrid melody creation. Chord tones at structural "
            "moments; melodic elements woven between them."
        )

    def validate_melodic_quality(self, melody: Melody) -> bool:
        """
        Validate that a generated melody meets the quality threshold.

        Returns True if the melody passes all quality checks.

        TODO: Implement quality checks: contour coherence, rhythmic variety,
        phrase structure validity, avoid note violations, taste profile
        alignment, overall musical interest threshold.
        """
        raise NotImplementedError(
            "TODO: Implement melodic quality validation. All structural, "
            "harmonic, and musical interest checks must pass."
        )
