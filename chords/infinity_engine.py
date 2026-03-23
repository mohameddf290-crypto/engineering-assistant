"""
Infinity Engine for the Chords package.
Generates infinite variations of chord progressions.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from chords.chord_creator import (
    CHORD_INTERVALS, NOTES, SCALES, ChordProgression, ChordVoicing,
)


@dataclass
class GenerationRequest:
    source_progression: Optional[ChordProgression] = None
    variation_mode: str = "similar"
    similarity_score: float = 0.7
    taste_profile: Dict[str, Any] = field(default_factory=dict)
    max_attempts: int = 10


class InfinityEngine:
    """Generates infinite variations of chord progressions."""

    def generate_similar(
        self, source_progression: ChordProgression, taste_profile: Optional[Dict] = None
    ) -> ChordProgression:
        taste_profile = taste_profile or {}
        new_voicings = []
        for v in source_progression.voicings:
            new_v = self._vary_voicing(v)
            new_v.duration_beats = v.duration_beats
            new_v.position_bar = v.position_bar
            new_voicings.append(new_v)
        return ChordProgression(
            voicings=new_voicings,
            key=source_progression.key,
            scale=source_progression.scale,
            length_bars=source_progression.length_bars,
            emotional_character=source_progression.emotional_character,
            creation_plan_ref=source_progression.creation_plan_ref,
        )

    def generate_different(
        self, source_progression: ChordProgression, taste_profile: Optional[Dict] = None
    ) -> ChordProgression:
        taste_profile = taste_profile or {}
        key = source_progression.key
        scale = source_progression.scale

        contrast_choice = random.choice(["relative", "parallel", "tritone"])
        note_idx = NOTES.index(key)

        if contrast_choice == "relative":
            if scale in ("major",):
                new_scale = "minor"
                new_key = NOTES[(note_idx + 9) % 12]
            else:
                new_scale = "major"
                new_key = NOTES[(note_idx + 3) % 12]
        elif contrast_choice == "parallel":
            new_key = key
            new_scale = "minor" if scale == "major" else "major"
        else:
            new_key = NOTES[(note_idx + 6) % 12]
            new_scale = scale

        new_voicings = []
        new_root_pc = NOTES.index(new_key)
        scale_intervals = SCALES.get(new_scale, SCALES["major"])
        scale_pcs = [(new_root_pc + i) % 12 for i in scale_intervals]

        for i, v in enumerate(source_progression.voicings):
            pc = scale_pcs[i % len(scale_pcs)]
            new_root_midi = 60 + pc
            quality = random.choice(["maj", "min", "m7", "maj7", "dom7"])
            new_v = self._build_voicing(new_root_midi, quality)
            new_v.duration_beats = v.duration_beats
            new_v.position_bar = v.position_bar
            new_voicings.append(new_v)

        return ChordProgression(
            voicings=new_voicings,
            key=new_key,
            scale=new_scale,
            length_bars=source_progression.length_bars,
            emotional_character=source_progression.emotional_character,
        )

    def generate_variation(
        self,
        source_progression: ChordProgression,
        similarity_score: float,
        taste_profile: Optional[Dict] = None,
    ) -> ChordProgression:
        if similarity_score >= 0.8:
            return self.generate_similar(source_progression, taste_profile)
        elif similarity_score <= 0.2:
            return self.generate_different(source_progression, taste_profile)
        similar = self.generate_similar(source_progression, taste_profile)
        different = self.generate_different(source_progression, taste_profile)
        n = len(source_progression.voicings)
        n_similar = int(round(n * similarity_score))
        mixed_voicings = similar.voicings[:n_similar] + different.voicings[n_similar:]
        return ChordProgression(
            voicings=mixed_voicings,
            key=source_progression.key if similarity_score > 0.5 else different.key,
            scale=source_progression.scale if similarity_score > 0.5 else different.scale,
            length_bars=source_progression.length_bars,
            emotional_character=source_progression.emotional_character,
        )

    def apply_quality_gate(self, progression: ChordProgression) -> bool:
        if not progression.voicings:
            return False
        durations = [v.duration_beats for v in progression.voicings]
        unique_durations = len(set(durations))
        if len(durations) >= 4 and unique_durations == 1:
            return False
        qualities = [v.quality for v in progression.voicings]
        unique_qualities = len(set(qualities))
        if len(qualities) >= 4 and unique_qualities == 1:
            return False
        return True

    def build_variation_space(self, source_progression: ChordProgression) -> Dict:
        return {
            "key": source_progression.key,
            "scale": source_progression.scale,
            "qualities": list({v.quality for v in source_progression.voicings}),
            "rhythms": list({v.duration_beats for v in source_progression.voicings}),
            "length": source_progression.length_bars,
            "contrast_keys": [
                NOTES[(NOTES.index(source_progression.key) + 3) % 12],
                NOTES[(NOTES.index(source_progression.key) + 6) % 12],
                NOTES[(NOTES.index(source_progression.key) + 9) % 12],
            ],
        }

    def _vary_voicing(self, voicing: ChordVoicing) -> ChordVoicing:
        if len(voicing.midi_notes) > 2:
            new_notes = list(voicing.midi_notes)
            upper = [n for n in new_notes if n >= 60]
            if upper:
                lowest_upper_idx = new_notes.index(min(upper))
                candidate = new_notes[lowest_upper_idx] + 12
                if candidate <= 83:
                    new_notes[lowest_upper_idx] = candidate
            return ChordVoicing(
                root=voicing.root,
                quality=voicing.quality,
                extensions=voicing.extensions,
                bass_note=voicing.bass_note,
                midi_notes=sorted(new_notes),
                duration_beats=voicing.duration_beats,
                position_bar=voicing.position_bar,
            )
        return voicing

    def _vary_rhythm(self, voicing: ChordVoicing) -> ChordVoicing:
        choices = [voicing.duration_beats * 0.5, voicing.duration_beats, voicing.duration_beats * 2.0]
        new_dur = random.choice(choices)
        new_dur = max(0.5, min(8.0, new_dur))
        return ChordVoicing(
            root=voicing.root,
            quality=voicing.quality,
            extensions=voicing.extensions,
            bass_note=voicing.bass_note,
            midi_notes=list(voicing.midi_notes),
            duration_beats=new_dur,
            position_bar=voicing.position_bar,
        )

    def _add_extension(self, voicing: ChordVoicing) -> ChordVoicing:
        ext_map = {"maj": "maj7", "min": "m7", "maj7": "maj9", "m7": "m9", "dom7": "dom9"}
        new_quality = ext_map.get(voicing.quality, voicing.quality)
        intervals = CHORD_INTERVALS.get(new_quality, CHORD_INTERVALS.get(voicing.quality, [0, 4, 7]))
        root = voicing.root
        upper_notes = [root + iv for iv in intervals]
        upper_notes = [max(60, min(83, n)) for n in upper_notes]
        return ChordVoicing(
            root=root,
            quality=new_quality,
            extensions=voicing.extensions,
            bass_note=voicing.bass_note,
            midi_notes=[voicing.bass_note] + upper_notes,
            duration_beats=voicing.duration_beats,
            position_bar=voicing.position_bar,
        )

    def _build_voicing(self, root_midi: int, quality: str) -> ChordVoicing:
        while root_midi < 60:
            root_midi += 12
        while root_midi > 71:
            root_midi -= 12
        bass = max(36, min(47, root_midi - 24))
        intervals = CHORD_INTERVALS.get(quality, [0, 4, 7])
        upper_notes = [max(60, min(83, root_midi + iv)) for iv in intervals]
        return ChordVoicing(
            root=root_midi,
            quality=quality,
            extensions=[],
            bass_note=bass,
            midi_notes=[bass] + upper_notes,
            duration_beats=2.0,
            position_bar=1,
        )
