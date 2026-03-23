"""
OPERATING SYSTEM BRAIN: Infinity Engine (Melodies)
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

Purpose: Generates infinite melodies from any input without any quality
degradation.

Default AI thinking says "re-run the same generator with different random seeds
and hope for variance." Seeds produce minor surface variations while the
underlying pattern — same scale runs, same rhythmic grid, same contour shape —
remains identical. This brain defines a structured melodic variation space:
every variation has explicit axes (contour, rhythm, note selection), and
movement through the space is deliberate, not random. Quality is enforced on
every generation with zero tolerance for degradation.

Similar regeneration preserves melodic DNA: the contour shape, rhythmic
character, and note vocabulary stay recognisably similar while specific note
choices, rhythmic placements, and phrase details change. It feels like a
different take on the same melodic idea.

Different regeneration applies contrast operators across all three dimensions
simultaneously: contour is inverted or transformed, rhythmic density is shifted,
note selection is biased toward different pool priorities. The result is
genuinely different — a new melodic idea in the same harmonic framework.

Protocols:
  1. Similar regeneration preserves melodic DNA (contour, rhythm) while
     varying specific note choices and phrasing details.
  2. Different regeneration applies contrast operators across contour, rhythm,
     and note selection simultaneously — not just one dimension.
  3. Quality gate runs on every melody — no degradation tolerated. Failure
     triggers immediate regeneration up to max_attempts.
"""

# TODO: Design this brain with Cursor — define the melodic variation space:
# similarity axes (what constitutes melodic DNA vs. surface detail), contrast
# operators for each dimension, quality gate criteria for melodies, and the
# failure protocol when max_attempts is reached.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from melodies.melody_creator import Melody, MelodyNote


@dataclass
class MelodyGenerationRequest:
    """
    A request for infinity-engine melody generation.

    Attributes:
        source_melody: The melody to vary from.
        variation_mode: Either "similar" or "different".
        similarity_score: Target similarity 0.0 (completely different) to 1.0 (identical).
        taste_profile: User taste profile to apply during generation.
        role: Target melodic role for the generated melody.
        max_attempts: Maximum regeneration attempts if quality gate fails.
    """

    source_melody: Melody
    variation_mode: str
    similarity_score: float = 0.7
    taste_profile: Dict[str, object] = field(default_factory=dict)
    role: str = "lead"
    max_attempts: int = 10


class MelodyInfinityEngine:
    """
    Brain M5 — Infinity Engine (Melodies).

    Generates unlimited high-quality melodies from any source melody with
    zero quality degradation across the generation space.
    """

    def __init__(self) -> None:
        self._variation_space: Dict[str, object] = {}
        self._quality_threshold: float = 0.75

    def build_melodic_variation_space(
        self, source_melody: Melody
    ) -> Dict[str, object]:
        """Analyse the source melody and define variation axes."""
        notes = source_melody.notes
        if not notes:
            self._variation_space = {
                "contour": [],
                "rhythmic_pattern": [],
                "pitch_classes": set(),
                "register": (60, 72),
                "density": 0.0,
                "phrase_length": 0,
            }
            return self._variation_space

        # Contour: list of interval directions between consecutive notes
        contour: List[int] = []
        for i in range(1, len(notes)):
            diff = notes[i].pitch_midi - notes[i - 1].pitch_midi
            if diff > 0:
                contour.append(1)
            elif diff < 0:
                contour.append(-1)
            else:
                contour.append(0)

        rhythmic_pattern = [n.duration_beats for n in notes]
        pitch_classes = {n.pitch_midi % 12 for n in notes}
        midi_values = [n.pitch_midi for n in notes]
        register = (min(midi_values), max(midi_values))

        end_positions = [n.position_beats + n.duration_beats for n in notes]
        total_beats = max(end_positions) if end_positions else 1.0
        density = len(notes) / total_beats if total_beats > 0 else 0.0

        self._variation_space = {
            "contour": contour,
            "rhythmic_pattern": rhythmic_pattern,
            "pitch_classes": pitch_classes,
            "register": register,
            "density": density,
            "phrase_length": len(notes),
        }
        return self._variation_space

    def generate_similar(
        self,
        source_melody: Melody,
        taste_profile: Dict[str, object],
    ) -> Melody:
        """Generate a new melody that preserves contour and rhythmic character."""
        import random

        space = self.build_melodic_variation_space(source_melody)
        src_notes = source_melody.notes
        if not src_notes:
            return Melody(
                notes=[],
                key=source_melody.key,
                scale=source_melody.scale,
                length_bars=source_melody.length_bars,
                role=source_melody.role,
            )

        new_notes: list = []
        for note in src_notes:
            shift = random.choice([-2, -1, 0, 1, 2])
            new_pitch = max(0, min(127, note.pitch_midi + shift))
            new_notes.append(
                MelodyNote(
                    pitch_midi=new_pitch,
                    duration_beats=note.duration_beats,
                    position_beats=note.position_beats,
                    velocity=max(1, min(127, note.velocity + random.randint(-5, 5))),
                    is_chord_tone=note.is_chord_tone,
                    role_annotation=note.role_annotation,
                )
            )

        melody = Melody(
            notes=new_notes,
            key=source_melody.key,
            scale=source_melody.scale,
            length_bars=source_melody.length_bars,
            role=source_melody.role,
            complexity_level=source_melody.complexity_level,
            mode=source_melody.mode,
        )

        if not self.apply_quality_gate(melody):
            return self.generate_similar(source_melody, taste_profile)
        return melody

    def generate_different(
        self,
        source_melody: Melody,
        taste_profile: Dict[str, object],
    ) -> Melody:
        """Generate a genuinely different melody using contrast operators."""
        import random

        space = self.build_melodic_variation_space(source_melody)
        src_notes = source_melody.notes
        if not src_notes:
            return Melody(
                notes=[],
                key=source_melody.key,
                scale=source_melody.scale,
                length_bars=source_melody.length_bars,
                role=source_melody.role,
            )

        contour = space.get("contour", [])
        inverted_contour = [-d for d in contour]
        transposition = random.choice([5, 6, 7, -5, -6, -7])

        new_notes: list = []
        current_pitch = src_notes[0].pitch_midi + transposition
        current_pitch = max(30, min(100, current_pitch))
        density_factor = random.choice([0.5, 1.5, 2.0])

        for i, note in enumerate(src_notes):
            if i == 0:
                pitch = current_pitch
            else:
                direction = inverted_contour[i - 1] if i - 1 < len(inverted_contour) else 0
                step = random.randint(1, 4) * direction
                pitch = current_pitch + step
                pitch = max(30, min(100, pitch))
                current_pitch = pitch

            new_dur = note.duration_beats * density_factor
            new_dur = max(0.25, min(4.0, new_dur))

            new_notes.append(
                MelodyNote(
                    pitch_midi=pitch,
                    duration_beats=new_dur,
                    position_beats=note.position_beats,
                    velocity=random.randint(65, 95),
                    is_chord_tone=False,
                    role_annotation="",
                )
            )

        melody = Melody(
            notes=new_notes,
            key=source_melody.key,
            scale=source_melody.scale,
            length_bars=source_melody.length_bars,
            role=source_melody.role,
            complexity_level=source_melody.complexity_level,
            mode=source_melody.mode,
        )

        if not self.apply_quality_gate(melody):
            return self.generate_different(source_melody, taste_profile)
        return melody

    def generate_variation(
        self,
        source_melody: Melody,
        similarity_score: float,
        taste_profile: Dict[str, object],
    ) -> Melody:
        """Interpolate between similar (1.0) and different (0.0)."""
        import random

        similarity_score = max(0.0, min(1.0, similarity_score))

        if similarity_score >= 0.7:
            return self.generate_similar(source_melody, taste_profile)
        if similarity_score <= 0.3:
            return self.generate_different(source_melody, taste_profile)

        # Blend: use similar as base, then apply partial contrast
        similar = self.generate_similar(source_melody, taste_profile)
        blend_ratio = 1.0 - similarity_score  # how much "different" to mix in

        new_notes: list = []
        for note in similar.notes:
            if random.random() < blend_ratio:
                shift = random.choice([-5, -4, -3, 3, 4, 5])
                pitch = max(30, min(100, note.pitch_midi + shift))
            else:
                pitch = note.pitch_midi

            dur_factor = 1.0 + (random.random() - 0.5) * blend_ratio
            dur = max(0.25, min(4.0, note.duration_beats * dur_factor))

            new_notes.append(
                MelodyNote(
                    pitch_midi=pitch,
                    duration_beats=dur,
                    position_beats=note.position_beats,
                    velocity=note.velocity,
                    is_chord_tone=note.is_chord_tone,
                    role_annotation=note.role_annotation,
                )
            )

        melody = Melody(
            notes=new_notes,
            key=source_melody.key,
            scale=source_melody.scale,
            length_bars=source_melody.length_bars,
            role=source_melody.role,
            complexity_level=source_melody.complexity_level,
            mode=source_melody.mode,
        )

        if not self.apply_quality_gate(melody):
            return self.generate_variation(source_melody, similarity_score, taste_profile)
        return melody

    def apply_quality_gate(self, melody: Melody) -> bool:
        """Return True if the melody meets minimum quality criteria."""
        notes = melody.notes
        if len(notes) < 4:
            return False

        unique_pitches = {n.pitch_midi for n in notes}
        if len(unique_pitches) <= 3:
            return False

        midi_vals = [n.pitch_midi for n in notes]
        pitch_range = max(midi_vals) - min(midi_vals)
        if pitch_range <= 3:
            return False

        durations = {n.duration_beats for n in notes}
        if len(durations) < 2 and len(notes) <= 4:
            return False

        return True
