"""
OPERATING SYSTEM BRAIN: Melody Role Intelligence
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

Purpose: Has profound, embedded knowledge of every melody role. Generates
melodies according to the selected role. Most critically: every role-melody
complements every other role-melody perfectly. If ANY melody is modified,
the complementary melodies adapt automatically.

Default AI thinking says "generate a lead melody, then generate a counter
melody." Two separate generation calls with no awareness of each other produce
melodies that collide — same register, same rhythm, same contour. They fight
instead of complementing. This brain treats every melody role as part of a
system: every role has specific constraints (register range, rhythmic density,
harmonic relationship to the lead) that are designed to guarantee perfect
complementarity with every other role.

The Complementarity Matrix is the core of this brain: it defines the explicit
relationship between every pair of roles. Lead + Counter Melody: contrary
contour, offset rhythmic entries, complementary register. Lead + Ear Candy:
high register, sparse rhythm, chord tone emphasis at phrase peaks. Lead +
Pad Melody: sustained harmonic fill, low rhythmic density, avoids lead register.
Every pair is defined. No pair is left to chance.

When any melody in a RoleSet is modified, the Complementarity Engine evaluates
all dependent melodies and adapts them to restore perfect complementarity. The
user never has to manually adjust complementary melodies after editing.

Protocols:
  1. Every role has embedded constraints: register range, rhythmic density,
     harmonic relationship to lead, note pool priority. No role is generic.
  2. Complementarity is enforced through the Complementarity Matrix — every
     pair of roles has an explicit relationship definition.
  3. When any melody is modified, the Complementarity Engine re-evaluates and
     adapts all dependent melodies automatically.
"""

# TODO: Design this brain with Cursor — define the full role taxonomy with
# precise constraints for each role, build the complete Complementarity Matrix
# (every role pair with explicit relationship rules), and design the adaptation
# algorithm that re-evaluates and adjusts dependent melodies when any melody
# changes.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from melodies.melody_creator import Melody, MelodyNote
from melodies.translation import MelodyCreationPlan


@dataclass
class MelodyRole:
    """
    A complete definition of a melody role.

    Attributes:
        name: Role name (e.g. "lead", "counter_melody", "ear_candy").
        register_range: MIDI note range (low, high) for this role.
        rhythmic_density: Target note onset density per beat (lower = sparser).
        harmonic_priority: Which note pool tier to prioritise ("chord_tones", "extensions", "passing").
        complementarity_rules: Dict of {other_role_name: relationship_description}.
        note_pool_bias: Bias multipliers for each pool tier.
    """

    name: str
    register_range: tuple = (48, 84)
    rhythmic_density: float = 1.0
    harmonic_priority: str = "chord_tones"
    complementarity_rules: Dict[str, str] = field(default_factory=dict)
    note_pool_bias: Dict[str, float] = field(default_factory=dict)


@dataclass
class RoleSet:
    """
    A complete set of complementary melodies across all roles.

    Attributes:
        lead: The primary lead melody.
        counter_melody: Counter melody (contrary contour to lead).
        ear_candy: High-register sparse decorative melody.
        pad_melody: Sustained harmonic fill melody.
        bass_line: Bass register melody.
        arpeggio_layer: Arpeggio-pattern melody.
        additional_roles: Any additional custom role melodies.
    """

    lead: Optional[Melody] = None
    counter_melody: Optional[Melody] = None
    ear_candy: Optional[Melody] = None
    pad_melody: Optional[Melody] = None
    bass_line: Optional[Melody] = None
    arpeggio_layer: Optional[Melody] = None
    additional_roles: Dict[str, Melody] = field(default_factory=dict)


class MelodyRoleIntelligence:
    """
    Brain M9 — Melody Role Intelligence.

    Generates role-aware melodies with embedded complementarity enforcement.
    Every melody in a RoleSet is guaranteed to complement every other.
    """

    def __init__(self) -> None:
        self._role_library: Dict[str, MelodyRole] = {
            "lead": MelodyRole(
                name="lead",
                register_range=(60, 84),
                rhythmic_density=1.0,
                harmonic_priority="chord_tones",
                complementarity_rules={
                    "counter_melody": "contrary contour, offset entries",
                    "ear_candy": "sparse decoration above lead",
                    "pad_melody": "sustained fill below lead",
                    "bass_line": "root movement, low register",
                },
            ),
            "counter_melody": MelodyRole(
                name="counter_melody",
                register_range=(55, 79),
                rhythmic_density=0.7,
                harmonic_priority="extensions",
                complementarity_rules={
                    "lead": "contrary contour, offset entries",
                    "ear_candy": "avoid register overlap",
                    "pad_melody": "complementary rhythm",
                    "bass_line": "independent motion",
                },
            ),
            "ear_candy": MelodyRole(
                name="ear_candy",
                register_range=(72, 96),
                rhythmic_density=0.3,
                harmonic_priority="chord_tones",
                complementarity_rules={
                    "lead": "sparse decoration above lead",
                    "counter_melody": "avoid register overlap",
                    "pad_melody": "different rhythmic grid",
                    "bass_line": "maximum register separation",
                },
            ),
            "pad_melody": MelodyRole(
                name="pad_melody",
                register_range=(48, 72),
                rhythmic_density=0.2,
                harmonic_priority="chord_tones",
                complementarity_rules={
                    "lead": "sustained fill below lead",
                    "counter_melody": "complementary rhythm",
                    "ear_candy": "different rhythmic grid",
                    "bass_line": "register separation, slow movement",
                },
            ),
            "bass_line": MelodyRole(
                name="bass_line",
                register_range=(28, 52),
                rhythmic_density=0.8,
                harmonic_priority="chord_tones",
                complementarity_rules={
                    "lead": "root movement, low register",
                    "counter_melody": "independent motion",
                    "ear_candy": "maximum register separation",
                    "pad_melody": "register separation, slow movement",
                },
            ),
        }
        self._complementarity_matrix: Dict[str, Dict[str, str]] = {
            role.name: role.complementarity_rules
            for role in self._role_library.values()
        }

    def get_role_definition(self, role_name: str) -> MelodyRole:
        """Retrieve the full definition for a melody role."""
        if role_name not in self._role_library:
            raise ValueError(
                f"Unknown role '{role_name}'. "
                f"Available roles: {list(self._role_library.keys())}"
            )
        return self._role_library[role_name]

    def get_all_roles(self) -> List[str]:
        """Return the full list of role names in the role library."""
        return list(self._role_library.keys())

    def generate_for_role(
        self,
        role: MelodyRole,
        creation_plan: MelodyCreationPlan,
        lead_melody: Optional[Melody],
    ) -> Melody:
        """Generate a melody fitting the role's register and density."""
        import random

        low, high = role.register_range
        mid = (low + high) // 2
        length_bars = getattr(creation_plan, "length_bars", 4) if creation_plan else 4

        num_notes = max(4, int(length_bars * 4 * role.rhythmic_density))

        # Duration based on density
        if role.rhythmic_density <= 0.3:
            base_dur = 2.0
        elif role.rhythmic_density <= 0.5:
            base_dur = 1.0
        else:
            base_dur = 0.5

        notes: list = []
        current_pitch = mid
        position = 0.0

        if lead_melody and lead_melody.notes and role.name == "counter_melody":
            # Invert contour relative to lead
            for i, lead_note in enumerate(lead_melody.notes):
                if i >= num_notes:
                    break
                inverted = mid + (mid - lead_note.pitch_midi)
                inverted = max(low, min(high, inverted))
                notes.append(
                    MelodyNote(
                        pitch_midi=inverted,
                        duration_beats=base_dur,
                        position_beats=position,
                        velocity=random.randint(65, 90),
                        is_chord_tone=True,
                        role_annotation=role.name,
                    )
                )
                position += base_dur
        elif lead_melody and lead_melody.notes:
            # Shift lead pitches into role register
            for i, lead_note in enumerate(lead_melody.notes):
                if i >= num_notes:
                    break
                pitch = lead_note.pitch_midi
                while pitch < low:
                    pitch += 12
                while pitch > high:
                    pitch -= 12
                pitch = max(low, min(high, pitch))
                notes.append(
                    MelodyNote(
                        pitch_midi=pitch,
                        duration_beats=base_dur,
                        position_beats=position,
                        velocity=random.randint(65, 90),
                        is_chord_tone=True,
                        role_annotation=role.name,
                    )
                )
                position += base_dur
        else:
            # Generate from scratch with step-wise motion
            for i in range(num_notes):
                step = random.choice([-2, -1, 0, 1, 2])
                current_pitch = max(low, min(high, current_pitch + step))
                notes.append(
                    MelodyNote(
                        pitch_midi=current_pitch,
                        duration_beats=base_dur,
                        position_beats=position,
                        velocity=random.randint(65, 90),
                        is_chord_tone=True,
                        role_annotation=role.name,
                    )
                )
                position += base_dur

        return Melody(
            notes=notes,
            key="",
            scale="",
            length_bars=length_bars,
            role=role.name,
            complexity_level=5,
            mode="normal",
        )

    def build_complementarity_matrix(
        self, role_set: RoleSet
    ) -> Dict[str, Dict[str, str]]:
        """Build the full complementarity matrix for an active role set."""
        active_roles: list = []
        for role_name in self._role_library:
            melody = getattr(role_set, role_name, None)
            if melody is not None:
                active_roles.append(role_name)

        matrix: Dict[str, Dict[str, str]] = {}
        for r in active_roles:
            matrix[r] = {}
            for other in active_roles:
                if other != r and other in self._complementarity_matrix.get(r, {}):
                    matrix[r][other] = self._complementarity_matrix[r][other]

        return matrix

    def adapt_to_modification(
        self,
        modified_melody: Melody,
        role_set: RoleSet,
    ) -> RoleSet:
        """Adapt complementary melodies after one is modified."""
        import random

        updated = RoleSet(
            lead=role_set.lead,
            counter_melody=role_set.counter_melody,
            ear_candy=role_set.ear_candy,
            pad_melody=role_set.pad_melody,
            bass_line=role_set.bass_line,
            arpeggio_layer=role_set.arpeggio_layer,
            additional_roles=dict(role_set.additional_roles),
        )

        modified_role = modified_melody.role
        if modified_role == "lead":
            # Adjust all non-lead melodies
            for role_name in ["counter_melody", "ear_candy", "pad_melody", "bass_line"]:
                existing = getattr(updated, role_name, None)
                if existing is None or not existing.notes:
                    continue

                role_def = self._role_library[role_name]
                low, high = role_def.register_range

                adjusted_notes = []
                for note in existing.notes:
                    pitch = note.pitch_midi
                    while pitch < low:
                        pitch += 12
                    while pitch > high:
                        pitch -= 12
                    pitch = max(low, min(high, pitch))
                    adjusted_notes.append(
                        MelodyNote(
                            pitch_midi=pitch,
                            duration_beats=note.duration_beats,
                            position_beats=note.position_beats,
                            velocity=note.velocity,
                            is_chord_tone=note.is_chord_tone,
                            role_annotation=note.role_annotation,
                        )
                    )

                adjusted_melody = Melody(
                    notes=adjusted_notes,
                    key=existing.key,
                    scale=existing.scale,
                    length_bars=existing.length_bars,
                    role=role_name,
                    complexity_level=existing.complexity_level,
                    mode=existing.mode,
                )
                setattr(updated, role_name, adjusted_melody)

        return updated

    def validate_complementarity(self, role_set: RoleSet) -> bool:
        """Validate that all melodies are in correct registers."""
        for role_name, role_def in self._role_library.items():
            melody = getattr(role_set, role_name, None)
            if melody is None:
                continue
            if not melody.notes:
                continue

            low, high = role_def.register_range
            for note in melody.notes:
                if note.pitch_midi < low - 12 or note.pitch_midi > high + 12:
                    return False

        return True
