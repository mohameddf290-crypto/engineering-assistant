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

from melodies.melody_creator import Melody
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
        self._role_library: Dict[str, MelodyRole] = {}
        self._complementarity_matrix: Dict[str, Dict[str, str]] = {}

    def get_role_definition(self, role_name: str) -> MelodyRole:
        """
        Retrieve the full definition for a melody role.

        TODO: Look up role_name in self._role_library. Raise a descriptive
        error if not found. Library must be fully populated at init — no
        on-the-fly role fabrication.
        """
        raise NotImplementedError(
            "TODO: Implement role definition lookup. Library fully populated "
            "at init — every role has precise, embedded constraints."
        )

    def generate_for_role(
        self,
        role: MelodyRole,
        creation_plan: MelodyCreationPlan,
        lead_melody: Optional[Melody],
    ) -> Melody:
        """
        Generate a melody for a specific role, with awareness of the lead melody.

        TODO: Apply role constraints (register_range, rhythmic_density,
        harmonic_priority) to the creation plan before passing to the Melody
        Creation Brain. If lead_melody is provided, use complementarity rules
        to ensure the generated melody complements it.
        """
        raise NotImplementedError(
            "TODO: Implement role-constrained melody generation. Role constraints "
            "override plan defaults. Complementarity rules are enforced when "
            "lead_melody is provided."
        )

    def build_complementarity_matrix(
        self, role_set: RoleSet
    ) -> Dict[str, Dict[str, str]]:
        """
        Build the full complementarity matrix for an active role set.

        Returns a nested dict of {role_a: {role_b: relationship_description}}.

        TODO: Populate from self._complementarity_matrix for all active role
        pairs in the role_set. This is a read from embedded definitions, not
        computed on the fly.
        """
        raise NotImplementedError(
            "TODO: Implement complementarity matrix building. Read from embedded "
            "definitions for all active role pairs in the role set."
        )

    def adapt_to_modification(
        self,
        modified_melody: Melody,
        role_set: RoleSet,
    ) -> RoleSet:
        """
        Adapt all complementary melodies in a role set after one melody is modified.

        Returns an updated RoleSet with all dependent melodies adjusted.

        TODO: Identify which roles are dependent on the modified melody via the
        complementarity matrix. Re-evaluate each dependent melody and adjust
        it to restore complementarity. Run AI Blocker on each adjusted melody.
        """
        raise NotImplementedError(
            "TODO: Implement complementarity adaptation. Identify dependent "
            "roles, re-evaluate each, and adjust to restore complementarity. "
            "AI Blocker screens every adjusted melody."
        )

    def validate_complementarity(self, role_set: RoleSet) -> bool:
        """
        Validate that all melodies in a role set are mutually complementary.

        Returns True if all role pairs pass their complementarity rules.

        TODO: For every active role pair, evaluate the complementarity rules
        from the matrix. Return True only if all pairs pass. Provide detailed
        failure information for any pair that fails.
        """
        raise NotImplementedError(
            "TODO: Implement complementarity validation. Every active role pair "
            "must pass its complementarity rules. Detailed failure reporting."
        )

    def get_all_roles(self) -> List[str]:
        """
        Return the full list of role names in the role library.

        TODO: Return all keys from self._role_library.
        """
        raise NotImplementedError(
            "TODO: Implement get_all_roles. Return the complete role taxonomy."
        )
