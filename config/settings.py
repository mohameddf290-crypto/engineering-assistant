"""
App Configuration — Engineering Assistant Music Production AI

Central configuration module for all paths, plugin directories,
analysis settings, and runtime options.
"""

import os
from pathlib import Path
from typing import List

# ── Base paths ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PRESETS_DIR = DATA_DIR / "presets"
MANUALS_DIR = DATA_DIR / "manuals"
OUTCOMES_DIR = DATA_DIR / "outcomes"
ANALYSIS_RESULTS_DIR = DATA_DIR / "analysis_results"

# ── Plugin directories ──────────────────────────────────────────────────────
# TODO: Set these to the actual plugin scan paths on the user's system.
# On Windows these are typically under C:/Program Files/VSTPlugins or
# C:/Program Files/Common Files/VST3. On macOS: /Library/Audio/Plug-Ins/.
PLUGIN_SCAN_PATHS: List[str] = [
    # "C:/Program Files/VSTPlugins",
    # "C:/Program Files/Common Files/VST3",
    # "/Library/Audio/Plug-Ins/VST",
    # "/Library/Audio/Plug-Ins/VST3",
]

# ── Essentia settings ───────────────────────────────────────────────────────
# Sample rate assumed for all audio loaded into Essentia analysis pipelines.
SAMPLE_RATE: int = 44100

# Frame and hop sizes for spectral/temporal analysis.
FRAME_SIZE: int = 2048
HOP_SIZE: int = 512

# ── FastAPI settings ────────────────────────────────────────────────────────
API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
API_PORT: int = int(os.getenv("API_PORT", "8000"))
API_RELOAD: bool = os.getenv("API_RELOAD", "true").lower() == "true"

# ── Logging ─────────────────────────────────────────────────────────────────
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# ── Outcome library ──────────────────────────────────────────────────────────
# Path to the JSON file that holds all embedded sonic outcome definitions.
OUTCOMES_DEFINITIONS_FILE = OUTCOMES_DIR / "outcome_definitions.json"

# ── Verification thresholds ──────────────────────────────────────────────────
# How close an Essentia metric must be to the target before a verification
# check is considered "passed".
VERIFICATION_TOLERANCE: float = 0.05
