"""Melody AI Blocker — rejects boring/generic melody output."""
from __future__ import annotations
import math
from typing import List, Tuple

from melodies.melody_creator import MelodyLine, MelodyNote


class MelodyAIBlocker:
    """Screens melody output and rejects low-quality generations."""

    def check_melody(self, melody: MelodyLine) -> Tuple[bool, float, List[str]]:
        notes = melody.notes
        if not notes:
            return False, 0.0, ["Empty melody"]
        reasons: List[str] = []
        scores: List[float] = []

        # 1. Reject pure scale runs (>5 consecutive steps same direction)
        run_score = self._score_runs(notes)
        scores.append(run_score)
        if run_score < 0.3:
            reasons.append("Pure scale run detected — melody has no shape")

        # 2. Reject arpeggio-only patterns
        arp_score = self._score_not_arpeggio(notes)
        scores.append(arp_score)
        if arp_score < 0.3:
            reasons.append("Arpeggio-only pattern — melody just outlines chords")

        # 3. Reject tiny range
        range_score = self._score_range(notes)
        scores.append(range_score)
        if range_score < 0.2:
            reasons.append("Melody stays in fewer than 3 distinct pitches")

        # 4. Reject rhythmic flatness
        rhythm_score = self._score_rhythmic_variety(notes)
        scores.append(rhythm_score)
        if rhythm_score < 0.2:
            reasons.append("All notes have identical duration — no rhythmic interest")

        # 5. Singability — penalise jumps > octave
        sing_score = self._score_singability(notes)
        scores.append(sing_score)
        if sing_score < 0.2:
            reasons.append("Too many large leaps — melody is not singable")

        overall = sum(scores) / len(scores)
        passed = overall >= 0.45 and len(reasons) == 0
        return passed, round(overall, 3), reasons

    # ------------------------------------------------------------------ helpers
    def _score_runs(self, notes: List[MelodyNote]) -> float:
        if len(notes) < 3:
            return 1.0
        pitches = [n.pitch for n in notes]
        max_run = 1
        cur_run = 1
        for i in range(1, len(pitches)):
            diff_prev = pitches[i] - pitches[i - 1]
            if i >= 2:
                diff_pprev = pitches[i - 1] - pitches[i - 2]
                if diff_prev != 0 and diff_pprev != 0 and math.copysign(1, diff_prev) == math.copysign(1, diff_pprev):
                    cur_run += 1
                    max_run = max(max_run, cur_run)
                else:
                    cur_run = 1
            else:
                cur_run = 1
        if max_run > 7:
            return 0.0
        if max_run > 5:
            return 0.3
        if max_run > 4:
            return 0.6
        return 1.0

    def _score_not_arpeggio(self, notes: List[MelodyNote]) -> float:
        if len(notes) < 3:
            return 1.0
        pitches = [n.pitch for n in notes]
        intervals = [abs(pitches[i] - pitches[i - 1]) for i in range(1, len(pitches))]
        chord_intervals = {3, 4, 5, 7, 8, 9}
        chord_count = sum(1 for iv in intervals if iv in chord_intervals)
        ratio = chord_count / max(len(intervals), 1)
        if ratio > 0.85:
            return 0.1
        if ratio > 0.7:
            return 0.5
        return 1.0

    def _score_range(self, notes: List[MelodyNote]) -> float:
        pitches = set(n.pitch for n in notes)
        span = max(pitches) - min(pitches) if len(pitches) > 1 else 0
        if len(pitches) < 3 or span < 2:
            return 0.0
        if span < 5:
            return 0.4
        if span < 9:
            return 0.7
        return 1.0

    def _score_rhythmic_variety(self, notes: List[MelodyNote]) -> float:
        durations = set(round(n.duration, 2) for n in notes)
        if len(durations) == 1:
            return 0.0
        if len(durations) == 2:
            return 0.6
        return 1.0

    def _score_singability(self, notes: List[MelodyNote]) -> float:
        if len(notes) < 2:
            return 1.0
        pitches = [n.pitch for n in notes]
        big_leaps = sum(1 for i in range(1, len(pitches)) if abs(pitches[i] - pitches[i - 1]) > 12)
        ratio = big_leaps / max(len(pitches) - 1, 1)
        if ratio > 0.3:
            return 0.1
        if ratio > 0.15:
            return 0.5
        return 1.0
