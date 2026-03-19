"""
Piano Roll-Style Editor Logic (Melodies)

UI-logic module for the in-app piano roll-style melody editor. Handles note
position, pitch, duration adjustments, and partial lock state management.

This is not a generation brain — it is a stateful UI layer. It does not make
musical decisions; it manages the editor state and exposes operations that the
UI layer can call directly. The partial lock state is a first-class concern of
this module: any note can be individually locked to prevent modification.
"""

# TODO: Design this editor with Cursor — define the full state management
# model, the lock state persistence strategy, the MIDI export format, undo/redo
# stack requirements, and how editor state syncs back to the Melody data model.

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set

from melodies.melody_creator import Melody


@dataclass
class MelodyEditorState:
    """
    The current state of the melody editor.

    Attributes:
        melody: The Melody currently loaded in the editor.
        locked_note_indices: Set of note indices that are locked from editing.
        selected_note_index: Index of the currently selected note (None if none selected).
        playback_position: Current playback position in beats.
        zoom_level: Current horizontal zoom level (1.0 = default).
        is_playing: Whether playback is currently active.
    """

    melody: Optional[Melody] = None
    locked_note_indices: Set[int] = field(default_factory=set)
    selected_note_index: Optional[int] = None
    playback_position: float = 0.0
    zoom_level: float = 1.0
    is_playing: bool = False


class MelodyEditor:
    """
    Piano Roll-Style Editor — Melodies.

    Manages the in-app piano roll editor for melody editing. Exposes operations
    for note selection, pitch adjustments, duration editing, lock toggling,
    and MIDI export.
    """

    def __init__(self) -> None:
        self._state: MelodyEditorState = MelodyEditorState()

    def load_melody(self, melody: Melody) -> None:
        """
        Load a melody into the editor.

        TODO: Populate self._state.melody, reset playback position, clear
        selection, clear lock state, and initialise any internal layout data
        structures required for the piano roll display.
        """
        raise NotImplementedError(
            "TODO: Implement melody loading. Reset all editor state and "
            "prepare display data structures."
        )

    def select_note(self, index: int) -> None:
        """
        Select a note by its index in the current melody.

        TODO: Validate index against the current melody note count. Update
        self._state.selected_note_index and notify any registered listeners.
        """
        raise NotImplementedError(
            "TODO: Implement note selection. Validate index and update state."
        )

    def move_note_pitch(self, index: int, semitones: int) -> None:
        """
        Move a note's pitch by a number of semitones.

        TODO: Check that the note at index is not locked. Adjust pitch_midi
        by semitones. Validate that the result is in range (0–127).
        """
        raise NotImplementedError(
            "TODO: Implement semitone pitch adjustment. Check lock state and "
            "validate MIDI range (0–127)."
        )

    def move_note_octave(self, index: int, octaves: int) -> None:
        """
        Move a note's pitch by a number of octaves (12 semitones each).

        TODO: Check that the note at index is not locked. Adjust pitch_midi
        by octaves * 12. Validate that the result is in range (0–127).
        """
        raise NotImplementedError(
            "TODO: Implement octave pitch adjustment. Check lock state and "
            "validate MIDI range (0–127)."
        )

    def adjust_note_duration(self, index: int, new_duration_beats: float) -> None:
        """
        Adjust the duration of a specific note.

        TODO: Check that the note at index is not locked. Validate
        new_duration_beats (must be positive). Update the note duration and
        recompute the positions of any notes that follow in the timeline.
        """
        raise NotImplementedError(
            "TODO: Implement note duration adjustment. Check lock state, "
            "validate duration, and recompute subsequent note positions."
        )

    def toggle_note_lock(self, index: int) -> None:
        """
        Toggle the lock state of a note.

        TODO: If the note at index is in self._state.locked_note_indices,
        remove it (unlock). Otherwise add it (lock). Update the display state.
        """
        raise NotImplementedError(
            "TODO: Implement note lock toggling. Add to or remove from "
            "locked_note_indices and update display state."
        )

    def export_to_midi(self, output_path: str) -> Path:
        """
        Export the current melody to a MIDI file.

        Returns the Path of the exported file.

        TODO: Convert all MelodyNotes to MIDI events with correct note on/off
        timing, using pitch_midi, duration_beats, position_beats, and velocity.
        Write a valid Type 1 MIDI file to output_path.
        """
        raise NotImplementedError(
            "TODO: Implement MIDI export. Convert all notes to note events "
            "with correct timing and write a valid MIDI file."
        )

    def get_editor_state(self) -> MelodyEditorState:
        """
        Return the current editor state.

        TODO: Return a copy of self._state to prevent external mutation of
        the internal state object.
        """
        raise NotImplementedError(
            "TODO: Implement state retrieval. Return a copy, not a reference."
        )
