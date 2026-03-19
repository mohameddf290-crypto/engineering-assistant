"""Engineering Assistant — melodies package."""

from melodies.chord_analysis import ChordAnalysisEngine
from melodies.song_analysis import SongAnalysisEngine
from melodies.translation import MelodyTranslationSystem
from melodies.melody_creator import MelodyCreationBrain
from melodies.infinity_engine import MelodyInfinityEngine
from melodies.elongation import MelodyElongationSystem
from melodies.ai_blocker import MelodyAIBlocker
from melodies.modification_engine import ModificationEngine
from melodies.role_intelligence import MelodyRoleIntelligence
from melodies.editor import MelodyEditor

__all__ = [
    "ChordAnalysisEngine",
    "SongAnalysisEngine",
    "MelodyTranslationSystem",
    "MelodyCreationBrain",
    "MelodyInfinityEngine",
    "MelodyElongationSystem",
    "MelodyAIBlocker",
    "ModificationEngine",
    "MelodyRoleIntelligence",
    "MelodyEditor",
]
