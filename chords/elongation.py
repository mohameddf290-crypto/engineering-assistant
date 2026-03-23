"""
Elongation System for the Chords package.
Extends and develops chord progressions.
"""
from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from chords.chord_creator import (
    CHORD_INTERVALS, NOTES, SCALES, ChordProgression, ChordVoicing,
)


@dataclass
class ElongationRequest:
    source_progression: Optional[ChordProgression] = None
    additional_bars: int = 4
    style: str = "develop"
    taste_profile: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ElongationResult:
    original_progression: Optional[ChordProgression] = None
    extended_progression: Optional[ChordProgression] = None
    added_bars: int = 0
    continuity_score: float = 0.0
    style_used: str = ""


class ElongationSystem:
    """Extends chord progressions using various compositional strategies."""

    def elongate(
        self,
        source_progression: ChordProgression,
        additional_bars: int,
        style: str = "develop",
    ) -> ChordProgression:
        arc = self.analyse_harmonic_arc(source_progression)
        extension = self.generate_continuation(source_progression, arc, additional_bars)
        combined_voicings = list(source_progression.voicings) + list(extension.voicings)
        for v in combined_voicings[len(source_progression.voicings):]:
            v.position_bar += source_progression.length_bars
        return ChordProgression(
            voicings=combined_voicings,
            key=source_progression.key,
            scale=source_progression.scale,
            length_bars=source_progression.length_bars + additional_bars,
            emotional_character=source_progression.emotional_character,
            creation_plan_ref=source_progression.creation_plan_ref,
        )

    def analyse_harmonic_arc(self, progression: ChordProgression) -> Dict:
        if not progression.voicings:
            return {"tension_trajectory": [], "cadence_points": [], "rhythm_pattern": [], "quality_vocab": []}
        _complexity = {q: len(ivs) for q, ivs in CHORD_INTERVALS.items()}
        tension_traj = [_complexity.get(v.quality, 3) for v in progression.voicings]
        cadence_points = [len(progression.voicings) - 1]
        rhythm_pattern = [v.duration_beats for v in progression.voicings]
        quality_vocab = list({v.quality for v in progression.voicings})
        key_pc = NOTES.index(progression.key) if progression.key in NOTES else 0
        intervals = SCALES.get(progression.scale, SCALES["major"])
        scale_pcs = [(key_pc + i) % 12 for i in intervals]
        degree_seq = []
        for v in progression.voicings:
            root_pc = v.root % 12
            try:
                deg = scale_pcs.index(root_pc) + 1
            except ValueError:
                deg = 1
            degree_seq.append(deg)
        return {
            "tension_trajectory": tension_traj,
            "cadence_points": cadence_points,
            "rhythm_pattern": rhythm_pattern,
            "quality_vocab": quality_vocab,
            "degree_sequence": degree_seq,
        }

    def generate_continuation(
        self,
        progression: ChordProgression,
        arc_analysis: Dict,
        additional_bars: int,
    ) -> ChordProgression:
        degree_seq = arc_analysis.get("degree_sequence", [1, 4, 5, 1])
        quality_vocab = arc_analysis.get("quality_vocab", ["maj", "min"])
        rhythm_pattern = arc_analysis.get("rhythm_pattern", [2.0])
        key_pc = NOTES.index(progression.key) if progression.key in NOTES else 0
        intervals = SCALES.get(progression.scale, SCALES["major"])
        scale_pcs = [(key_pc + i) % 12 for i in intervals]
        avg_dur = sum(rhythm_pattern) / max(1, len(rhythm_pattern))
        n_new = max(2, int(additional_bars * 4 / max(1, avg_dur)))
        new_voicings = []
        for i in range(n_new):
            deg = degree_seq[i % len(degree_seq)]
            pc = scale_pcs[(deg - 1) % len(scale_pcs)]
            root_midi = 60 + pc
            quality = quality_vocab[i % len(quality_vocab)]
            duration = rhythm_pattern[i % len(rhythm_pattern)]
            bass = max(36, min(47, root_midi - 24))
            ivs = CHORD_INTERVALS.get(quality, [0, 4, 7])
            upper = [max(60, min(83, root_midi + iv)) for iv in ivs]
            new_voicings.append(ChordVoicing(
                root=root_midi,
                quality=quality,
                extensions=[],
                bass_note=bass,
                midi_notes=[bass] + upper,
                duration_beats=duration,
                position_bar=i // 2 + 1,
            ))
        return ChordProgression(
            voicings=new_voicings,
            key=progression.key,
            scale=progression.scale,
            length_bars=additional_bars,
            emotional_character=progression.emotional_character,
        )

    def validate_continuity(
        self, original: ChordProgression, extension: ChordProgression
    ) -> float:
        if not original.voicings or not extension.voicings:
            return 0.0
        same_key = original.key == extension.key
        same_scale = original.scale == extension.scale
        orig_quals = {v.quality for v in original.voicings}
        ext_quals = {v.quality for v in extension.voicings}
        overlap = len(orig_quals & ext_quals) / max(1, len(orig_quals | ext_quals))
        score = 0.4 * overlap
        if same_key:
            score += 0.4
        if same_scale:
            score += 0.2
        return min(1.0, score)
