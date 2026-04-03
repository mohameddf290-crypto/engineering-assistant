"""Translation System — Melodies package."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union
from collections import Counter

from melodies.chord_analysis import ChordAnalysisResult, NoteAvailabilityMap
from melodies.song_analysis import MelodicDNA

_NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
_ROLE_RANGES: Dict[str, Tuple[int, int]] = {
    "lead": (60, 84), "counter": (55, 79), "ear_candy": (76, 100),
    "pad": (48, 72), "bass": (36, 60),
}
_COMPLEXITY_STEP_LEAP = {"simple": 0.8, "medium": 0.7, "complex": 0.55}
_COMPLEXITY_LEVEL = {"simple": 3, "medium": 5, "complex": 8}


@dataclass
class MelodyCreationPlan:
    key: str = "C"
    scale: str = "major"
    length_bars: int = 8
    role: str = "lead"
    complexity: str = "medium"
    mode: str = "normal"
    note_pool_per_beat: Dict[float, List[int]] = field(default_factory=dict)
    rhythmic_framework: List[float] = field(default_factory=list)
    contour_shape: str = "arch"
    phrase_boundaries: List[int] = field(default_factory=list)
    step_leap_ratio: float = 0.7
    target_range: Tuple[int, int] = (60, 84)
    input_type: str = "chords"
    note_pool_strategy: str = "chord_tones_priority"
    contour_target: str = ""
    rhythmic_framework_meta: Dict[str, float] = field(default_factory=dict)
    phrasing_plan: Dict[str, object] = field(default_factory=dict)
    complexity_level: int = 5
    hybrid_mode: bool = False


class MelodyTranslationSystem:
    def __init__(self) -> None:
        pass

    def translate(self, note_map: NoteAvailabilityMap, complexity: str, role: str, length_bars: int) -> MelodyCreationPlan:
        note_pool_per_beat: Dict[float, List[int]] = {}
        for beat, pool in note_map.items():
            consonant = pool.get("consonant", [])
            tension = pool.get("tension", [])
            combined = list(dict.fromkeys(consonant + tension))
            note_pool_per_beat[beat] = combined
        all_consonant = [n for p in note_map.values() for n in p.get("consonant", [])]
        key = self._infer_key(all_consonant)
        scale = self._infer_scale(all_consonant, key)
        rhythmic_fw = self._build_rhythmic_list(complexity, length_bars)
        phrase_bounds = self._default_phrase_boundaries(length_bars)
        target_range = _ROLE_RANGES.get(role, (60, 84))
        return MelodyCreationPlan(
            key=key, scale=scale, length_bars=length_bars,
            role=role, complexity=complexity, mode="normal",
            note_pool_per_beat=note_pool_per_beat,
            rhythmic_framework=rhythmic_fw, contour_shape="arch",
            phrase_boundaries=phrase_bounds,
            step_leap_ratio=_COMPLEXITY_STEP_LEAP.get(complexity, 0.7),
            target_range=target_range, input_type="chords",
            complexity_level=_COMPLEXITY_LEVEL.get(complexity, 5),
        )

    def translate_with_inspiration(self, note_map: NoteAvailabilityMap, dna_blueprint: MelodicDNA, complexity: str, role: str, length_bars: int) -> MelodyCreationPlan:
        plan = self.translate(note_map, complexity, role, length_bars)
        plan.contour_shape = dna_blueprint.contour_shape
        plan.step_leap_ratio = self._dna_step_leap(dna_blueprint)
        plan.rhythmic_framework_meta = {"onset_density": dna_blueprint.rhythmic_density, "syncopation": dna_blueprint.syncopation_level}
        plan.hybrid_mode = True
        plan.input_type = "hybrid"
        return plan

    def translate_from_chords(self, chord_analysis: ChordAnalysisResult) -> MelodyCreationPlan:
        prog = chord_analysis.progression
        note_pool_per_beat: Dict[float, List[int]] = {}
        abs_beat = 0.0
        for chord_idx, voicing in enumerate(prog.voicings):
            pool = chord_analysis.note_pools_per_chord.get(chord_idx, [])
            for step in range(int(voicing.duration_beats / 0.5)):
                note_pool_per_beat[round(abs_beat + step * 0.5, 4)] = pool
            abs_beat += voicing.duration_beats
        avg_tension = sum(chord_analysis.tension_arc) / max(len(chord_analysis.tension_arc), 1)
        contour = "arch" if avg_tension < 0.5 else "wave"
        return MelodyCreationPlan(
            key=prog.key, scale=prog.scale, length_bars=prog.length_bars,
            role="lead", complexity="medium", mode="normal",
            note_pool_per_beat=note_pool_per_beat,
            rhythmic_framework=self._build_rhythmic_list("medium", prog.length_bars),
            contour_shape=contour,
            phrase_boundaries=self._default_phrase_boundaries(prog.length_bars),
            step_leap_ratio=0.7, target_range=_ROLE_RANGES["lead"],
            input_type="chords", complexity_level=5,
            note_pool_strategy=self.build_note_pool_strategy(chord_analysis),
        )

    def translate_from_song(self, melodic_dna: MelodicDNA) -> MelodyCreationPlan:
        length_bars = 8
        return MelodyCreationPlan(
            key="C", scale="major", length_bars=length_bars, role="lead",
            complexity=self._density_to_complexity(melodic_dna.rhythmic_density),
            mode="normal", note_pool_per_beat={},
            rhythmic_framework=self._build_rhythmic_list("medium", length_bars),
            contour_shape=melodic_dna.contour_shape,
            phrase_boundaries=self._default_phrase_boundaries(length_bars),
            step_leap_ratio=self._dna_step_leap(melodic_dna),
            target_range=_ROLE_RANGES["lead"], input_type="song", complexity_level=5,
        )

    def translate_from_both(self, chord_analysis: ChordAnalysisResult, melodic_dna: MelodicDNA) -> MelodyCreationPlan:
        plan = self.translate_from_chords(chord_analysis)
        plan.contour_shape = melodic_dna.contour_shape
        plan.step_leap_ratio = self._dna_step_leap(melodic_dna)
        plan.hybrid_mode = True
        plan.input_type = "hybrid"
        return plan

    def build_note_pool_strategy(self, chord_analysis: ChordAnalysisResult) -> str:
        avg_t = sum(chord_analysis.tension_arc) / max(len(chord_analysis.tension_arc), 1)
        if avg_t > 0.6:
            return "favour chord tones on beats 1,3; use extensions on 2,4; approach notes at phrase endings"
        return "chord tones priority on strong beats; extensions on weak beats"

    def design_contour_target(self, input_data: object) -> str:
        if isinstance(input_data, MelodicDNA):
            return input_data.contour_shape
        if isinstance(input_data, ChordAnalysisResult):
            arc = input_data.tension_arc
            if not arc:
                return "arch"
            mid = len(arc) // 2
            first = sum(arc[:mid]) / max(mid, 1)
            second = sum(arc[mid:]) / max(len(arc) - mid, 1)
            if first < second:
                return "ascending"
            if first > second * 1.2:
                return "descending"
            return "arch"
        return "arch"

    def design_rhythmic_framework(self, input_data: object) -> Dict[str, float]:
        if isinstance(input_data, MelodicDNA):
            return {"onset_density_target": input_data.rhythmic_density, "syncopation_target": input_data.syncopation_level, "grid_alignment": 1.0 - input_data.syncopation_level}
        return {"onset_density_target": 2.0, "syncopation_target": 0.3, "grid_alignment": 0.7}

    def _infer_key(self, notes: List[int]) -> str:
        if not notes:
            return "C"
        counts = Counter(n % 12 for n in notes)
        return _NOTES[counts.most_common(1)[0][0]]

    def _infer_scale(self, notes: List[int], key: str) -> str:
        if not notes:
            return "major"
        pcs = set(n % 12 for n in notes)
        root = _NOTES.index(key)
        return "minor" if {(root + 3) % 12} & pcs else "major"

    def _build_rhythmic_list(self, complexity: str, length_bars: int) -> List[float]:
        beats_total = length_bars * 4
        if complexity == "simple":
            units = [2.0, 1.0, 2.0, 1.0]
        elif complexity == "complex":
            units = [0.5, 0.25, 0.5, 0.25, 0.5, 0.25]
        else:
            units = [1.0, 0.5, 1.0, 0.5]
        result: List[float] = []
        total = 0.0
        i = 0
        while total < beats_total:
            d = units[i % len(units)]
            if total + d > beats_total:
                d = beats_total - total
            result.append(d)
            total += d
            i += 1
        return result

    def _default_phrase_boundaries(self, length_bars: int) -> List[int]:
        bounds = list(range(4, length_bars + 1, 4))
        if not bounds or bounds[-1] != length_bars:
            bounds.append(length_bars)
        return bounds

    def _dna_step_leap(self, dna: MelodicDNA) -> float:
        prefs = dna.interval_preferences
        if not prefs:
            return 0.7
        step_weight = prefs.get(1, 0) + prefs.get(2, 0)
        total = sum(prefs.values()) or 1.0
        return round(min(0.9, max(0.4, step_weight / total + 0.3)), 2)

    def _density_to_complexity(self, density: float) -> str:
        if density < 1.5:
            return "simple"
        if density < 4.0:
            return "medium"
        return "complex"
