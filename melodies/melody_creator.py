"""Melody Creation Brain — Melodies package."""
from __future__ import annotations
import math, random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from melodies.translation import MelodyCreationPlan

_ROLE_RANGES: Dict[str, Tuple[int, int]] = {
    "lead": (60, 84), "counter": (55, 79), "ear_candy": (76, 100), "pad": (48, 72), "bass": (36, 60),
}

@dataclass
class MelodyNote:
    pitch: int
    duration: float
    position: float
    bar: int
    velocity: int = 80
    locked: bool = False
    is_chord_tone: bool = False
    role_annotation: str = ""
    @property
    def pitch_midi(self) -> int: return self.pitch
    @property
    def duration_beats(self) -> float: return self.duration
    @property
    def position_beats(self) -> float: return (self.bar - 1) * 4.0 + self.position

@dataclass
class MelodyLine:
    notes: List[MelodyNote] = field(default_factory=list)
    key: str = "C"
    scale: str = "major"
    length_bars: int = 8
    role: str = "lead"
    complexity: str = "medium"
    mode: str = "normal"
    creation_plan_ref: Optional[str] = None
    taste_profile_ref: Optional[str] = None
    @property
    def complexity_level(self) -> int:
        return {"simple": 3, "medium": 5, "complex": 8}.get(self.complexity, 5)

Melody = MelodyLine

class MelodyCreationBrain:
    def __init__(self) -> None:
        self._construction_rules: Dict[str, object] = {}

    def create_from_plan(self, creation_plan: MelodyCreationPlan, taste_profile: Optional[Dict] = None) -> MelodyLine:
        taste_profile = taste_profile or {}
        lo, hi = creation_plan.target_range or _ROLE_RANGES.get(creation_plan.role, (60, 84))
        rhythm = self._make_rhythm(creation_plan)
        total = len(rhythm)
        prev_pitch = (lo + hi) // 2
        last_interval = 0
        notes: List[MelodyNote] = []
        climax_used = False
        for i, (bar, position, duration) in enumerate(rhythm):
            abs_beat = round((bar - 1) * 4.0 + position, 4)
            t = i / max(total - 1, 1)
            pool = self._get_pool(creation_plan.note_pool_per_beat, abs_beat, lo, hi)
            strong = position % 4.0 in (0.0, 2.0) and abs(position - round(position)) < 0.01
            if strong:
                pool = [p for p in pool if (p - lo) % 7 in (0, 2, 4) or not pool] or pool
            if 0.68 <= t <= 0.82 and not climax_used and pool:
                pitch = max(p for p in pool if p <= hi)
                climax_used = True
            else:
                direction = self._contour_direction(creation_plan.contour_shape, t)
                pitch = self._pick_note(pool, prev_pitch, direction, creation_plan.step_leap_ratio, last_interval, lo, hi)
            velocity = 90 if strong else (75 if position % 1.0 == 0.0 else 65)
            notes.append(MelodyNote(pitch=pitch, duration=duration, position=position, bar=bar, velocity=velocity))
            last_interval = pitch - prev_pitch
            prev_pitch = pitch
        notes = self._apply_phrase_structure(notes, creation_plan.phrase_boundaries, creation_plan.note_pool_per_beat, lo, hi)
        if creation_plan.mode == "hybrid":
            notes = self._add_hybrid_chord_tones(notes, creation_plan.note_pool_per_beat, lo)
        return MelodyLine(notes=notes, key=creation_plan.key, scale=creation_plan.scale, length_bars=creation_plan.length_bars, role=creation_plan.role, complexity=creation_plan.complexity, mode=creation_plan.mode)

    def build_melodic_contour(self, plan: MelodyCreationPlan) -> List[str]:
        total = max(len(plan.rhythmic_framework), 8)
        return [self._contour_direction(plan.contour_shape, i / max(total - 1, 1)) for i in range(total)]

    def select_notes_from_pool(self, contour: List[str], note_pool: List[int], harmonic_context: Dict) -> List[MelodyNote]:
        lo = min(note_pool) if note_pool else 60
        hi = max(note_pool) if note_pool else 84
        notes: List[MelodyNote] = []
        prev = (lo + hi) // 2
        last_iv = 0
        for i, direction in enumerate(contour):
            pitch = self._pick_note(note_pool, prev, direction, 0.7, last_iv, lo, hi)
            notes.append(MelodyNote(pitch=pitch, duration=1.0, position=float(i % 4), bar=i // 4 + 1))
            last_iv = pitch - prev
            prev = pitch
        return notes

    def apply_rhythmic_framework(self, notes: List[MelodyNote], rhythmic_framework: Dict[str, float]) -> List[MelodyNote]:
        density = rhythmic_framework.get("onset_density_target", 2.0)
        base_dur = max(0.25, 1.0 / max(density, 0.5))
        pos = 0.0
        result: List[MelodyNote] = []
        for note in notes:
            bar = int(pos // 4) + 1
            position = pos % 4.0
            result.append(MelodyNote(pitch=note.pitch, duration=base_dur, position=position, bar=bar, velocity=note.velocity, locked=note.locked))
            pos += base_dur
        return result

    def create_hybrid_melody(self, plan: MelodyCreationPlan, chord_progression: object, taste_profile: Dict) -> MelodyLine:
        import dataclasses
        hybrid_plan = dataclasses.replace(plan, mode="hybrid")
        return self.create_from_plan(hybrid_plan, taste_profile)

    def validate_melodic_quality(self, melody: MelodyLine) -> bool:
        if not melody.notes:
            return False
        pitches = [n.pitch for n in melody.notes]
        if max(pitches) - min(pitches) < 3:
            return False
        if len(set(n.duration for n in melody.notes)) < 2 and len(melody.notes) > 4:
            return False
        return True

    def _make_rhythm(self, plan: MelodyCreationPlan) -> List[Tuple[int, float, float]]:
        durations = list(plan.rhythmic_framework) if plan.rhythmic_framework else self._default_durations(plan.complexity, plan.length_bars)
        result: List[Tuple[int, float, float]] = []
        abs_pos = 0.0
        for dur in durations:
            bar = int(abs_pos // 4) + 1
            pos = abs_pos % 4.0
            if bar > plan.length_bars:
                break
            result.append((bar, pos, dur))
            abs_pos += dur
        return result

    def _default_durations(self, complexity: str, length_bars: int) -> List[float]:
        beats = length_bars * 4
        if complexity == "simple":
            pool = [2.0, 1.0]
        elif complexity == "complex":
            pool = [0.5, 0.25, 0.5, 0.75]
        else:
            pool = [1.0, 0.5, 1.0, 0.5]
        result: List[float] = []
        total = 0.0
        i = 0
        while total < beats:
            d = pool[i % len(pool)]
            if total + d > beats:
                d = beats - total
            result.append(d)
            total += d
            i += 1
        return result

    def _get_pool(self, pool_map: Dict[float, List[int]], beat: float, lo: int, hi: int) -> List[int]:
        if not pool_map:
            return list(range(lo, hi + 1, 1))
        if beat in pool_map:
            pool = pool_map[beat]
        else:
            keys = sorted(pool_map.keys())
            nearest = min(keys, key=lambda k: abs(k - beat))
            pool = pool_map[nearest]
        filtered = [n for n in pool if lo <= n <= hi]
        return filtered if filtered else list(range(lo, hi + 1, 2))

    def _contour_direction(self, shape: str, t: float) -> str:
        if shape == "ascending": return "up"
        if shape == "descending": return "down"
        if shape == "arch": return "up" if t < 0.6 else "down"
        if shape == "inverted_arch": return "down" if t < 0.4 else "up"
        if shape == "wave": return "up" if math.sin(t * math.pi * 4) >= 0 else "down"
        return random.choice(["up", "down"])

    def _pick_note(self, pool: List[int], prev: int, direction: str, step_ratio: float, last_iv: int, lo: int, hi: int) -> int:
        if not pool:
            return prev
        if abs(last_iv) >= 5:
            opposite = [n for n in pool if (last_iv > 0 and prev - 2 <= n <= prev - 1) or (last_iv < 0 and prev + 1 <= n <= prev + 2)]
            if opposite:
                return random.choice(opposite)
        r = random.random()
        if r < step_ratio:
            cands = [n for n in pool if 1 <= abs(n - prev) <= 2]
        elif r < step_ratio + 0.2:
            cands = [n for n in pool if 3 <= abs(n - prev) <= 4]
        else:
            cands = [n for n in pool if abs(n - prev) >= 5]
        if direction == "up":
            cands = [n for n in cands if n >= prev] or cands
        elif direction == "down":
            cands = [n for n in cands if n <= prev] or cands
        if not cands:
            cands = pool
        return random.choice(cands)

    def _apply_phrase_structure(self, notes: List[MelodyNote], phrase_boundaries: List[int], pool_map: Dict[float, List[int]], lo: int, hi: int) -> List[MelodyNote]:
        if not phrase_boundaries or not notes:
            return notes
        boundary_bars = set(phrase_boundaries)
        result = list(notes)
        for i, note in enumerate(result):
            if note.bar in boundary_bars:
                is_last_in_bar = (i == len(result) - 1 or result[i + 1].bar != note.bar)
                if is_last_in_bar:
                    abs_beat = round((note.bar - 1) * 4.0 + note.position, 4)
                    pool = self._get_pool(pool_map, abs_beat, lo, hi)
                    stable = [p for p in pool if p % 12 in {0, 4, 7, 3}]
                    if stable:
                        result[i] = MelodyNote(pitch=min(stable, key=lambda p: abs(p - note.pitch)), duration=note.duration, position=note.position, bar=note.bar, velocity=note.velocity, locked=note.locked)
        return result

    def _add_hybrid_chord_tones(self, notes: List[MelodyNote], pool_map: Dict[float, List[int]], lo: int) -> List[MelodyNote]:
        result: List[MelodyNote] = []
        for note in notes:
            result.append(note)
            abs_beat = round((note.bar - 1) * 4.0 + note.position, 4)
            pool = self._get_pool(pool_map, abs_beat, lo, note.pitch - 1)
            if pool:
                harmonic = min(pool, key=lambda p: abs(p - (note.pitch - 7)))
                result.append(MelodyNote(pitch=harmonic, duration=note.duration, position=note.position, bar=note.bar, velocity=note.velocity - 15, is_chord_tone=True, role_annotation="chord_support"))
        return result

    def generate_rhythm(self, complexity: str, length_bars: int) -> List[float]:
        durations = self._default_durations(complexity, length_bars)
        positions: List[float] = []
        pos = 0.0
        for d in durations:
            positions.append(pos)
            pos += d
        return positions
