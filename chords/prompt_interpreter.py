"""
OPERATING SYSTEM BRAIN: Prompt Interpreter (Chords)
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

Purpose: Reads a text prompt, maps it to emotion combinations and sonic
characteristics, and feeds the result to the Chord Creation Brain.

Default AI thinking feeds a text prompt directly into a generation model and
produces output with no transparent reasoning — you get a result but you have
no idea why those chords were chosen, and you cannot steer the output
deliberately. This brain replaces that with a deliberate interpretation
pipeline: every prompt is parsed for emotional intent, genre context, energy
level, and sonic character. The output is a fully traceable mapping — every
chord in the final output can be traced back to specific words in the input
prompt through the Emotion Description System and Translation System.

The mapping is always explainable. The user can see exactly which words
triggered which emotions, which emotions produced which harmonic plan, and
which plan drove which chord choices. This transparency makes the tool
steerable and trustworthy.

Protocols:
  1. Every prompt is interpreted for emotional content, genre context, energy
     level, and sonic character. All four dimensions are extracted explicitly.
  2. Interpretation maps explicitly to the Emotion Description System —
     no bypassing. Every emotional word maps to a named emotion in the taxonomy.
  3. The mapping is fully explainable: every output has a traceable chain from
     prompt words → emotion labels → chord creation plan.
"""

# TODO: Design this brain with Cursor — define the full interpretation pipeline:
# NLP extraction rules for emotional content/genre/energy/sonic character,
# the mapping vocabulary from prompt words to Emotion System labels, the
# explain_mapping trace format, and edge case handling for ambiguous prompts.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from chords.translation import ChordCreationPlan


@dataclass
class PromptInterpretation:
    """
    The full interpretation of a text prompt.

    Attributes:
        original_prompt: The raw input prompt text.
        extracted_emotions: Emotion labels extracted from the prompt.
        genre_context: Detected genre context (e.g. "jazz", "cinematic", "lo-fi").
        energy_level: Detected energy level on a 1–10 scale.
        sonic_characteristics: Detected sonic character descriptors (e.g. "dark", "spacious").
        emotion_weights: Mapping of emotion label → weight (0.0–1.0, must sum to 1.0).
        creation_plan: The ChordCreationPlan produced from this interpretation.
    """

    original_prompt: str
    extracted_emotions: List[str] = field(default_factory=list)
    genre_context: str = ""
    energy_level: int = 5
    sonic_characteristics: List[str] = field(default_factory=list)
    emotion_weights: Dict[str, float] = field(default_factory=dict)
    creation_plan: Optional[ChordCreationPlan] = None


class PromptInterpreter:
    """
    Brain 6 — Prompt Interpreter (Chords).

    Translates free-text prompts into structured PromptInterpretations and
    ChordCreationPlans via the Emotion Description System.
    """

    def __init__(self) -> None:
        self._vocabulary_map: Dict[str, str] = {}

    def interpret_prompt(self, prompt_text: str) -> PromptInterpretation:
        """
        Run the full interpretation pipeline on a text prompt.

        TODO: Orchestrate extract_emotional_content → map_to_emotions →
        build_creation_plan. Return a fully populated PromptInterpretation
        with a complete creation plan and a traceable explanation.
        """
        raise NotImplementedError(
            "TODO: Implement full prompt interpretation pipeline. Every step "
            "must be traceable from prompt words to final creation plan."
        )

    def extract_emotional_content(
        self, prompt_text: str
    ) -> Dict[str, object]:
        """
        Extract emotional content, genre context, energy level, and sonic
        characteristics from a raw prompt string.

        TODO: Implement extraction logic: keyword matching, contextual inference,
        ambiguity handling. Return a structured dict with all four dimensions
        populated — incomplete extraction is not acceptable.
        """
        raise NotImplementedError(
            "TODO: Implement prompt content extraction. Extract emotions, genre, "
            "energy, and sonic character. All four dimensions must be populated."
        )

    def map_to_emotions(
        self, extracted_content: Dict[str, object]
    ) -> Dict[str, float]:
        """
        Map extracted prompt content to Emotion Description System labels
        with weights.

        Returns a dict of {emotion_name: weight} where weights sum to 1.0.

        TODO: Use the vocabulary map to translate extracted words/phrases to
        Emotion System labels. Resolve ambiguities. Assign weights based on
        emphasis and repetition in the prompt.
        """
        raise NotImplementedError(
            "TODO: Implement extracted content to emotion label mapping. "
            "Every mapping must reference a valid Emotion System label. "
            "Weights must sum to 1.0."
        )

    def build_creation_plan(
        self, interpretation: PromptInterpretation
    ) -> ChordCreationPlan:
        """
        Build a ChordCreationPlan from a populated PromptInterpretation.

        TODO: Feed the emotion labels and weights through EmotionDescriptionSystem
        and ChordTranslationSystem to produce a complete ChordCreationPlan.
        Also incorporate genre_context, energy_level, and sonic_characteristics.
        """
        raise NotImplementedError(
            "TODO: Implement creation plan building from interpretation. "
            "Feed through EmotionDescriptionSystem → ChordTranslationSystem. "
            "Genre, energy, and sonic character all influence the plan."
        )

    def explain_mapping(self, interpretation: PromptInterpretation) -> str:
        """
        Produce a human-readable explanation of the full prompt → plan mapping.

        TODO: Generate a traceable explanation string: for each prompt word →
        extracted feature → emotion label → creation plan parameter. The
        explanation must be specific enough for the user to understand and
        steer the interpretation.
        """
        raise NotImplementedError(
            "TODO: Implement mapping explanation. Must trace every prompt word "
            "through to the final creation plan parameter it influenced."
        )
