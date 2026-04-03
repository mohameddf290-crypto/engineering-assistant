"""
Chord Editor for the Chords package.
Provides editing operations for chord progressions.
"""
from __future__ import annotations

import copy
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from chords.chord_creator import ChordProgression, ChordVoicing


@dataclass
class ChordEditorState:
    progression: Optional[ChordProgression] = None
    selected_chord_index: Optional[int] = None
    playback_position: float = 0.0
    zoom_level: float = 1.0
    is_playing: bool = False
    history: List[ChordProgression] = field(default_factory=list)
    future: List[ChordProgression] = field(default_factory=list)


def _encode_vlq(value: int) -> bytes:
    if value < 128:
        return bytes([value])
    result = []
    result.append(value & 0x7F)
    value >>= 7
    while value:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    return bytes(reversed(result))


class ChordEditor:
    """Provides editing operations for chord progressions with undo/redo support."""

    def __init__(self) -> None:
        self._state = ChordEditorState()

    def add_chord(
        self, state: ChordEditorState, chord_voicing: ChordVoicing, position: int = -1
    ) -> ChordEditorState:
        new_history = list(state.history) + ([state.progression] if state.progression else [])
        prog = copy.deepcopy(state.progression) if state.progression else ChordProgression()
        voicings = list(prog.voicings)
        if position < 0 or position >= len(voicings):
            voicings.append(chord_voicing)
        else:
            voicings.insert(position, chord_voicing)
        prog.voicings = voicings
        return ChordEditorState(
            progression=prog,
            selected_chord_index=state.selected_chord_index,
            playback_position=state.playback_position,
            zoom_level=state.zoom_level,
            is_playing=state.is_playing,
            history=new_history,
            future=[],
        )

    def remove_chord(self, state: ChordEditorState, index: int) -> ChordEditorState:
        if state.progression is None:
            return state
        new_history = list(state.history) + [state.progression]
        prog = copy.deepcopy(state.progression)
        voicings = list(prog.voicings)
        if 0 <= index < len(voicings):
            voicings.pop(index)
        prog.voicings = voicings
        return ChordEditorState(
            progression=prog,
            selected_chord_index=None,
            playback_position=state.playback_position,
            zoom_level=state.zoom_level,
            is_playing=state.is_playing,
            history=new_history,
            future=[],
        )

    def update_chord_duration(
        self, state: ChordEditorState, index: int, duration: float
    ) -> ChordEditorState:
        if state.progression is None:
            return state
        new_history = list(state.history) + [state.progression]
        prog = copy.deepcopy(state.progression)
        if 0 <= index < len(prog.voicings):
            prog.voicings[index].duration_beats = duration
        return ChordEditorState(
            progression=prog,
            selected_chord_index=state.selected_chord_index,
            playback_position=state.playback_position,
            zoom_level=state.zoom_level,
            is_playing=state.is_playing,
            history=new_history,
            future=[],
        )

    def undo(self, state: ChordEditorState) -> ChordEditorState:
        if not state.history:
            return state
        new_history = list(state.history)
        previous_progression = new_history.pop()
        new_future = ([state.progression] if state.progression else []) + list(state.future)
        return ChordEditorState(
            progression=previous_progression,
            selected_chord_index=state.selected_chord_index,
            playback_position=state.playback_position,
            zoom_level=state.zoom_level,
            is_playing=state.is_playing,
            history=new_history,
            future=new_future,
        )

    def redo(self, state: ChordEditorState) -> ChordEditorState:
        if not state.future:
            return state
        new_future = list(state.future)
        next_progression = new_future.pop(0)
        new_history = list(state.history) + ([state.progression] if state.progression else [])
        return ChordEditorState(
            progression=next_progression,
            selected_chord_index=state.selected_chord_index,
            playback_position=state.playback_position,
            zoom_level=state.zoom_level,
            is_playing=state.is_playing,
            history=new_history,
            future=new_future,
        )

    def load_progression(self, progression: ChordProgression) -> None:
        if self._state.progression is not None:
            self._state.history.append(self._state.progression)
        self._state.progression = copy.deepcopy(progression)
        self._state.future = []

    def select_chord(self, index: int) -> None:
        self._state.selected_chord_index = index

    def adjust_chord_duration(self, index: int, new_duration: float) -> None:
        if self._state.progression and 0 <= index < len(self._state.progression.voicings):
            if self._state.progression is not None:
                self._state.history.append(copy.deepcopy(self._state.progression))
            self._state.progression.voicings[index].duration_beats = new_duration

    def move_chord(self, from_index: int, to_index: int) -> None:
        if self._state.progression is None:
            return
        voicings = list(self._state.progression.voicings)
        if 0 <= from_index < len(voicings) and 0 <= to_index < len(voicings):
            self._state.history.append(copy.deepcopy(self._state.progression))
            chord = voicings.pop(from_index)
            voicings.insert(to_index, chord)
            self._state.progression.voicings = voicings

    def transpose_chord(self, index: int, semitones: int) -> None:
        if self._state.progression is None:
            return
        if 0 <= index < len(self._state.progression.voicings):
            self._state.history.append(copy.deepcopy(self._state.progression))
            v = self._state.progression.voicings[index]
            v.root = v.root + semitones
            v.bass_note = max(36, min(47, v.bass_note + semitones))
            v.midi_notes = [max(21, min(108, n + semitones)) for n in v.midi_notes]

    def export_to_midi(self, output_path: str) -> Path:
        tempo = 500000  # 120 BPM
        ticks_per_beat = 480
        events = []
        tick = 0
        if self._state.progression:
            for v in self._state.progression.voicings:
                duration_ticks = int(v.duration_beats * ticks_per_beat)
                for note in v.midi_notes:
                    events.append((tick, 0x90, note, 100))
                    events.append((tick + duration_ticks, 0x80, note, 0))
                tick += duration_ticks
        events.sort(key=lambda e: (e[0], e[1]))
        track_data = bytearray()
        track_data += b'\x00\xff\x51\x03'
        track_data += struct.pack('>I', tempo)[1:]
        prev_tick = 0
        for tick, status, note, vel in events:
            delta = tick - prev_tick
            track_data += _encode_vlq(delta)
            track_data += bytes([status, note, vel])
            prev_tick = tick
        track_data += b'\x00\xff\x2f\x00'
        header = b'MThd' + struct.pack('>IHHH', 6, 0, 1, ticks_per_beat)
        track = b'MTrk' + struct.pack('>I', len(track_data)) + bytes(track_data)
        path = Path(output_path)
        path.write_bytes(header + track)
        return path

    def get_editor_state(self) -> ChordEditorState:
        return copy.deepcopy(self._state)
