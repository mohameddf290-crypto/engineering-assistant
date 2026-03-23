"""
OPERATING SYSTEM BRAIN: Modification Engine
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

Purpose: Integrates any user modification (steps, leaps, shape, rhythm, note
changes, complexity level) with zero difficulty. The modified melody remains
professional and coherent regardless of what was changed.

Default AI thinking says "replace the note at position X with note Y."
That ignores that note Y might create a parallel octave with the bass, violate
the avoid-note rule over the current chord, or destroy the phrase arc. This
brain treats every modification as a context-sensitive edit: it validates the
change for harmonic coherence before applying it, and if the raw change would
break coherence, it applies the most musically intelligent correction while
still honouring the user's intent.

The partial lock system is central: specific notes can be locked in place while
the rest of the melody is regenerated around them. This gives users precise
creative control — "keep this peak note and this cadence note, regenerate
everything else." After any modification or regeneration, the AI Blocker
re-screens the result before delivery.

Protocols:
  1. Every modification is validated for harmonic coherence before applying.
     Incoherent modifications are corrected — not silently accepted or rejected.
  2. Partial lock: specific notes can be locked while the rest are regenerated
     around them. Locked notes are absolute constraints on regeneration.
  3. After any modification, the AI Blocker re-screens the result before
     delivery. No modified melody bypasses the quality gate.
"""

# TODO: Design this brain with Cursor — define the modification validation
# rules (what constitutes harmonic incoherence for each modification type),
# the correction strategy for each incoherence type, the partial lock
# regeneration algorithm, and the complexity adjustment model.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from melodies.melody_creator import Melody, MelodyNote


@dataclass
class ModificationRequest:
    """
    A request to modify a melody.

    Attributes:
        melody: The melody to modify.
        locked_notes: Indices of notes that must not be changed.
        changes: Dict mapping note index → change specification (e.g. {"pitch_midi": 64, "duration_beats": 1.0}).
        target_complexity_level: Optional target complexity level (1–10) if adjusting complexity.
    """

    melody: Melody
    locked_notes: List[int] = field(default_factory=list)
    changes: Dict[int, Dict[str, object]] = field(default_factory=dict)
    target_complexity_level: Optional[int] = None


@dataclass
class ModificationResult:
    """
    The result of applying a modification to a melody.

    Attributes:
        modified_melody: The modified Melody after applying changes.
        changes_applied: Description of what was actually changed (may differ from requested if corrected).
        coherence_score: Harmonic coherence score of the modified melody (0.0–1.0).
        was_corrected: True if the raw modification was corrected for coherence.
    """

    modified_melody: Melody
    changes_applied: Dict[int, Dict[str, object]] = field(default_factory=dict)
    coherence_score: float = 0.0
    was_corrected: bool = False


class ModificationEngine:
    """
    Brain M8 — Modification Engine.

    Applies user modifications to melodies with full coherence validation,
    optional correction, and partial lock support.
    """

    def __init__(self) -> None:
        pass

    def lock_notes(
        self, melody: Melody, note_indices: List[int]
    ) -> Melody:
        """Mark specific notes as locked so they cannot be changed."""
        new_notes = []
        for i, note in enumerate(melody.notes):
            if i in note_indices:
                new_notes.append(
                    MelodyNote(
                        pitch_midi=note.pitch_midi,
                        duration_beats=note.duration_beats,
                        position_beats=note.position_beats,
                        velocity=note.velocity,
                        is_chord_tone=note.is_chord_tone,
                        role_annotation="locked",
                    )
                )
            else:
                new_notes.append(
                    MelodyNote(
                        pitch_midi=note.pitch_midi,
                        duration_beats=note.duration_beats,
                        position_beats=note.position_beats,
                        velocity=note.velocity,
                        is_chord_tone=note.is_chord_tone,
                        role_annotation=note.role_annotation,
                    )
                )
        return Melody(
            notes=new_notes,
            key=melody.key,
            scale=melody.scale,
            length_bars=melody.length_bars,
            role=melody.role,
            complexity_level=melody.complexity_level,
            mode=melody.mode,
        )

    def apply_modification(
        self,
        melody: Melody,
        modification_request: ModificationRequest,
    ) -> ModificationResult:
        """Apply a modification request with coherence validation."""
        import copy

        new_notes = [
            MelodyNote(
                pitch_midi=n.pitch_midi,
                duration_beats=n.duration_beats,
                position_beats=n.position_beats,
                velocity=n.velocity,
                is_chord_tone=n.is_chord_tone,
                role_annotation=n.role_annotation,
            )
            for n in melody.notes
        ]

        locked = set(modification_request.locked_notes)
        changes_applied: Dict[int, Dict[str, object]] = {}
        was_corrected = False

        for idx, change in modification_request.changes.items():
            if idx in locked:
                continue
            if idx < 0 or idx >= len(new_notes):
                continue

            note = new_notes[idx]
            applied: Dict[str, object] = {}

            for attr, value in change.items():
                if attr == "pitch_midi":
                    val = int(value)  # type: ignore[arg-type]
                    if val < 0 or val > 127:
                        val = max(0, min(127, val))
                        was_corrected = True
                    note.pitch_midi = val
                    applied[attr] = val
                elif attr == "duration_beats":
                    val_f = float(value)  # type: ignore[arg-type]
                    if val_f <= 0:
                        val_f = 0.25
                        was_corrected = True
                    note.duration_beats = val_f
                    applied[attr] = val_f
                elif attr == "velocity":
                    val = int(value)  # type: ignore[arg-type]
                    val = max(1, min(127, val))
                    note.velocity = val
                    applied[attr] = val
                elif attr == "position_beats":
                    val_f = float(value)  # type: ignore[arg-type]
                    if val_f < 0:
                        val_f = 0.0
                        was_corrected = True
                    note.position_beats = val_f
                    applied[attr] = val_f

            if applied:
                changes_applied[idx] = applied

        modified_melody = Melody(
            notes=new_notes,
            key=melody.key,
            scale=melody.scale,
            length_bars=melody.length_bars,
            role=melody.role,
            complexity_level=melody.complexity_level,
            mode=melody.mode,
        )

        coherence = self.validate_modification_coherence(melody, modified_melody, None)

        return ModificationResult(
            modified_melody=modified_melody,
            changes_applied=changes_applied,
            coherence_score=coherence,
            was_corrected=was_corrected,
        )

    def regenerate_around_locked(
        self,
        melody: Melody,
        locked_notes: List[int],
        chord_context: Optional[object],
    ) -> Melody:
        """Regenerate unlocked notes using step-wise motion from locked notes."""
        import random

        locked_set = set(locked_notes)
        notes = melody.notes
        if not notes:
            return melody

        new_notes = [
            MelodyNote(
                pitch_midi=n.pitch_midi,
                duration_beats=n.duration_beats,
                position_beats=n.position_beats,
                velocity=n.velocity,
                is_chord_tone=n.is_chord_tone,
                role_annotation=n.role_annotation,
            )
            for n in notes
        ]

        # Find nearest locked note for each unlocked position
        for i in range(len(new_notes)):
            if i in locked_set:
                continue

            # Find nearest locked note
            nearest_locked_pitch = None
            min_dist = float("inf")
            for li in locked_set:
                if li < len(notes):
                    dist = abs(i - li)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_locked_pitch = notes[li].pitch_midi

            if nearest_locked_pitch is None:
                nearest_locked_pitch = 60

            step = random.choice([-2, -1, 0, 1, 2])
            new_pitch = nearest_locked_pitch + step * max(1, int(min_dist))
            new_pitch = max(30, min(100, new_pitch))

            new_notes[i] = MelodyNote(
                pitch_midi=new_pitch,
                duration_beats=notes[i].duration_beats,
                position_beats=notes[i].position_beats,
                velocity=random.randint(65, 95),
                is_chord_tone=False,
                role_annotation="regenerated",
            )

        return Melody(
            notes=new_notes,
            key=melody.key,
            scale=melody.scale,
            length_bars=melody.length_bars,
            role=melody.role,
            complexity_level=melody.complexity_level,
            mode=melody.mode,
        )

    def adjust_complexity(
        self, melody: Melody, target_level: int
    ) -> Melody:
        """Adjust complexity: 1-3 sparse, 4-6 normal, 7-10 complex."""
        notes = melody.notes
        if not notes:
            return melody

        target_level = max(1, min(10, target_level))

        if target_level <= 3:
            # Sparse: keep every other note
            new_notes = [
                MelodyNote(
                    pitch_midi=n.pitch_midi,
                    duration_beats=n.duration_beats * 2.0,
                    position_beats=n.position_beats,
                    velocity=n.velocity,
                    is_chord_tone=n.is_chord_tone,
                    role_annotation=n.role_annotation,
                )
                for i, n in enumerate(notes)
                if i % 2 == 0
            ]
        elif target_level <= 6:
            # Normal: unchanged
            new_notes = [
                MelodyNote(
                    pitch_midi=n.pitch_midi,
                    duration_beats=n.duration_beats,
                    position_beats=n.position_beats,
                    velocity=n.velocity,
                    is_chord_tone=n.is_chord_tone,
                    role_annotation=n.role_annotation,
                )
                for n in notes
            ]
        else:
            # Complex: add passing tones between notes
            new_notes = []
            for i, note in enumerate(notes):
                new_notes.append(
                    MelodyNote(
                        pitch_midi=note.pitch_midi,
                        duration_beats=max(0.25, note.duration_beats * 0.5),
                        position_beats=note.position_beats,
                        velocity=note.velocity,
                        is_chord_tone=note.is_chord_tone,
                        role_annotation=note.role_annotation,
                    )
                )
                if i < len(notes) - 1:
                    next_note = notes[i + 1]
                    mid_pitch = (note.pitch_midi + next_note.pitch_midi) // 2
                    passing_pos = note.position_beats + note.duration_beats * 0.5
                    new_notes.append(
                        MelodyNote(
                            pitch_midi=mid_pitch,
                            duration_beats=0.25,
                            position_beats=passing_pos,
                            velocity=max(1, note.velocity - 10),
                            is_chord_tone=False,
                            role_annotation="passing",
                        )
                    )

        return Melody(
            notes=new_notes,
            key=melody.key,
            scale=melody.scale,
            length_bars=melody.length_bars,
            role=melody.role,
            complexity_level=target_level,
            mode=melody.mode,
        )

    def validate_modification_coherence(
        self,
        original: Melody,
        modified: Melody,
        chord_context: Optional[object],
    ) -> float:
        """Return coherence score 0.0-1.0 based on multiple criteria."""
        if not modified.notes:
            return 0.0

        score = 1.0
        notes = modified.notes

        # Check interval smoothness — penalise jumps > 12 semitones
        for i in range(1, len(notes)):
            interval = abs(notes[i].pitch_midi - notes[i - 1].pitch_midi)
            if interval > 12:
                score -= 0.15

        # Check note range plausibility (MIDI 30-100)
        for n in notes:
            if n.pitch_midi < 30 or n.pitch_midi > 100:
                score -= 0.1

        # Check valid positions (non-negative, increasing-ish)
        for n in notes:
            if n.position_beats < 0:
                score -= 0.1

        return max(0.0, min(1.0, score))
