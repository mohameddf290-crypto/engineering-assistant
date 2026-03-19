"""
OPERATING SYSTEM BRAIN: Emotion Description System
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

Purpose: Contains deep, profound, accurate descriptions of simple and complex
emotions — written WITHOUT AI lenses, embedded directly in the brain. Can
create chords for any single emotion or any combination.

Default AI thinking maps "sad = minor chords." That is a caricature of emotion,
not a description of it. This brain contains a full emotion taxonomy where every
emotion has precise musical correlates: specific chord qualities, voicing
densities, harmonic rhythms, tension profiles, resolution tendencies, and
extension vocabularies that accurately capture what that emotion *feels* like
harmonically — not what a simplified model says it should sound like.

Blended emotions are not averaged. "Nostalgia + power" is not "somewhat sad +
somewhat loud." It is its own thing, and this brain has an embedded description
of exactly what that blend sounds like harmonically. The weighting system
respects the primacy of each emotion in the blend without flattening either.

Protocols:
  1. Every emotion has an embedded harmonic descriptor: specific chord qualities,
     extensions, voice leading tendencies, rhythm profiles, tension level, and
     resolution tendency. Nothing is vague.
  2. Blended emotions are resolved through a weighting system, not averaging.
     Each emotion contributes its full character at its weighted proportion.
  3. Complex emotions (nostalgia + power, melancholy + beauty, tension + release)
     have their own dedicated mappings — they are not computed from simpler ones.
"""

# TODO: Design this brain with Cursor — build the full emotion taxonomy:
# every emotion (including complex blends) as an EmotionDescriptor with
# precise harmonic, rhythmic, and tension parameters. Define the weighting
# system for blends. Document the musical reasoning behind every mapping.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from chords.translation import ChordCreationPlan


@dataclass
class EmotionDescriptor:
    """
    A precise harmonic descriptor for a single emotion.

    Attributes:
        name: Emotion label (e.g. "melancholy", "power", "nostalgia").
        harmonic_qualities: Chord qualities most strongly associated with this emotion.
        preferred_extensions: Extensions that reinforce this emotion's character.
        voice_leading_tendency: Characteristic voice leading pattern (e.g. "descending chromatic").
        harmonic_rhythm_profile: Typical chord duration tendencies for this emotion.
        tension_level: Tension level on a 1–10 scale.
        resolution_tendency: How strongly the emotion tends toward resolution ("strong", "weak", "ambiguous").
        blend_compatible_with: List of emotions that blend naturally with this one.
    """

    name: str
    harmonic_qualities: List[str] = field(default_factory=list)
    preferred_extensions: List[str] = field(default_factory=list)
    voice_leading_tendency: str = ""
    harmonic_rhythm_profile: Dict[str, float] = field(default_factory=dict)
    tension_level: int = 5
    resolution_tendency: str = "ambiguous"
    blend_compatible_with: List[str] = field(default_factory=list)


class EmotionDescriptionSystem:
    """
    Brain 5 — Emotion Description System.

    Holds the full emotion taxonomy and provides translation to chord
    creation plans for any single emotion or blended emotion combination.
    """

    def __init__(self) -> None:
        self._emotion_library: Dict[str, EmotionDescriptor] = {}

    def get_emotion_descriptor(self, emotion_name: str) -> EmotionDescriptor:
        """
        Retrieve the precise EmotionDescriptor for a named emotion.

        TODO: Look up emotion_name in self._emotion_library. If not found,
        raise a descriptive error — do not fabricate a generic descriptor.
        The library must be populated at init from the embedded taxonomy.
        """
        raise NotImplementedError(
            "TODO: Implement emotion descriptor lookup. Library must be fully "
            "populated at init — no on-the-fly fabrication of descriptors."
        )

    def blend_emotions(
        self,
        emotion_list: List[str],
        weights: List[float],
    ) -> EmotionDescriptor:
        """
        Blend multiple emotions using the weighted blend system.

        Returns a composite EmotionDescriptor representing the blend.

        TODO: Implement the weighting system. Each emotion contributes its
        full harmonic character at its weighted proportion — not averaged.
        Check for dedicated complex-emotion mappings before computing a blend.
        """
        raise NotImplementedError(
            "TODO: Implement weighted emotion blending. Check for dedicated "
            "complex-emotion mappings first. Never average — always weight "
            "full character contributions."
        )

    def map_to_chord_creation_plan(
        self, emotion_descriptor: EmotionDescriptor
    ) -> ChordCreationPlan:
        """
        Convert an EmotionDescriptor to a ChordCreationPlan.

        TODO: Translate all EmotionDescriptor fields to specific ChordCreationPlan
        parameters: harmonic_qualities → chord_quality_palette, tension_level →
        tension_strategy, voice_leading_tendency → voice_leading_rules, etc.
        """
        raise NotImplementedError(
            "TODO: Implement emotion-to-creation-plan translation. Every field "
            "in EmotionDescriptor maps to specific plan parameters."
        )

    def resolve_emotion_conflicts(
        self, emotion_list: List[str]
    ) -> List[str]:
        """
        Resolve any conflicts in a list of emotions before blending.

        Returns a cleaned, conflict-resolved emotion list.

        TODO: Identify contradictory emotions (e.g. "serene" + "frantic"),
        apply resolution rules (one dominates, or a mediating third emotion
        is introduced), and return a coherent list for blending.
        """
        raise NotImplementedError(
            "TODO: Implement emotion conflict resolution. Contradictory emotions "
            "must be resolved with explicit rules, not silently discarded."
        )

    def get_all_emotions(self) -> List[str]:
        """
        Return the full list of emotion names in the taxonomy.

        TODO: Return all keys from self._emotion_library, including all
        complex blend emotions that have dedicated mappings.
        """
        raise NotImplementedError(
            "TODO: Implement get_all_emotions. Return the complete taxonomy "
            "including complex blend emotions."
        )
