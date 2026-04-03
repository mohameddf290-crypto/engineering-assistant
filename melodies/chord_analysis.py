"""
Chord Analysis Engine — Melodies package.
Analyses any chord progression and builds per-beat note availability maps
for the Melody Creation Brain.

Original header preserved below.
----------------------------------------------------------------------
OPERATING SYSTEM BRAIN: Chord Analysis Engine (Melodies)
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

Purpose: Analyzes any chord progression (from Chords module or external) and
extracts everything needed for melody generation: harmonic structure, tension
points, resolution points, available note pools.

Default AI thinking says "use the chord root notes as the melody." That is
not a melody — it is an arpeggio with no rhythmic or melodic intelligence.
This brain performs a full harmonic analysis pipeline specifically oriented
toward melody generation: it identifies chord tones, available tensions,
approach notes, avoid notes, harmonic rhythm, and builds the complete tension/
resolution arc — everything the Melody Creation Brain needs to make informed
note-by-note decisions.

Every chord in the progression is fully analysed. The note pool is constructed
per-chord with priority weighting: chord tones are highest priority, available
extensions come second, passing/approach tones come third. Avoid notes are
explicitly identified and must never appear as strong beat melody notes.

Protocols:
  1. Every chord is fully analysed: chord tones, available extensions,
     approach notes, avoid notes. Partial analysis is not acceptable.
  2. Harmonic rhythm is mapped per-bar and per-beat — the melody engine
     needs to know exactly when harmonic changes occur.
  3. Note pool is constructed per-chord with priority weighting (chord tones
     > extensions > passing tones). The weighting drives note selection
     probability in the Melody Creation Brain.
"""

# TODO: Design this brain with Cursor — define the note pool construction
# algorithm (how chord quality + key determines available tensions and avoid
# notes), the tension arc mapping model, the approach note calculation rules,
# and the priority weighting system for melody note selection.

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

from chords.chord_creator import ChordProgression, ChordVoicing

# ── Music-theory constants ─────────────────────────────────────────────────

_NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

_NOTE_NAME_TO_PC: Dict[str, int] = {
    "C": 0, "B#": 0,
    "C#": 1, "Db": 1,
    "D": 2,
    "D#": 3, "Eb": 3,
    "E": 4, "Fb": 4,
    "F": 5, "E#": 5,
    "F#": 6, "Gb": 6,
    "G": 7,
    "G#": 8, "Ab": 8,
    "A": 9,
    "A#": 10, "Bb": 10,
    "B": 11, "Cb": 11,
}

_CHORD_INTERVALS: Dict[str, List[int]] = {
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

# Extra tension intervals (above root) available over each quality.
_TENSIONS: Dict[str, List[int]] = {
    "maj":   [2, 9, 14],
    "min":   [2, 5, 14],
    "dom7":  [1, 2, 3, 5, 6, 14],
    "maj7":  [2, 9, 14],
    "m7":    [2, 5, 14],
    "dim":   [2, 5, 8],
    "dim7":  [2, 5],
    "aug":   [2, 9],
    "m7b5":  [2, 5],
    "sus2":  [7, 10, 14],
    "sus4":  [7, 10, 14],
    "maj9":  [9, 17],
    "m9":    [5, 17],
    "dom9":  [1, 3, 5, 6],
    "add9":  [9, 17],
    "13":    [],
    "madd9": [9],
    "6":     [2, 14],
    "m6":    [2, 14],
    "maj11": [9],
    "m11":   [9],
}

# Notes to avoid on strong beats per chord quality (semitones above root).
_AVOID: Dict[str, List[int]] = {
    "maj":   [5],
    "maj7":  [5, 10],
    "min":   [],
    "m7":    [6],
    "dom7":  [],
    "dom9":  [],
    "dim":   [1, 6],
    "dim7":  [1],
    "aug":   [5],
    "sus2":  [3, 4],
    "sus4":  [3, 4],
}

# Tension level (0.0–1.0) per quality — used for tension arc.
_CHORD_TENSION_LEVEL: Dict[str, float] = {
    "maj": 0.1, "maj7": 0.2, "maj9": 0.3, "add9": 0.25, "6": 0.15,
    "min": 0.3, "m7": 0.35, "m9": 0.4, "m6": 0.35, "madd9": 0.4,
    "dom7": 0.6, "dom9": 0.65, "13": 0.7,
    "aug": 0.7, "sus2": 0.4, "sus4": 0.45,
    "dim": 0.75, "dim7": 0.8, "m7b5": 0.7,
    "maj11": 0.5, "m11": 0.55,
}

# Ordered patterns for quality suffix parsing (longer first to avoid greedy clash).
_QUALITY_PATTERNS: List[Tuple[str, str]] = [
    ("maj11", "maj11"), ("maj9", "maj9"), ("maj7", "maj7"),
    ("Maj7", "maj7"), ("M7", "maj7"), ("M9", "maj9"),
    ("m7b5", "m7b5"), ("ø", "m7b5"),
    ("m11", "m11"), ("m9", "m9"), ("m7", "m7"),
    ("min7", "m7"), ("min9", "m9"), ("min11", "m11"),
    ("dim7", "dim7"), ("o7", "dim7"), ("dim", "dim"), ("o", "dim"),
    ("aug", "aug"), ("+", "aug"),
    ("dom7", "dom7"), ("dom9", "dom9"),
    ("add9", "add9"), ("add2", "add9"),
    ("13", "13"), ("11", "maj11"), ("9", "dom9"), ("7", "dom7"),
    ("sus4", "sus4"), ("sus2", "sus2"), ("sus", "sus4"),
    ("m6", "m6"), ("6", "6"),
    ("m", "min"), ("min", "min"),
    ("maj", "maj"),
    ("", "maj"),
]

# NoteAvailabilityMap: beat_position → {category: [midi, ...]}
NoteAvailabilityMap = Dict[float, Dict[str, List[int]]]


# ── Helpers ────────────────────────────────────────────────────────────────

def _note_pool_for_pcs(pcs: set, lo: int = 36, hi: int = 96) -> List[int]:
    """All MIDI notes in [lo, hi] whose pitch-class is in *pcs*."""
    return sorted(n for n in range(lo, hi + 1) if n % 12 in pcs)


def parse_chord_name(chord_str: str) -> Tuple[int, str]:
    """Parse a chord name string to (root_midi, quality).

    The root MIDI note is placed in the C4-B4 octave (60–71).

    Examples
    --------
    >>> parse_chord_name("Cmaj7")  → (60, "maj7")
    >>> parse_chord_name("Am7")   → (69, "m7")
    >>> parse_chord_name("F")     → (65, "maj")
    """
    chord_str = chord_str.strip()
    # Match root (longest first to catch e.g. "Bb" before "B")
    root_pc: Optional[int] = None
    suffix = chord_str
    for note in sorted(_NOTE_NAME_TO_PC.keys(), key=len, reverse=True):
        if chord_str.startswith(note):
            root_pc = _NOTE_NAME_TO_PC[note]
            suffix = chord_str[len(note):]
            break
    if root_pc is None:
        return (60, "maj")

    quality = "maj"
    for pattern, qual in _QUALITY_PATTERNS:
        if suffix == pattern or (pattern and suffix.startswith(pattern)):
            quality = qual
            break

    return (60 + root_pc, quality)  # place root in C4-B4 range


@dataclass
class ChordAnalysisResult:
    """
    Complete harmonic analysis of a chord progression for melody generation.

    Attributes:
        progression: The source ChordProgression that was analysed.
        note_pools_per_chord: Mapping of chord index → prioritised note list (MIDI numbers).
        tension_arc: Tension score (0.0–1.0) per beat across the progression.
        resolution_points: List of (bar, beat) positions where resolution occurs.
        approach_note_map: Mapping of chord transition index → approach MIDI note numbers.
        avoid_note_map: Mapping of chord index → MIDI note numbers to avoid on strong beats.
        harmonic_rhythm_grid: Mapping of bar → list of (beat, chord_index) pairs.
    """

    progression: ChordProgression
    note_pools_per_chord: Dict[int, List[int]] = field(default_factory=dict)
    tension_arc: List[float] = field(default_factory=list)
    resolution_points: List[Tuple[int, float]] = field(default_factory=list)
    approach_note_map: Dict[int, List[int]] = field(default_factory=dict)
    avoid_note_map: Dict[int, List[int]] = field(default_factory=dict)
    harmonic_rhythm_grid: Dict[int, List[Tuple[float, int]]] = field(default_factory=dict)


class ChordAnalysisEngine:
    """
    Brain M1 — Chord Analysis Engine (Melodies).

    Analyses a chord progression (ChordProgression or list of chord-name strings)
    and returns rich harmonic data for the Melody Creation Brain.
    """

    def __init__(self) -> None:
        pass

    # ── Public API ─────────────────────────────────────────────────────────

    def analyse_progression(
        self, progression: Union[ChordProgression, List[str]]
    ) -> "ChordAnalysisResult":
        """Full harmonic analysis pipeline. Returns ChordAnalysisResult."""
        prog = self._normalise_to_progression(progression)

        note_pools_per_chord: Dict[int, List[int]] = {}
        avoid_note_map: Dict[int, List[int]] = {}
        approach_note_map: Dict[int, List[int]] = {}
        harmonic_rhythm_grid: Dict[int, List[Tuple[float, int]]] = {}

        for i, voicing in enumerate(prog.voicings):
            note_pools_per_chord[i] = self.build_note_pools(voicing)
            avoid_note_map[i] = self.get_avoid_notes(voicing)

        for i in range(len(prog.voicings) - 1):
            approach_note_map[i] = self.get_approach_notes(
                prog.voicings[i], prog.voicings[i + 1]
            )

        beat = 0.0
        for i, v in enumerate(prog.voicings):
            bar = int(beat // 4) + 1
            beat_in_bar = beat % 4.0
            harmonic_rhythm_grid.setdefault(bar, []).append((beat_in_bar, i))
            beat += v.duration_beats

        tension_arc = self.map_tension_arc(prog)
        resolution_points = self.identify_resolution_points(prog)

        return ChordAnalysisResult(
            progression=prog,
            note_pools_per_chord=note_pools_per_chord,
            tension_arc=tension_arc,
            resolution_points=resolution_points,
            approach_note_map=approach_note_map,
            avoid_note_map=avoid_note_map,
            harmonic_rhythm_grid=harmonic_rhythm_grid,
        )

    def analyze_progression(
        self, progression: Union[ChordProgression, List[str]]
    ) -> NoteAvailabilityMap:
        """
        Analyse progression and return a per-beat NoteAvailabilityMap.

        Keys are absolute beat positions (0.0, 0.5, 1.0, …).
        Values are dicts with keys 'consonant', 'tension', 'passing'.
        """
        prog = self._normalise_to_progression(progression)
        note_map: NoteAvailabilityMap = {}
        beat_step = 0.5
        chord_starts: List[Tuple[float, ChordVoicing]] = []
        t = 0.0
        for v in prog.voicings:
            chord_starts.append((t, v))
            t += v.duration_beats
        total_beats = t

        pos = 0.0
        while pos < total_beats:
            active = chord_starts[0][1]
            for (cs, v) in chord_starts:
                if cs <= pos:
                    active = v
            root_pc = active.root % 12
            quality = active.quality
            note_map[round(pos, 4)] = {
                "consonant": _build_consonant_pool(root_pc, quality),
                "tension":   _build_tension_pool(root_pc, quality),
                "passing":   _build_passing_pool(root_pc, quality),
            }
            pos += beat_step
        return note_map

    def build_note_pools(self, chord: ChordVoicing) -> List[int]:
        """
        Prioritised note pool: chord tones first, then extensions, then passing.
        Returns MIDI numbers in range 36–96.
        """
        root_pc = chord.root % 12
        quality = chord.quality
        consonant = _build_consonant_pool(root_pc, quality)
        tension   = _build_tension_pool(root_pc, quality)
        passing   = _build_passing_pool(root_pc, quality)
        # Deduplicate while preserving priority order
        seen: set = set()
        pool: List[int] = []
        for n in consonant + tension + passing:
            if n not in seen:
                seen.add(n)
                pool.append(n)
        return pool

    def map_tension_arc(self, progression: ChordProgression) -> List[float]:
        """Per-beat tension scores (0.0–1.0) across the progression."""
        arc: List[float] = []
        total_beats = sum(v.duration_beats for v in progression.voicings)
        abs_beat = 0.0
        for v in progression.voicings:
            base_tension = _CHORD_TENSION_LEVEL.get(v.quality, 0.4)
            # Position bonus: tension peaks around 65-75% through the progression
            pos_ratio = abs_beat / max(total_beats, 1)
            position_bonus = max(0.0, 0.2 * (1.0 - abs(pos_ratio - 0.7) * 3))
            tension = min(1.0, base_tension + position_bonus)
            beats = int(v.duration_beats / 0.5)
            arc.extend([round(tension, 3)] * max(1, beats))
            abs_beat += v.duration_beats
        return arc

    def identify_resolution_points(
        self, progression: ChordProgression
    ) -> List[Tuple[int, float]]:
        """
        Return (bar, beat_in_bar) tuples where harmonic resolution occurs.
        Detects V→I, vii°→I, and tension-reducing movements.
        """
        points: List[Tuple[int, float]] = []
        voicings = progression.voicings
        abs_beat = 0.0
        for i in range(1, len(voicings)):
            prev = voicings[i - 1]
            curr = voicings[i]
            prev_tension = _CHORD_TENSION_LEVEL.get(prev.quality, 0.4)
            curr_tension = _CHORD_TENSION_LEVEL.get(curr.quality, 0.4)
            is_resolution = False
            # Authentic cadence: dominant → tonic (root a 5th above tonic)
            interval = (curr.root - prev.root) % 12
            if prev.quality in ("dom7", "dom9", "maj", "13") and curr.quality in ("maj", "min", "maj7", "m7"):
                if interval == 5:  # V→I (root motion down a 5th = up a 4th)
                    is_resolution = True
            # Leading-tone resolution
            if prev.quality in ("dim", "dim7", "m7b5") and interval in (1, 11):
                is_resolution = True
            # General tension drop
            if curr_tension < prev_tension - 0.25:
                is_resolution = True
            if is_resolution:
                bar = int(abs_beat // 4) + 1
                beat_in_bar = abs_beat % 4.0
                points.append((bar, beat_in_bar))
            abs_beat += prev.duration_beats
        return points

    def get_approach_notes(
        self, chord: ChordVoicing, next_chord: ChordVoicing
    ) -> List[int]:
        """
        Chromatic and diatonic approach notes into next_chord's tones.
        Returns MIDI notes in range 48–96.
        """
        root_pc = next_chord.root % 12
        quality = next_chord.quality
        target_pcs = set((root_pc + iv) % 12 for iv in _CHORD_INTERVALS.get(quality, [0, 4, 7]))
        approach_pcs: set = set()
        for pc in target_pcs:
            approach_pcs.add((pc - 1) % 12)  # chromatic below
            approach_pcs.add((pc + 1) % 12)  # chromatic above
            approach_pcs.add((pc - 2) % 12)  # diatonic below (whole step)
        # Exclude target chord tones from approach set
        approach_pcs -= target_pcs
        return _note_pool_for_pcs(approach_pcs, 48, 96)

    def get_avoid_notes(self, chord: ChordVoicing) -> List[int]:
        """
        MIDI notes to avoid on strong beats over this chord (range 48–96).
        """
        root_pc = chord.root % 12
        avoid_ivs = _AVOID.get(chord.quality, [])
        avoid_pcs = set((root_pc + iv) % 12 for iv in avoid_ivs)
        return _note_pool_for_pcs(avoid_pcs, 48, 96)

    # ── Helpers ────────────────────────────────────────────────────────────

    def _normalise_to_progression(
        self, progression: Union[ChordProgression, List[str]]
    ) -> ChordProgression:
        """Convert list-of-strings to ChordProgression if needed."""
        if isinstance(progression, ChordProgression):
            return progression
        voicings: List[ChordVoicing] = []
        bar = 1
        for chord_str in progression:
            root_midi, quality = parse_chord_name(chord_str)
            intervals = _CHORD_INTERVALS.get(quality, [0, 4, 7])
            midi_notes = [root_midi + iv for iv in intervals]
            voicings.append(ChordVoicing(
                root=root_midi,
                quality=quality,
                midi_notes=midi_notes,
                bass_note=root_midi - 24,
                duration_beats=2.0,
                position_bar=bar,
            ))
            bar += 1
        return ChordProgression(
            voicings=voicings,
            key=_NOTES[voicings[0].root % 12] if voicings else "C",
            scale="major",
            length_bars=max(1, len(voicings) // 2),
        )


# ── Note-pool builders ─────────────────────────────────────────────────────

def _build_consonant_pool(root_pc: int, quality: str, lo: int = 36, hi: int = 96) -> List[int]:
    pcs = set((root_pc + iv) % 12 for iv in _CHORD_INTERVALS.get(quality, [0, 4, 7]))
    return _note_pool_for_pcs(pcs, lo, hi)


def _build_tension_pool(root_pc: int, quality: str, lo: int = 36, hi: int = 96) -> List[int]:
    chord_pcs = set((root_pc + iv) % 12 for iv in _CHORD_INTERVALS.get(quality, [0, 4, 7]))
    tension_pcs = set((root_pc + iv) % 12 for iv in _TENSIONS.get(quality, []))
    tension_only = tension_pcs - chord_pcs
    return _note_pool_for_pcs(tension_only, lo, hi)


def _build_passing_pool(root_pc: int, quality: str, lo: int = 36, hi: int = 96) -> List[int]:
    chord_pcs = set((root_pc + iv) % 12 for iv in _CHORD_INTERVALS.get(quality, [0, 4, 7]))
    tension_pcs = set((root_pc + iv) % 12 for iv in _TENSIONS.get(quality, []))
    used = chord_pcs | tension_pcs
    passing_pcs = set(range(12)) - used
    return _note_pool_for_pcs(passing_pcs, lo, hi)

