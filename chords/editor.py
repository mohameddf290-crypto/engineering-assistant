"""
Piano Roll-Style Editor Logic (Chords)

UI-logic module for the in-app piano roll-style chord progression editor.
Handles per-chord duration editing, note position adjustments, playback
position tracking, and editor state management.

This is not a generation brain — it is a stateful UI layer. It does not make
musical decisions; it manages the editor state and exposes operations that the
UI layer can call directly.
"""

# TODO: Design this editor with Cursor — define the full state management
# model, the MIDI export format, undo/redo stack requirements, and how editor
# state syncs back to the ChordProgression data model.

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from chords.chord_creator import ChordProgression


@dataclass
class ChordEditorState:
    """
    The current state of the chord progression editor.

    Attributes:
        progression: The ChordProgression currently loaded in the editor.
        selected_chord_index: Index of the currently selected chord (None if none selected).
        playback_position: Current playback position in beats.
        zoom_level: Current horizontal zoom level (1.0 = default).
        is_playing: Whether playback is currently active.
    """

    progression: Optional[ChordProgression] = None
    selected_chord_index: Optional[int] = None
    playback_position: float = 0.0
    zoom_level: float = 1.0
    is_playing: bool = False


class ChordEditor:
    """
    Piano Roll-Style Editor — Chords.

    Manages the in-app piano roll editor for chord progression editing.
    Exposes operations for chord selection, duration editing, repositioning,
    transposition, and MIDI export.
    """

    def __init__(self) -> None:
        self._state: ChordEditorState = ChordEditorState()

    def load_progression(self, progression: ChordProgression) -> None:
        """
        Load a chord progression into the editor.

        TODO: Populate self._state.progression, reset playback position,
        clear selection, and initialise any internal layout data structures
        required for the piano roll display.
        """
        raise NotImplementedError(
            "TODO: Implement progression loading. Reset editor state and "
            "prepare all display data structures."
        )

    def select_chord(self, index: int) -> None:
        """
        Select a chord by its index in the current progression.

        TODO: Validate index against the current progression length, update
        self._state.selected_chord_index, and notify any registered listeners.
        """
        raise NotImplementedError(
            "TODO: Implement chord selection. Validate index and update state."
        )

    def adjust_chord_duration(self, index: int, new_duration_beats: float) -> None:
        """
        Adjust the duration of a specific chord.

        TODO: Validate new_duration_beats (must be positive), update the
        ChordVoicing at the given index, and recompute the positions of all
        subsequent chords to maintain a gapless timeline.
        """
        raise NotImplementedError(
            "TODO: Implement chord duration adjustment. Recompute all "
            "subsequent chord positions after any duration change."
        )

    def move_chord(self, from_index: int, to_index: int) -> None:
        """
        Move a chord from one position to another in the progression.

        TODO: Validate both indices, swap/insert the ChordVoicing at the
        new position, and recompute bar/beat positions for the affected range.
        """
        raise NotImplementedError(
            "TODO: Implement chord reordering. Recompute positions for all "
            "chords in the affected range after the move."
        )

    def transpose_chord(self, index: int, semitones: int) -> None:
        """
        Transpose a single chord by a number of semitones.

        TODO: Shift the root, bass_note, and all midi_notes in the ChordVoicing
        at the given index by the specified semitone offset. Validate that
        all resulting MIDI note numbers remain in the valid range (0–127).
        """
        raise NotImplementedError(
            "TODO: Implement single-chord transposition. Shift root, bass, "
            "and all MIDI notes. Validate MIDI range (0–127)."
        )

    def export_to_midi(self, output_path: str) -> Path:
        """
        Export the current progression to a MIDI file.

        Returns the Path of the exported file.

        TODO: Convert all ChordVoicings to MIDI events with correct note
        on/off timing. Write a valid Type 1 MIDI file to output_path.
        """
        raise NotImplementedError(
            "TODO: Implement MIDI export. Convert all voicings to note events "
            "with correct timing and write a valid MIDI file."
        )

    def get_editor_state(self) -> ChordEditorState:
        """
        Return the current editor state.

        TODO: Return a copy of self._state to prevent external mutation of
        the internal state object.
        """
        raise NotImplementedError(
            "TODO: Implement state retrieval. Return a copy, not a reference."
        )
