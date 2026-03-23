"""
AI Blocker for the Chords package.
Screens chord progressions for AI patterns and clichés.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from chords.chord_creator import NOTES, SCALES, ChordProgression


@dataclass
class AIPatternResult:
    progression_id: str = ""
    patterns_detected: List[str] = field(default_factory=list)
    is_blocked: bool = False
    blocking_reasons: List[str] = field(default_factory=list)
    quality_score: float = 0.5


_BLACKLISTED_PATTERNS = [
    [1, 5, 6, 4],
    [1, 5, 6, 3, 4, 1, 4, 5],
]

_CLICHE_PATTERNS = [
    [2, 5, 1],
    [1, 4, 5],
    [1, 6, 2, 5],
    [1, 4, 1, 5],
]


def _get_scale_degree(root_pc: int, key: str, scale: str) -> int:
    key_pc = NOTES.index(key) if key in NOTES else 0
    intervals = SCALES.get(scale, SCALES["major"])
    for i, interval in enumerate(intervals):
        if (key_pc + interval) % 12 == root_pc % 12:
            return i + 1
    return 0


def _contains_rotation(sequence: List[int], pattern: List[int]) -> bool:
    n = len(pattern)
    if len(sequence) < n:
        return False
    rotations = [pattern[i:] + pattern[:i] for i in range(n)]
    for i in range(len(sequence) - n + 1):
        sub = sequence[i: i + n]
        if sub in rotations:
            return True
    return False


class AIBlocker:
    """Screens chord progressions for AI-generated patterns and clichés."""

    def __init__(self) -> None:
        self._blacklist = [list(p) for p in _BLACKLISTED_PATTERNS]

    def screen_progression(self, progression: ChordProgression) -> AIPatternResult:
        prog_id = f"{progression.key}_{progression.scale}_{len(progression.voicings)}"
        patterns = self.detect_ai_patterns(progression)
        cliches = self.detect_cliches(progression)
        all_patterns = patterns + cliches
        score = self.calculate_quality_score(progression)
        is_blocked = len(all_patterns) > 0 and score < 0.4
        return AIPatternResult(
            progression_id=prog_id,
            patterns_detected=all_patterns,
            is_blocked=is_blocked,
            blocking_reasons=all_patterns if is_blocked else [],
            quality_score=score,
        )

    def detect_ai_patterns(self, progression: ChordProgression) -> List[str]:
        patterns_found = []
        degrees = self._extract_scale_degrees(progression)
        for pattern in _BLACKLISTED_PATTERNS:
            if _contains_rotation(degrees, pattern):
                pattern_str = "-".join(
                    ["I", "II", "III", "IV", "V", "VI", "VII"][d - 1] if 1 <= d <= 7 else "?"
                    for d in pattern
                )
                patterns_found.append(f"blacklisted:{pattern_str}")
        if len(progression.voicings) >= 4:
            durations = [v.duration_beats for v in progression.voicings]
            if len(set(durations)) == 1:
                patterns_found.append("monotone_rhythm")
        if progression.voicings:
            all_plain = all(
                v.quality in ("maj", "min") and not v.extensions
                for v in progression.voicings
            )
            if all_plain:
                patterns_found.append("no_harmonic_color")
        return patterns_found

    def detect_cliches(self, progression: ChordProgression) -> List[str]:
        cliches_found = []
        degrees = self._extract_scale_degrees(progression)
        cliche_names = {
            str([2, 5, 1]): "ii-V-I",
            str([1, 4, 5]): "I-IV-V",
            str([1, 6, 2, 5]): "I-vi-ii-V",
            str([1, 4, 1, 5]): "I-IV-I-V",
        }
        for pattern in _CLICHE_PATTERNS:
            name = cliche_names.get(str(pattern), str(pattern))
            if _contains_rotation(degrees, pattern):
                cliches_found.append(f"cliche:{name}")
        return cliches_found

    def calculate_quality_score(self, progression: ChordProgression) -> float:
        if not progression.voicings:
            return 0.0
        harmonic = self.score_harmonic_interest(progression)
        voice_leading = self.score_voice_leading(progression)
        durations = [v.duration_beats for v in progression.voicings]
        rhythmic = min(1.0, len(set(durations)) / max(1, len(durations) * 0.5))
        return (harmonic * 0.4 + voice_leading * 0.3 + rhythmic * 0.3)

    def score_harmonic_interest(self, progression: ChordProgression) -> float:
        if not progression.voicings:
            return 0.0
        qualities = [v.quality for v in progression.voicings]
        unique_q = len(set(qualities))
        complex_qualities = {"maj7", "m7", "dom7", "m9", "maj9", "m7b5", "dim7", "aug", "sus2", "sus4", "add9"}
        n_complex = sum(1 for q in qualities if q in complex_qualities)
        has_extensions = any(v.extensions for v in progression.voicings)
        score = min(1.0, (unique_q / max(1, len(qualities))) + (n_complex / max(1, len(qualities))) * 0.5)
        if has_extensions:
            score = min(1.0, score + 0.1)
        return score

    def score_voice_leading(self, progression: ChordProgression) -> float:
        if len(progression.voicings) < 2:
            return 0.5
        total_movement = 0.0
        n = 0
        for i in range(1, len(progression.voicings)):
            prev = sorted([x for x in progression.voicings[i - 1].midi_notes if x >= 60])
            curr = sorted([x for x in progression.voicings[i].midi_notes if x >= 60])
            pairs = min(len(prev), len(curr))
            if pairs > 0:
                movement = sum(abs(curr[j] - prev[j]) for j in range(pairs)) / pairs
                total_movement += movement
                n += 1
        if n == 0:
            return 0.5
        avg = total_movement / n
        if avg <= 3:
            return 1.0
        elif avg <= 6:
            return 0.7
        elif avg <= 10:
            return 0.4
        return 0.2

    def get_blacklisted_patterns(self) -> List[List[int]]:
        return list(self._blacklist)

    def check_progression(self, progression: ChordProgression) -> Tuple[bool, float, List[str]]:
        result = self.screen_progression(progression)
        passed = not result.is_blocked
        return passed, result.quality_score, result.blocking_reasons

    def detect_blacklisted_patterns(self, progression: ChordProgression) -> List[str]:
        return self.detect_ai_patterns(progression)

    def _extract_scale_degrees(self, progression: ChordProgression) -> List[int]:
        degrees = []
        for v in progression.voicings:
            root_pc = v.root % 12
            deg = _get_scale_degree(root_pc, progression.key, progression.scale)
            degrees.append(deg)
        return degrees
