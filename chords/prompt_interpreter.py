"""
Prompt Interpreter for the Chords package.
Translates natural language prompts into chord creation plans.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from chords.translation import ChordCreationPlan

EMOTION_KEYWORDS: Dict[str, Dict[str, float]] = {
    "sad": {"melancholy": 0.7, "grief": 0.3},
    "happy": {"joy": 0.7, "euphoria": 0.3},
    "dark": {"melancholy": 0.5, "mystery": 0.5},
    "bright": {"joy": 0.5, "hope": 0.5},
    "nostalgic": {"nostalgia": 1.0},
    "peaceful": {"serenity": 1.0},
    "calm": {"serenity": 0.8, "melancholy": 0.2},
    "powerful": {"power": 0.7, "defiance": 0.3},
    "tense": {"tension": 0.7, "aggression": 0.3},
    "hopeful": {"hope": 0.8, "yearning": 0.2},
    "mysterious": {"mystery": 1.0},
    "joyful": {"joy": 0.8, "euphoria": 0.2},
    "melancholy": {"melancholy": 1.0},
    "excited": {"excitement": 1.0},
    "angry": {"aggression": 0.7, "defiance": 0.3},
    "longing": {"longing": 0.7, "yearning": 0.3},
    "transcendent": {"transcendence": 1.0},
    "euphoric": {"euphoria": 1.0},
    "defiant": {"defiance": 1.0},
    "serene": {"serenity": 1.0},
    "sunset": {"nostalgia": 0.5, "serenity": 0.5},
    "storm": {"aggression": 0.5, "tension": 0.5},
    "rain": {"melancholy": 0.6, "serenity": 0.4},
    "fire": {"excitement": 0.5, "aggression": 0.5},
    "ocean": {"transcendence": 0.5, "serenity": 0.5},
    "night": {"mystery": 0.6, "melancholy": 0.4},
    "dawn": {"hope": 0.6, "serenity": 0.4},
    "shadow": {"mystery": 0.6, "melancholy": 0.4},
    "light": {"joy": 0.5, "hope": 0.5},
    "dream": {"nostalgia": 0.4, "transcendence": 0.6},
    "driving": {"excitement": 0.8, "power": 0.2},
    "floating": {"serenity": 0.7, "transcendence": 0.3},
    "pulsing": {"excitement": 0.6, "tension": 0.4},
    "soaring": {"euphoria": 0.6, "transcendence": 0.4},
    "heavy": {"power": 0.5, "melancholy": 0.5},
    "slow": {"melancholy": 0.5, "serenity": 0.5},
    "fast": {"excitement": 0.6, "aggression": 0.4},
}


@dataclass
class PromptInterpretation:
    original_prompt: str = ""
    extracted_emotions: Dict[str, float] = field(default_factory=dict)
    genre_context: str = ""
    energy_level: float = 0.5
    sonic_characteristics: List[str] = field(default_factory=list)
    emotion_weights: Dict[str, float] = field(default_factory=dict)
    creation_plan: Optional[ChordCreationPlan] = None


class PromptInterpreter:
    """Translates natural language prompts into chord creation plans."""

    def interpret_prompt(self, prompt_text: str) -> PromptInterpretation:
        extracted = self.extract_emotional_content(prompt_text)
        emotion_weights = self.map_to_emotions(extracted)
        interp = PromptInterpretation(
            original_prompt=prompt_text,
            extracted_emotions=extracted,
            genre_context=extracted.get("genre", ""),
            energy_level=extracted.get("energy_level", 0.5),
            sonic_characteristics=extracted.get("characteristics", []),
            emotion_weights=emotion_weights,
        )
        interp.creation_plan = self.build_creation_plan(interp)
        return interp

    def interpret(self, prompt_text: str) -> Dict[str, Any]:
        interp = self.interpret_prompt(prompt_text)
        return {
            "emotions": interp.emotion_weights,
            "genre": interp.genre_context,
            "energy_level": interp.energy_level,
            "creation_plan": interp.creation_plan,
        }

    def extract_emotional_content(self, prompt_text: str) -> Dict[str, Any]:
        words = prompt_text.lower().split()
        words = [w.strip(".,!?;:'\"") for w in words]
        matched: Dict[str, float] = {}
        for word in words:
            if word in EMOTION_KEYWORDS:
                for emotion, weight in EMOTION_KEYWORDS[word].items():
                    matched[emotion] = matched.get(emotion, 0.0) + weight
        energy_words = {"fast", "driving", "pulsing", "excited", "powerful", "fire", "soaring"}
        calm_words = {"slow", "calm", "peaceful", "floating", "serene"}
        energy_score = sum(1 for w in words if w in energy_words)
        calm_score = sum(1 for w in words if w in calm_words)
        energy_level = 0.5 + (energy_score - calm_score) * 0.1
        energy_level = max(0.0, min(1.0, energy_level))
        return {
            "raw_scores": matched,
            "energy_level": energy_level,
            "genre": "",
            "characteristics": list(matched.keys())[:5],
        }

    def map_to_emotions(self, extracted_content: Dict) -> Dict[str, float]:
        raw = extracted_content.get("raw_scores", {})
        if not raw:
            return {"serenity": 1.0}
        total = sum(raw.values())
        if total == 0:
            return {"serenity": 1.0}
        return {k: v / total for k, v in raw.items()}

    def build_creation_plan(self, interpretation: PromptInterpretation) -> ChordCreationPlan:
        from chords.emotion_system import EmotionDescriptionSystem

        emotions = interpretation.emotion_weights
        if not emotions:
            return ChordCreationPlan()

        es = EmotionDescriptionSystem()

        emotion_names = list(emotions.keys())
        weights = [emotions[e] for e in emotion_names]

        if len(emotion_names) == 1:
            descriptor = es.get_emotion_descriptor(emotion_names[0])
        else:
            descriptor = es.blend_emotions(emotion_names, weights)

        plan = es.map_to_chord_creation_plan(descriptor)
        return plan

    def explain_mapping(self, interpretation: PromptInterpretation) -> str:
        emotions = interpretation.emotion_weights
        if not emotions:
            return f"No emotional content detected in: '{interpretation.original_prompt}'"
        top = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]
        lines = [f"Prompt: '{interpretation.original_prompt}'"]
        lines.append("Detected emotions:")
        for e, w in top:
            lines.append(f"  - {e}: {w:.2f}")
        if interpretation.creation_plan:
            lines.append(f"Key: {interpretation.creation_plan.key}, Scale: {interpretation.creation_plan.scale}")
            lines.append(f"Tension strategy: {interpretation.creation_plan.tension_strategy}")
        return "\n".join(lines)
