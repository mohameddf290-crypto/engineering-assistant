"""
Translation System for the Chords package.
Converts harmonic analysis data into structured creation plans.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from chords.audio_analysis import HarmonicAnalysisResult


@dataclass
class ChordCreationPlan:
    key: str = "C"
    scale: str = "major"
    length_bars: int = 8
    chord_quality_palette: List[str] = field(default_factory=list)
    scale_degree_weights: Dict[int, float] = field(default_factory=dict)
    harmonic_rhythm_blueprint: List[float] = field(default_factory=list)
    tension_strategy: str = "gradual"
    voice_leading_rules: List[str] = field(default_factory=list)
    target_emotions: List[str] = field(default_factory=list)
    preferred_extensions: List[str] = field(default_factory=list)
    borrowed_chords_allowed: bool = False
    modal_interchange_allowed: bool = False


class ChordTranslationSystem:
    """Translates analysis results and emotion descriptors into ChordCreationPlan."""

    _DEGREE_WEIGHTS_MAJOR = {1: 0.25, 2: 0.10, 3: 0.10, 4: 0.20, 5: 0.20, 6: 0.10, 7: 0.05}
    _DEGREE_WEIGHTS_MINOR = {1: 0.25, 2: 0.08, 3: 0.12, 4: 0.18, 5: 0.20, 6: 0.10, 7: 0.07}

    _QUALITY_PALETTES = {
        "major": ["maj", "min", "maj7", "m7", "dom7", "add9"],
        "minor": ["min", "m7", "m9", "maj7", "m7b5", "dim"],
        "dorian": ["min", "m7", "dom7", "m9", "maj7"],
        "mixolydian": ["maj", "dom7", "min", "sus4", "add9"],
        "phrygian": ["min", "maj", "dim", "m7"],
        "lydian": ["maj7", "maj9", "maj", "add9", "6"],
        "harmonic_minor": ["min", "dim7", "m7b5", "aug", "dom7"],
        "melodic_minor": ["min", "m9", "dom7", "m7b5"],
    }

    def translate_analysis_to_plan(self, analysis_result: HarmonicAnalysisResult) -> ChordCreationPlan:
        key = analysis_result.key
        scale = analysis_result.scale
        palette = self.build_chord_quality_palette(analysis_result)
        rhythm_map = self.map_harmonic_rhythm(analysis_result)
        tension_strategy = self.define_tension_strategy(analysis_result)
        n_chords = len(analysis_result.detected_chords) or 8
        blueprint = analysis_result.chord_durations[:n_chords] if analysis_result.chord_durations else [2.0] * n_chords
        length_bars = max(4, int(sum(blueprint) / 4)) if blueprint else 8
        deg_weights = dict(self._DEGREE_WEIGHTS_MINOR if "minor" in scale else self._DEGREE_WEIGHTS_MAJOR)
        voice_leading_rules = ["smooth_voice_leading", "avoid_parallel_fifths"]
        return ChordCreationPlan(
            key=key,
            scale=scale,
            length_bars=length_bars,
            chord_quality_palette=palette,
            scale_degree_weights=deg_weights,
            harmonic_rhythm_blueprint=blueprint,
            tension_strategy=tension_strategy,
            voice_leading_rules=voice_leading_rules,
            target_emotions=[],
            preferred_extensions=["maj7", "9"] if scale == "major" else ["m7", "9"],
            borrowed_chords_allowed=len(analysis_result.modulation_markers) > 0,
            modal_interchange_allowed=False,
        )

    def translate_analysis(self, analysis_result: HarmonicAnalysisResult) -> ChordCreationPlan:
        return self.translate_analysis_to_plan(analysis_result)

    def build_chord_quality_palette(self, analysis_result: HarmonicAnalysisResult) -> List[str]:
        scale = analysis_result.scale
        return list(self._QUALITY_PALETTES.get(scale, self._QUALITY_PALETTES["major"]))

    def map_harmonic_rhythm(self, analysis_result: HarmonicAnalysisResult) -> Dict[str, float]:
        avg = analysis_result.harmonic_rhythm or 2.0
        return {"average": avg, "min": avg * 0.5, "max": avg * 2.0}

    def define_tension_strategy(self, analysis_result: HarmonicAnalysisResult) -> str:
        n_tension = len(analysis_result.tension_points)
        n_chords = max(1, len(analysis_result.detected_chords))
        ratio = n_tension / n_chords
        if ratio > 0.5:
            return "high_tension"
        elif ratio > 0.25:
            return "gradual"
        else:
            return "relaxed"

    def plan_from_emotion(self, emotion_descriptors: List[Dict]) -> ChordCreationPlan:
        if not emotion_descriptors:
            return ChordCreationPlan()
        primary = emotion_descriptors[0]
        palette = primary.get("harmonic_qualities", ["maj7", "m7", "dom7"])
        scale = primary.get("preferred_mode", "major")
        tension = primary.get("tension_level", 5)
        strategy = "high_tension" if tension > 7 else ("gradual" if tension > 4 else "relaxed")
        deg_weights = primary.get("preferred_scale_degrees", dict(self._DEGREE_WEIGHTS_MAJOR))
        blueprint = [2.0] * 8
        return ChordCreationPlan(
            key="C",
            scale=scale,
            length_bars=8,
            chord_quality_palette=list(palette),
            scale_degree_weights=dict(deg_weights),
            harmonic_rhythm_blueprint=blueprint,
            tension_strategy=strategy,
            voice_leading_rules=["smooth_voice_leading"],
            target_emotions=[primary.get("name", "unknown")],
            preferred_extensions=list(primary.get("preferred_extensions", [])),
            borrowed_chords_allowed=primary.get("borrowed_chords_allowed", False),
            modal_interchange_allowed=primary.get("modal_interchange_allowed", False),
        )

    def plan_from_prompt_mapping(self, prompt_mapping: Dict) -> ChordCreationPlan:
        emotions = prompt_mapping.get("emotions", {})
        if not emotions:
            return ChordCreationPlan()
        scale = prompt_mapping.get("scale", "major")
        key = prompt_mapping.get("key", "C")
        palette = self._QUALITY_PALETTES.get(scale, self._QUALITY_PALETTES["major"])
        return ChordCreationPlan(
            key=key,
            scale=scale,
            length_bars=prompt_mapping.get("length_bars", 8),
            chord_quality_palette=list(palette),
            scale_degree_weights=dict(self._DEGREE_WEIGHTS_MAJOR),
            harmonic_rhythm_blueprint=[2.0] * 8,
            tension_strategy="gradual",
            voice_leading_rules=["smooth_voice_leading"],
            target_emotions=list(emotions.keys()),
            preferred_extensions=["maj7", "9"],
            borrowed_chords_allowed=False,
            modal_interchange_allowed=False,
        )
