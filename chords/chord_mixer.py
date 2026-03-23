"""
Chord Mixer for the Chords package.
Blends and merges chord progressions.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from chords.chord_creator import CHORD_INTERVALS, NOTES, SCALES, ChordProgression, ChordVoicing


@dataclass
class MixRequest:
    progression_a: Optional[ChordProgression] = None
    progression_b: Optional[ChordProgression] = None
    blend_ratio: float = 0.5
    strategy: str = "interleave"
    output_length_bars: Optional[int] = None


@dataclass
class MixResult:
    blended_progression: Optional[ChordProgression] = None
    compatibility_score: float = 0.0
    strategy_used: str = ""
    notes: List[str] = field(default_factory=list)


class ChordMixer:
    """Blends and merges chord progressions using various strategies."""

    def mix_progressions(
        self,
        progression_a: ChordProgression,
        progression_b: ChordProgression,
        blend_ratio: float = 0.5,
    ) -> ChordProgression:
        a_adj, b_adj = self.resolve_key_conflict(progression_a, progression_b)
        n_a = len(a_adj.voicings)
        n_b = len(b_adj.voicings)
        total = n_a + n_b
        n_from_a = max(1, round(total * (1 - blend_ratio)))
        n_from_b = total - n_from_a
        a_voicings = list(a_adj.voicings)[:n_from_a]
        b_voicings = list(b_adj.voicings)[:n_from_b]
        mixed = a_voicings + b_voicings
        length = max(a_adj.length_bars, b_adj.length_bars)
        return ChordProgression(
            voicings=mixed,
            key=a_adj.key,
            scale=a_adj.scale,
            length_bars=length,
            emotional_character=f"{a_adj.emotional_character}+{b_adj.emotional_character}",
        )

    def mix(
        self,
        progression_a: ChordProgression,
        progression_b: ChordProgression,
        strategy: str = "interleave",
    ) -> ChordProgression:
        if strategy == "interleave":
            return self._interleave(progression_a, progression_b)
        elif strategy == "structural_blend":
            return self._structural_blend(progression_a, progression_b)
        elif strategy == "harmonic_merge":
            return self._harmonic_merge(progression_a, progression_b)
        else:
            return self._interleave(progression_a, progression_b)

    def _interleave(self, a: ChordProgression, b: ChordProgression) -> ChordProgression:
        result_voicings = []
        a_v = list(a.voicings)
        b_v = list(b.voicings)
        max_len = max(len(a_v), len(b_v))
        for i in range(max_len):
            if i < len(a_v):
                result_voicings.append(copy.deepcopy(a_v[i]))
            if i < len(b_v):
                v = copy.deepcopy(b_v[i])
                v.position_bar = (a_v[i].position_bar if i < len(a_v) else i + 1) + 1
                result_voicings.append(v)
        return ChordProgression(
            voicings=result_voicings,
            key=a.key,
            scale=a.scale,
            length_bars=a.length_bars + b.length_bars,
            emotional_character=f"{a.emotional_character}+{b.emotional_character}",
        )

    def _structural_blend(self, a: ChordProgression, b: ChordProgression) -> ChordProgression:
        result_voicings = []
        b_v = list(b.voicings)
        for i, av in enumerate(a.voicings):
            bv = b_v[i % len(b_v)] if b_v else av
            new_v = ChordVoicing(
                root=bv.root,
                quality=bv.quality,
                extensions=bv.extensions,
                bass_note=bv.bass_note,
                midi_notes=list(bv.midi_notes),
                duration_beats=av.duration_beats,
                position_bar=av.position_bar,
            )
            result_voicings.append(new_v)
        return ChordProgression(
            voicings=result_voicings,
            key=b.key,
            scale=b.scale,
            length_bars=a.length_bars,
            emotional_character=f"{a.emotional_character}+{b.emotional_character}",
        )

    def _harmonic_merge(self, a: ChordProgression, b: ChordProgression) -> ChordProgression:
        pivots = self.detect_pivot_chords(a, b)
        a_v = list(a.voicings)
        b_v = list(b.voicings)
        result = []
        for i in range(min(len(a_v), len(b_v))):
            av = a_v[i]
            bv = b_v[i]
            av_complexity = len(CHORD_INTERVALS.get(av.quality, []))
            bv_complexity = len(CHORD_INTERVALS.get(bv.quality, []))
            chosen = av if av_complexity >= bv_complexity else bv
            result.append(copy.deepcopy(chosen))
        return ChordProgression(
            voicings=result,
            key=a.key,
            scale=a.scale,
            length_bars=min(a.length_bars, b.length_bars),
            emotional_character=f"{a.emotional_character}+{b.emotional_character}",
        )

    def analyse_compatibility(
        self, progression_a: ChordProgression, progression_b: ChordProgression
    ) -> Dict:
        same_key = progression_a.key == progression_b.key
        same_scale = progression_a.scale == progression_b.scale
        key_distance = abs(
            NOTES.index(progression_a.key) - NOTES.index(progression_b.key)
        )
        relative = key_distance in (3, 9)
        score = 1.0
        if not same_key:
            score -= 0.2
        if not same_scale:
            score -= 0.1
        if key_distance > 6:
            score -= 0.2
        return {
            "same_key": same_key,
            "same_scale": same_scale,
            "relative_keys": relative,
            "key_distance_semitones": key_distance,
            "compatibility_score": max(0.0, score),
        }

    def detect_pivot_chords(
        self, progression_a: ChordProgression, progression_b: ChordProgression
    ) -> List[str]:
        a_roots = {v.root % 12 for v in progression_a.voicings}
        b_roots = {v.root % 12 for v in progression_b.voicings}
        common_pcs = a_roots & b_roots
        return [NOTES[pc] for pc in sorted(common_pcs)]

    def resolve_key_conflict(
        self, progression_a: ChordProgression, progression_b: ChordProgression
    ) -> Tuple[ChordProgression, ChordProgression]:
        if progression_a.key == progression_b.key:
            return progression_a, progression_b
        key_a_idx = NOTES.index(progression_a.key)
        key_b_idx = NOTES.index(progression_b.key)
        semitone_shift = key_a_idx - key_b_idx
        new_voicings = []
        for v in progression_b.voicings:
            new_root = v.root + semitone_shift
            while new_root < 60:
                new_root += 12
            while new_root > 71:
                new_root -= 12
            new_bass = max(36, min(47, new_root - 24))
            new_midi = [n + semitone_shift for n in v.midi_notes]
            new_midi = [max(36, min(83, n)) for n in new_midi]
            new_voicings.append(ChordVoicing(
                root=new_root,
                quality=v.quality,
                extensions=v.extensions,
                bass_note=new_bass,
                midi_notes=new_midi,
                duration_beats=v.duration_beats,
                position_bar=v.position_bar,
            ))
        adjusted_b = ChordProgression(
            voicings=new_voicings,
            key=progression_a.key,
            scale=progression_b.scale,
            length_bars=progression_b.length_bars,
            emotional_character=progression_b.emotional_character,
        )
        return progression_a, adjusted_b

    def evaluate_blend_quality(self, blended_progression: ChordProgression) -> float:
        if not blended_progression.voicings:
            return 0.0
        qualities = [v.quality for v in blended_progression.voicings]
        unique_q = len(set(qualities))
        durations = [v.duration_beats for v in blended_progression.voicings]
        unique_d = len(set(durations))
        q_score = min(1.0, unique_q / max(1, len(qualities)))
        d_score = min(1.0, unique_d / max(1, len(durations) * 0.5))
        return (q_score + d_score) / 2.0
