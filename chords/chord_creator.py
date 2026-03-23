"""
Chord Creation Brain for the Chords package.
Generates chord progressions from creation plans.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from chords.translation import ChordCreationPlan

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

SCALES = {
    "major":         [0, 2, 4, 5, 7, 9, 11],
    "minor":         [0, 2, 3, 5, 7, 8, 10],
    "dorian":        [0, 2, 3, 5, 7, 9, 10],
    "mixolydian":    [0, 2, 4, 5, 7, 9, 10],
    "phrygian":      [0, 1, 3, 5, 7, 8, 10],
    "lydian":        [0, 2, 4, 6, 7, 9, 11],
    "harmonic_minor":[0, 2, 3, 5, 7, 8, 11],
    "melodic_minor": [0, 2, 3, 5, 7, 9, 11],
}

CHORD_INTERVALS = {
    "maj":    [0, 4, 7],
    "min":    [0, 3, 7],
    "dim":    [0, 3, 6],
    "aug":    [0, 4, 8],
    "maj7":   [0, 4, 7, 11],
    "m7":     [0, 3, 7, 10],
    "dom7":   [0, 4, 7, 10],
    "m7b5":   [0, 3, 6, 10],
    "dim7":   [0, 3, 6, 9],
    "maj9":   [0, 4, 7, 11, 14],
    "m9":     [0, 3, 7, 10, 14],
    "dom9":   [0, 4, 7, 10, 14],
    "sus2":   [0, 2, 7],
    "sus4":   [0, 5, 7],
    "add9":   [0, 4, 7, 14],
    "madd9":  [0, 3, 7, 14],
    "6":      [0, 4, 7, 9],
    "m6":     [0, 3, 7, 9],
    "maj11":  [0, 4, 7, 11, 14, 17],
    "m11":    [0, 3, 7, 10, 14, 17],
    "13":     [0, 4, 7, 10, 14, 17, 21],
}

_DEGREE_QUALITIES = {
    "major":         {1:"maj", 2:"min", 3:"min", 4:"maj", 5:"maj", 6:"min", 7:"dim"},
    "minor":         {1:"min", 2:"dim", 3:"maj", 4:"min", 5:"min", 6:"maj", 7:"maj"},
    "dorian":        {1:"min", 2:"min", 3:"maj", 4:"maj", 5:"min", 6:"dim", 7:"maj"},
    "mixolydian":    {1:"maj", 2:"min", 3:"dim", 4:"maj", 5:"min", 6:"min", 7:"maj"},
    "phrygian":      {1:"min", 2:"maj", 3:"maj", 4:"min", 5:"dim", 6:"maj", 7:"min"},
    "lydian":        {1:"maj", 2:"maj", 3:"min", 4:"dim", 5:"maj", 6:"min", 7:"min"},
    "harmonic_minor":{1:"min", 2:"dim", 3:"aug", 4:"min", 5:"maj", 6:"maj", 7:"dim7"},
    "melodic_minor": {1:"min", 2:"min", 3:"aug", 4:"maj", 5:"maj", 6:"dim", 7:"dim"},
}

# Chord quality triadic type for palette compatibility
_QUALITY_TRIADIC_TYPE = {
    "maj": "maj", "maj7": "maj", "maj9": "maj", "add9": "maj", "6": "maj",
    "maj11": "maj", "dom7": "maj", "dom9": "maj", "13": "maj", "aug": "maj",
    "sus2": "any", "sus4": "any",  # sus chords are compatible with any context
    "min": "min", "m7": "min", "m9": "min", "madd9": "min", "m6": "min",
    "m11": "min", "m7b5": "min", "dim": "min", "dim7": "min",
}


def _clamp_to_range(note: int, lo: int, hi: int) -> int:
    """Clamp a MIDI note number into [lo, hi] by shifting octaves, then hard-clamping."""
    span = hi - lo + 1
    while note < lo:
        note += 12
    while note > hi:
        note -= 12
    return max(lo, min(hi, note))


@dataclass
class ChordVoicing:
    root: int = 60
    quality: str = "maj"
    extensions: List[str] = field(default_factory=list)
    bass_note: int = 36
    midi_notes: List[int] = field(default_factory=list)
    duration_beats: float = 2.0
    position_bar: int = 1


@dataclass
class ChordProgression:
    voicings: List[ChordVoicing] = field(default_factory=list)
    key: str = "C"
    scale: str = "major"
    length_bars: int = 8
    emotional_character: str = "neutral"
    creation_plan_ref: Optional[str] = None


class ChordCreationBrain:
    """Generates chord progressions from creation plans using music theory."""

    def create_from_plan(self, plan: ChordCreationPlan, taste_profile: Optional[Dict] = None) -> ChordProgression:
        taste_profile = taste_profile or {}
        root_pc = NOTES.index(plan.key)
        scale_intervals = SCALES.get(plan.scale, SCALES["major"])
        scale_pcs = [(root_pc + i) % 12 for i in scale_intervals]

        if plan.harmonic_rhythm_blueprint:
            num_chords = len(plan.harmonic_rhythm_blueprint)
        else:
            num_chords = plan.length_bars * 2

        degrees = list(range(1, len(scale_pcs) + 1))
        weights = [plan.scale_degree_weights.get(d, 1.0 / len(degrees)) for d in degrees]
        total = sum(weights)
        weights = [w / total for w in weights]

        voicings = []
        prev_notes: List[int] = []

        for i in range(num_chords):
            r = random.random()
            cumsum = 0.0
            degree_idx = len(degrees) - 1
            for j, w in enumerate(weights):
                cumsum += w
                if r <= cumsum:
                    degree_idx = j
                    break

            degree = degrees[degree_idx]
            root_pc_chord = scale_pcs[degree - 1]
            root_midi = 60 + root_pc_chord

            quality = self._select_quality_for_degree(degree, plan.scale, plan.chord_quality_palette)

            extensions: List[str] = []
            if plan.preferred_extensions and i % 3 == 0:
                extensions = [plan.preferred_extensions[0]]

            duration = plan.harmonic_rhythm_blueprint[i] if i < len(plan.harmonic_rhythm_blueprint) else 2.0
            bar = i // 2 + 1

            voicing = self.voice_chord(root_midi, quality, extensions, {"prev_notes": prev_notes})
            voicing.duration_beats = duration
            voicing.position_bar = bar

            prev_notes = voicing.midi_notes
            voicings.append(voicing)

        progression = ChordProgression(
            voicings=voicings,
            key=plan.key,
            scale=plan.scale,
            length_bars=plan.length_bars,
            emotional_character=", ".join(plan.target_emotions) if plan.target_emotions else "neutral",
        )
        if taste_profile:
            progression = self.apply_taste_profile(progression, taste_profile)
        return progression

    def voice_chord(self, root: int, quality: str, extensions: Optional[List[str]] = None,
                    context: Optional[Dict] = None) -> ChordVoicing:
        extensions = extensions or []
        context = context or {}

        while root < 60:
            root += 12
        while root > 71:
            root -= 12

        bass = root - 24
        bass = max(36, min(47, bass))

        intervals = list(CHORD_INTERVALS.get(quality, CHORD_INTERVALS["maj"]))

        ext_intervals: List[int] = []
        for ext in extensions:
            if ext in CHORD_INTERVALS:
                for iv in CHORD_INTERVALS[ext]:
                    if iv not in intervals and iv not in ext_intervals:
                        ext_intervals.append(iv)

        all_intervals = sorted(set(intervals + ext_intervals))

        upper_notes = [_clamp_to_range(root + iv, 60, 83) for iv in all_intervals]

        prev_notes = context.get("prev_notes", [])
        if prev_notes:
            upper_notes = self._apply_voice_leading(upper_notes, prev_notes)

        midi_notes = [bass] + upper_notes

        return ChordVoicing(
            root=root,
            quality=quality,
            extensions=extensions,
            bass_note=bass,
            midi_notes=midi_notes,
            duration_beats=2.0,
            position_bar=1,
        )

    def _apply_voice_leading(self, current_notes: List[int], prev_notes: List[int]) -> List[int]:
        if not prev_notes or len(current_notes) < 2:
            return current_notes
        prev_upper = [n for n in prev_notes if n >= 60]
        if not prev_upper:
            return current_notes

        best = list(current_notes)
        best_cost = sum(
            abs(a - b)
            for a, b in zip(sorted(current_notes), sorted(prev_upper)[: len(current_notes)])
        )

        for i in range(len(current_notes)):
            candidate = list(current_notes)
            candidate[i] -= 12
            if all(60 <= n <= 83 for n in candidate):
                cost = sum(
                    abs(a - b)
                    for a, b in zip(sorted(candidate), sorted(prev_upper)[: len(candidate)])
                )
                if cost < best_cost:
                    best_cost = cost
                    best = candidate
        return sorted(best)

    def _select_quality_for_degree(self, degree: int, scale: str, palette: List[str]) -> str:
        default_map = _DEGREE_QUALITIES.get(scale, _DEGREE_QUALITIES["major"])
        default_quality = default_map.get(degree, "maj")
        if not palette:
            return default_quality
        triadic_type = "min" if default_quality in ("min", "dim", "m7", "m7b5", "dim7") else "maj"
        compatible = []
        for q in palette:
            q_type = _QUALITY_TRIADIC_TYPE.get(q)
            if q_type == "any" or q_type == triadic_type:
                compatible.append(q)
        if compatible:
            return random.choice(compatible)
        if default_quality in palette:
            return default_quality
        return palette[0] if palette else default_quality

    def apply_taste_profile(self, progression: ChordProgression, taste_profile: Dict) -> ChordProgression:
        if not taste_profile:
            return progression
        complexity = taste_profile.get("complexity", 0.5)
        if complexity > 0.7:
            for v in progression.voicings:
                if not v.extensions and v.quality in ("maj", "min"):
                    v.extensions = ["maj7"] if v.quality == "maj" else ["m7"]
                    new_v = self.voice_chord(v.root, v.quality, v.extensions, {})
                    v.midi_notes = new_v.midi_notes
        density = taste_profile.get("density", 0.5)
        if density < 0.3:
            for v in progression.voicings:
                if len(v.midi_notes) > 4:
                    v.midi_notes = v.midi_notes[:4]
        return progression

    def generate_extensions(self, chord: ChordVoicing, harmonic_context: Optional[Dict] = None) -> List[str]:
        harmonic_context = harmonic_context or {}
        tension = harmonic_context.get("tension_level", 5)
        if tension >= 8:
            return ["dom9", "13"]
        elif tension >= 6:
            return ["maj7", "9"]
        elif tension >= 4:
            return ["maj7"]
        return []

    def validate_progression_coherence(self, progression: ChordProgression) -> bool:
        if not progression.voicings:
            return False
        for v in progression.voicings:
            if not v.midi_notes:
                return False
            if v.quality not in CHORD_INTERVALS:
                return False
        return True
