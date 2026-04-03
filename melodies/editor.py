"""Melody Piano Roll Editor — stateful CRUD with undo/redo."""
from __future__ import annotations
import copy
from dataclasses import dataclass, field
from typing import List

from melodies.melody_creator import MelodyLine, MelodyNote


@dataclass
class MelodyEditorState:
    melody: MelodyLine
    history: List[MelodyLine] = field(default_factory=list)
    future: List[MelodyLine] = field(default_factory=list)


class MelodyEditor:
    """CRUD operations on MelodyLine with undo/redo support."""

    def _snapshot(self, state: MelodyEditorState) -> MelodyEditorState:
        state.history.append(copy.deepcopy(state.melody))
        state.future.clear()
        return state

    def add_note(self, state: MelodyEditorState, note: MelodyNote) -> MelodyEditorState:
        self._snapshot(state)
        state.melody.notes.append(note)
        state.melody.notes.sort(key=lambda n: (n.bar, n.position))
        return state

    def remove_note(self, state: MelodyEditorState, index: int) -> MelodyEditorState:
        if 0 <= index < len(state.melody.notes):
            self._snapshot(state)
            state.melody.notes.pop(index)
        return state

    def move_note(self, state: MelodyEditorState, index: int, new_pitch: int, new_position: float) -> MelodyEditorState:
        if 0 <= index < len(state.melody.notes):
            self._snapshot(state)
            note = state.melody.notes[index]
            note.pitch = max(0, min(127, new_pitch))
            note.position = max(0.0, new_position)
        return state

    def resize_note(self, state: MelodyEditorState, index: int, new_duration: float) -> MelodyEditorState:
        if 0 <= index < len(state.melody.notes):
            self._snapshot(state)
            state.melody.notes[index].duration = max(0.125, new_duration)
        return state

    def undo(self, state: MelodyEditorState) -> MelodyEditorState:
        if state.history:
            state.future.append(copy.deepcopy(state.melody))
            state.melody = state.history.pop()
        return state

    def redo(self, state: MelodyEditorState) -> MelodyEditorState:
        if state.future:
            state.history.append(copy.deepcopy(state.melody))
            state.melody = state.future.pop()
        return state
