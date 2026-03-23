"""Melody Elongation System — extends a melody by N bars."""
from __future__ import annotations
import copy, random
from typing import Dict, List

from melodies.melody_creator import MelodyLine, MelodyNote


class MelodyElongationSystem:
    """Extends a MelodyLine while maintaining coherence."""

    def elongate(
        self,
        melody: MelodyLine,
        additional_bars: int,
        note_map: Dict[float, Dict[str, List[int]]],
    ) -> MelodyLine:
        if additional_bars <= 0:
            return melody
        strategy = self._pick_strategy(melody)
        if strategy == "motivic_development":
            extension = self._motivic_development(melody, additional_bars, note_map)
        elif strategy == "sequence":
            extension = self._sequence(melody, additional_bars, note_map)
        else:
            extension = self._augmentation(melody, additional_bars, note_map)

        result = copy.deepcopy(melody)
        offset_bar = melody.length_bars + 1
        for note in extension:
            note.bar += offset_bar - 1
        result.notes.extend(extension)
        result.length_bars = melody.length_bars + additional_bars
        return result

    def _pick_strategy(self, melody: MelodyLine) -> str:
        return random.choice(["motivic_development", "sequence", "augmentation"])

    def _motivic_development(
        self, melody: MelodyLine, bars: int, note_map: Dict
    ) -> List[MelodyNote]:
        """Take the first 2-bar motif and develop it."""
        if not melody.notes:
            return []
        motif = [n for n in melody.notes if n.bar <= 2]
        if not motif:
            motif = melody.notes[:4]
        extension: List[MelodyNote] = []
        bar = 1
        for b in range(bars):
            for src in motif:
                note = copy.deepcopy(src)
                note.bar = bar
                # vary pitch slightly
                note.pitch = max(36, min(96, note.pitch + random.choice([-2, 0, 2])))
                extension.append(note)
            bar += 1
        return extension[:bars * 4]  # cap

    def _sequence(self, melody: MelodyLine, bars: int, note_map: Dict) -> List[MelodyNote]:
        """Repeat motif transposed by a diatonic interval."""
        if not melody.notes:
            return []
        interval = random.choice([2, 3, -2, -3])
        motif = melody.notes[:min(4, len(melody.notes))]
        extension: List[MelodyNote] = []
        bar = 1
        for _ in range(bars):
            for src in motif:
                note = copy.deepcopy(src)
                note.bar = bar
                note.pitch = max(36, min(96, note.pitch + interval))
            bar += 1
            extension.extend([copy.deepcopy(n) for n in motif])
        return extension[:bars * 4]

    def _augmentation(self, melody: MelodyLine, bars: int, note_map: Dict) -> List[MelodyNote]:
        """Stretch rhythm by doubling durations."""
        if not melody.notes:
            return []
        motif = melody.notes[:min(4, len(melody.notes))]
        extension: List[MelodyNote] = []
        pos = 0.0
        bar = 1
        for src in motif:
            note = copy.deepcopy(src)
            note.duration = min(src.duration * 2, 4.0)
            note.position = pos
            note.bar = bar
            pos += note.duration
            if pos >= 4.0:
                pos = 0.0
                bar += 1
            extension.append(note)
            if bar > bars:
                break
        return extension
