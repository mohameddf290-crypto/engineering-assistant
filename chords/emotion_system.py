"""
Emotion Description System for the Chords package.
Maps emotional concepts to musical parameters.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from chords.translation import ChordCreationPlan


@dataclass
class EmotionDescriptor:
    name: str = "neutral"
    preferred_scale_degrees: Dict[int, float] = field(default_factory=dict)
    harmonic_qualities: List[str] = field(default_factory=list)
    preferred_extensions: List[str] = field(default_factory=list)
    tension_level: float = 5.0
    preferred_mode: str = "major"
    preferred_rhythm: str = "medium"
    voice_leading_tendency: str = "smooth"
    borrowed_chords_allowed: bool = False
    modal_interchange_allowed: bool = False


_EMOTION_REGISTRY: Dict[str, EmotionDescriptor] = {
    "nostalgia": EmotionDescriptor(
        name="nostalgia",
        preferred_scale_degrees={1: 0.25, 4: 0.25, 6: 0.25, 2: 0.15, 5: 0.10},
        harmonic_qualities=["maj7", "m7", "add9", "6"],
        preferred_extensions=["maj7", "add9"],
        tension_level=4.0,
        preferred_mode="major",
        preferred_rhythm="medium",
        voice_leading_tendency="descending",
        borrowed_chords_allowed=True,
        modal_interchange_allowed=True,
    ),
    "excitement": EmotionDescriptor(
        name="excitement",
        preferred_scale_degrees={1: 0.20, 4: 0.20, 5: 0.30, 2: 0.15, 7: 0.15},
        harmonic_qualities=["dom7", "sus4", "maj", "aug"],
        preferred_extensions=["dom7", "sus4"],
        tension_level=7.0,
        preferred_mode="mixolydian",
        preferred_rhythm="fast",
        voice_leading_tendency="ascending",
        borrowed_chords_allowed=True,
        modal_interchange_allowed=False,
    ),
    "melancholy": EmotionDescriptor(
        name="melancholy",
        preferred_scale_degrees={1: 0.30, 4: 0.20, 6: 0.20, 2: 0.15, 5: 0.15},
        harmonic_qualities=["m7", "m9", "m7b5", "min"],
        preferred_extensions=["m7", "m9"],
        tension_level=5.0,
        preferred_mode="minor",
        preferred_rhythm="slow",
        voice_leading_tendency="descending",
        borrowed_chords_allowed=False,
        modal_interchange_allowed=False,
    ),
    "power": EmotionDescriptor(
        name="power",
        preferred_scale_degrees={1: 0.35, 5: 0.30, 4: 0.20, 2: 0.15},
        harmonic_qualities=["dom7", "maj", "aug"],
        preferred_extensions=["dom7"],
        tension_level=8.0,
        preferred_mode="mixolydian",
        preferred_rhythm="medium",
        voice_leading_tendency="static",
        borrowed_chords_allowed=True,
        modal_interchange_allowed=False,
    ),
    "serenity": EmotionDescriptor(
        name="serenity",
        preferred_scale_degrees={1: 0.35, 4: 0.25, 2: 0.20, 6: 0.20},
        harmonic_qualities=["maj7", "maj9", "add9"],
        preferred_extensions=["maj7", "maj9"],
        tension_level=2.0,
        preferred_mode="lydian",
        preferred_rhythm="slow",
        voice_leading_tendency="static",
        borrowed_chords_allowed=False,
        modal_interchange_allowed=False,
    ),
    "tension": EmotionDescriptor(
        name="tension",
        preferred_scale_degrees={5: 0.30, 7: 0.25, 2: 0.25, 1: 0.20},
        harmonic_qualities=["dim7", "m7b5", "aug", "dom7"],
        preferred_extensions=["dim7", "m7b5"],
        tension_level=9.0,
        preferred_mode="harmonic_minor",
        preferred_rhythm="medium",
        voice_leading_tendency="chromatic",
        borrowed_chords_allowed=True,
        modal_interchange_allowed=True,
    ),
    "euphoria": EmotionDescriptor(
        name="euphoria",
        preferred_scale_degrees={1: 0.30, 4: 0.25, 5: 0.25, 2: 0.20},
        harmonic_qualities=["maj7", "6", "add9", "maj9"],
        preferred_extensions=["maj7", "add9"],
        tension_level=5.0,
        preferred_mode="major",
        preferred_rhythm="fast",
        voice_leading_tendency="ascending",
        borrowed_chords_allowed=False,
        modal_interchange_allowed=True,
    ),
    "longing": EmotionDescriptor(
        name="longing",
        preferred_scale_degrees={1: 0.25, 4: 0.20, 2: 0.25, 6: 0.20, 5: 0.10},
        harmonic_qualities=["m7", "maj7", "sus2"],
        preferred_extensions=["m7", "sus2"],
        tension_level=6.0,
        preferred_mode="dorian",
        preferred_rhythm="slow",
        voice_leading_tendency="ascending_then_descending",
        borrowed_chords_allowed=True,
        modal_interchange_allowed=True,
    ),
    "aggression": EmotionDescriptor(
        name="aggression",
        preferred_scale_degrees={1: 0.30, 5: 0.25, 7: 0.25, 2: 0.20},
        harmonic_qualities=["dim7", "dom7", "aug"],
        preferred_extensions=["dim7", "dom7"],
        tension_level=9.0,
        preferred_mode="phrygian",
        preferred_rhythm="fast",
        voice_leading_tendency="ascending",
        borrowed_chords_allowed=True,
        modal_interchange_allowed=False,
    ),
    "hope": EmotionDescriptor(
        name="hope",
        preferred_scale_degrees={1: 0.30, 4: 0.25, 5: 0.25, 2: 0.20},
        harmonic_qualities=["maj7", "sus2", "add9"],
        preferred_extensions=["maj7", "sus2"],
        tension_level=4.0,
        preferred_mode="major",
        preferred_rhythm="medium",
        voice_leading_tendency="ascending",
        borrowed_chords_allowed=False,
        modal_interchange_allowed=False,
    ),
    "mystery": EmotionDescriptor(
        name="mystery",
        preferred_scale_degrees={1: 0.20, 6: 0.25, 2: 0.25, 4: 0.20, 7: 0.10},
        harmonic_qualities=["m7b5", "maj7", "sus4"],
        preferred_extensions=["m7b5", "sus4"],
        tension_level=6.0,
        preferred_mode="dorian",
        preferred_rhythm="slow",
        voice_leading_tendency="chromatic",
        borrowed_chords_allowed=True,
        modal_interchange_allowed=True,
    ),
    "joy": EmotionDescriptor(
        name="joy",
        preferred_scale_degrees={1: 0.30, 4: 0.25, 5: 0.25, 6: 0.20},
        harmonic_qualities=["maj", "6", "add9"],
        preferred_extensions=["6", "add9"],
        tension_level=3.0,
        preferred_mode="major",
        preferred_rhythm="fast",
        voice_leading_tendency="ascending",
        borrowed_chords_allowed=False,
        modal_interchange_allowed=False,
    ),
    "grief": EmotionDescriptor(
        name="grief",
        preferred_scale_degrees={1: 0.35, 4: 0.25, 6: 0.20, 2: 0.20},
        harmonic_qualities=["m9", "m7", "m7b5"],
        preferred_extensions=["m9", "m7"],
        tension_level=7.0,
        preferred_mode="minor",
        preferred_rhythm="slow",
        voice_leading_tendency="descending",
        borrowed_chords_allowed=False,
        modal_interchange_allowed=False,
    ),
    "transcendence": EmotionDescriptor(
        name="transcendence",
        preferred_scale_degrees={1: 0.30, 4: 0.25, 2: 0.25, 6: 0.20},
        harmonic_qualities=["maj7", "maj9", "maj11"],
        preferred_extensions=["maj7", "maj9", "maj11"],
        tension_level=3.0,
        preferred_mode="lydian",
        preferred_rhythm="slow",
        voice_leading_tendency="static",
        borrowed_chords_allowed=False,
        modal_interchange_allowed=True,
    ),
    "yearning": EmotionDescriptor(
        name="yearning",
        preferred_scale_degrees={1: 0.25, 4: 0.20, 2: 0.25, 6: 0.20, 5: 0.10},
        harmonic_qualities=["m9", "m7", "sus2"],
        preferred_extensions=["m9", "sus2"],
        tension_level=6.0,
        preferred_mode="dorian",
        preferred_rhythm="medium",
        voice_leading_tendency="ascending",
        borrowed_chords_allowed=True,
        modal_interchange_allowed=True,
    ),
    "defiance": EmotionDescriptor(
        name="defiance",
        preferred_scale_degrees={1: 0.35, 5: 0.30, 4: 0.20, 2: 0.15},
        harmonic_qualities=["dom7", "maj", "aug"],
        preferred_extensions=["dom7"],
        tension_level=8.0,
        preferred_mode="mixolydian",
        preferred_rhythm="fast",
        voice_leading_tendency="ascending",
        borrowed_chords_allowed=True,
        modal_interchange_allowed=False,
    ),
}


class EmotionDescriptionSystem:
    """Maps emotional concepts to musical parameters and chord creation plans."""

    def get_emotion_descriptor(self, name: str) -> EmotionDescriptor:
        name_lower = name.lower()
        if name_lower in _EMOTION_REGISTRY:
            return _EMOTION_REGISTRY[name_lower]
        return EmotionDescriptor(name=name_lower)

    def blend_emotions(self, emotion_list: List[str], weights: List[float]) -> EmotionDescriptor:
        if not emotion_list:
            return EmotionDescriptor()
        total = sum(weights) or 1.0
        norm_weights = [w / total for w in weights]
        descriptors = [self.get_emotion_descriptor(e) for e in emotion_list]

        tension = sum(d.tension_level * w for d, w in zip(descriptors, norm_weights))

        max_idx = norm_weights.index(max(norm_weights))
        preferred_mode = descriptors[max_idx].preferred_mode
        voice_leading_tendency = descriptors[max_idx].voice_leading_tendency

        _rhythm_speed = {"slow": 1, "medium": 2, "fast": 3}
        _speed_rhythm = {1: "slow", 2: "medium", 3: "fast"}
        avg_speed = sum(_rhythm_speed.get(d.preferred_rhythm, 2) * w for d, w in zip(descriptors, norm_weights))
        preferred_rhythm = _speed_rhythm[max(1, min(3, round(avg_speed)))]

        quality_scores: Dict[str, float] = {}
        for d, w in zip(descriptors, norm_weights):
            for q in d.harmonic_qualities:
                quality_scores[q] = quality_scores.get(q, 0.0) + w
        sorted_qualities = sorted(quality_scores, key=quality_scores.get, reverse=True)
        harmonic_qualities = sorted_qualities[:4]

        ext_scores: Dict[str, float] = {}
        for d, w in zip(descriptors, norm_weights):
            for e in d.preferred_extensions:
                ext_scores[e] = ext_scores.get(e, 0.0) + w
        preferred_extensions = sorted(ext_scores, key=ext_scores.get, reverse=True)[:3]

        all_degrees = set()
        for d in descriptors:
            all_degrees.update(d.preferred_scale_degrees.keys())
        blended_degrees: Dict[int, float] = {}
        for deg in all_degrees:
            blended_degrees[deg] = sum(
                d.preferred_scale_degrees.get(deg, 0.0) * w for d, w in zip(descriptors, norm_weights)
            )
        deg_total = sum(blended_degrees.values()) or 1.0
        blended_degrees = {k: v / deg_total for k, v in blended_degrees.items()}

        borrowed = any(
            d.borrowed_chords_allowed and w > 0.3 for d, w in zip(descriptors, norm_weights)
        )
        modal = any(
            d.modal_interchange_allowed and w > 0.3 for d, w in zip(descriptors, norm_weights)
        )

        blended_name = "+".join(emotion_list)
        return EmotionDescriptor(
            name=blended_name,
            preferred_scale_degrees=blended_degrees,
            harmonic_qualities=harmonic_qualities,
            preferred_extensions=preferred_extensions,
            tension_level=tension,
            preferred_mode=preferred_mode,
            preferred_rhythm=preferred_rhythm,
            voice_leading_tendency=voice_leading_tendency,
            borrowed_chords_allowed=borrowed,
            modal_interchange_allowed=modal,
        )

    def map_to_chord_creation_plan(self, descriptor: EmotionDescriptor) -> ChordCreationPlan:
        tension = descriptor.tension_level
        if tension >= 8:
            tension_strategy = "high_tension"
        elif tension >= 5:
            tension_strategy = "gradual"
        else:
            tension_strategy = "relaxed"

        _rhythm_speed = {"slow": 1, "medium": 2, "fast": 3}
        speed = _rhythm_speed.get(descriptor.preferred_rhythm, 2)
        base_duration = 4.0 / speed
        num_chords = 8
        blueprint = [base_duration] * num_chords

        voice_leading_rules = ["smooth_voice_leading"]
        tendency = descriptor.voice_leading_tendency
        if "descend" in tendency:
            voice_leading_rules.append("prefer_descending")
        elif "ascend" in tendency:
            voice_leading_rules.append("prefer_ascending")
        elif "chromatic" in tendency:
            voice_leading_rules.append("chromatic_motion_allowed")

        return ChordCreationPlan(
            key="C",
            scale=descriptor.preferred_mode,
            length_bars=8,
            chord_quality_palette=list(descriptor.harmonic_qualities),
            scale_degree_weights=dict(descriptor.preferred_scale_degrees),
            harmonic_rhythm_blueprint=blueprint,
            tension_strategy=tension_strategy,
            voice_leading_rules=voice_leading_rules,
            target_emotions=[descriptor.name],
            preferred_extensions=list(descriptor.preferred_extensions),
            borrowed_chords_allowed=descriptor.borrowed_chords_allowed,
            modal_interchange_allowed=descriptor.modal_interchange_allowed,
        )

    def get_all_emotions(self) -> List[str]:
        return list(_EMOTION_REGISTRY.keys())
