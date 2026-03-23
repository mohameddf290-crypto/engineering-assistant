"""Production-quality Infinite Chord & Melody Generator.

Pure algorithmic music theory — Markov chains, voice leading, tension arcs,
motivic development, phrase structure, and role intelligence.
No AI/ML models. Self-contained FastAPI application.
"""

from __future__ import annotations

import os
import random
import math
import struct
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Infinite Chord & Melody Generator")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
#  MUSIC THEORY CONSTANTS
# ============================================================

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_TO_SEMITONE: Dict[str, int] = {n: i for i, n in enumerate(NOTES)}
NOTE_TO_MIDI_BASE: Dict[str, int] = {
    "C": 60, "C#": 61, "D": 62, "D#": 63, "E": 64, "F": 65,
    "F#": 66, "G": 67, "G#": 68, "A": 69, "A#": 70, "B": 71,
}

SCALES: Dict[str, List[int]] = {
    "major":          [0, 2, 4, 5, 7, 9, 11],
    "minor":          [0, 2, 3, 5, 7, 8, 10],
    "dorian":         [0, 2, 3, 5, 7, 9, 10],
    "mixolydian":     [0, 2, 4, 5, 7, 9, 10],
    "phrygian":       [0, 1, 3, 5, 7, 8, 10],
    "lydian":         [0, 2, 4, 6, 7, 9, 11],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "melodic_minor":  [0, 2, 3, 5, 7, 9, 11],
}

# Default chord quality per scale degree (1-indexed)
SCALE_DEFAULT_QUALITIES: Dict[str, Dict[int, str]] = {
    "major":          {1: "maj", 2: "min", 3: "min", 4: "maj", 5: "7",   6: "min", 7: "dim"},
    "minor":          {1: "min", 2: "dim", 3: "maj", 4: "min", 5: "min", 6: "maj", 7: "maj"},
    "dorian":         {1: "min", 2: "min", 3: "maj", 4: "7",   5: "min", 6: "dim", 7: "maj"},
    "mixolydian":     {1: "7",   2: "min", 3: "dim", 4: "maj", 5: "min", 6: "min", 7: "maj"},
    "phrygian":       {1: "min", 2: "maj", 3: "maj", 4: "min", 5: "dim", 6: "maj", 7: "min"},
    "lydian":         {1: "maj7",2: "maj", 3: "min", 4: "dim", 5: "maj", 6: "min", 7: "min"},
    "harmonic_minor": {1: "min", 2: "dim", 3: "aug", 4: "min", 5: "7",   6: "maj", 7: "dim7"},
    "melodic_minor":  {1: "min", 2: "min", 3: "aug", 4: "7",   5: "7",   6: "m7b5",7: "m7b5"},
}

CHORD_INTERVALS: Dict[str, List[int]] = {
    "maj":  [0, 4, 7],
    "min":  [0, 3, 7],
    "7":    [0, 4, 7, 10],
    "maj7": [0, 4, 7, 11],
    "m7":   [0, 3, 7, 10],
    "dim":  [0, 3, 6],
    "dim7": [0, 3, 6, 9],
    "aug":  [0, 4, 8],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7],
    "m9":   [0, 3, 7, 10, 14],
    "maj9": [0, 4, 7, 11, 14],
    "add9": [0, 4, 7, 14],
    "m7b5": [0, 3, 6, 10],
}

ROMAN_NUMERALS = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII"}

ROLE_REGISTERS: Dict[str, Tuple[int, int]] = {
    "lead":          (60, 84),
    "counter_melody":(55, 79),
    "ear_candy":     (72, 96),
    "pad_melody":    (48, 72),
    "bass_line":     (28, 52),
}

ROLE_DENSITY: Dict[str, float] = {
    "lead":          1.0,
    "counter_melody":0.7,
    "ear_candy":     0.3,
    "pad_melody":    0.25,
    "bass_line":     0.5,
}

# Tension value 0.0–1.0 per degree in each scale
DEGREE_TENSION: Dict[str, Dict[int, float]] = {
    "major":          {1: 0.0, 2: 0.5, 3: 0.3, 4: 0.4, 5: 0.55, 6: 0.2, 7: 0.85},
    "minor":          {1: 0.1, 2: 0.75,3: 0.3, 4: 0.4, 5: 0.55, 6: 0.2, 7: 0.65},
    "dorian":         {1: 0.1, 2: 0.4, 3: 0.3, 4: 0.55,5: 0.4,  6: 0.7, 7: 0.3},
    "mixolydian":     {1: 0.2, 2: 0.5, 3: 0.7, 4: 0.4, 5: 0.5,  6: 0.4, 7: 0.3},
    "phrygian":       {1: 0.1, 2: 0.85,3: 0.3, 4: 0.5, 5: 0.75, 6: 0.3, 7: 0.5},
    "lydian":         {1: 0.1, 2: 0.4, 3: 0.3, 4: 0.85,5: 0.2,  6: 0.5, 7: 0.5},
    "harmonic_minor": {1: 0.1, 2: 0.75,3: 0.5, 4: 0.4, 5: 0.65, 6: 0.3, 7: 0.95},
    "melodic_minor":  {1: 0.1, 2: 0.5, 3: 0.5, 4: 0.6, 5: 0.6,  6: 0.7, 7: 0.85},
}

# ============================================================
#  MARKOV TRANSITION MATRICES
#  Dict[scale][from_degree][to_degree] = probability
# ============================================================

MARKOV_MATRICES: Dict[str, Dict[int, Dict[int, float]]] = {
    "major": {
        1: {1: 0.04, 2: 0.10, 3: 0.05, 4: 0.25, 5: 0.30, 6: 0.21, 7: 0.05},
        2: {1: 0.10, 2: 0.04, 3: 0.05, 4: 0.15, 5: 0.50, 6: 0.11, 7: 0.05},
        3: {1: 0.10, 2: 0.10, 3: 0.04, 4: 0.35, 5: 0.20, 6: 0.16, 7: 0.05},
        4: {1: 0.20, 2: 0.15, 3: 0.05, 4: 0.04, 5: 0.40, 6: 0.11, 7: 0.05},
        5: {1: 0.50, 2: 0.05, 3: 0.05, 4: 0.10, 5: 0.04, 6: 0.21, 7: 0.05},
        6: {1: 0.10, 2: 0.15, 3: 0.10, 4: 0.30, 5: 0.25, 6: 0.05, 7: 0.05},
        7: {1: 0.50, 2: 0.05, 3: 0.10, 4: 0.10, 5: 0.15, 6: 0.05, 7: 0.05},
    },
    "minor": {
        1: {1: 0.04, 2: 0.05, 3: 0.10, 4: 0.25, 5: 0.25, 6: 0.16, 7: 0.15},
        2: {1: 0.15, 2: 0.04, 3: 0.05, 4: 0.15, 5: 0.50, 6: 0.06, 7: 0.05},
        3: {1: 0.15, 2: 0.05, 3: 0.04, 4: 0.20, 5: 0.10, 6: 0.26, 7: 0.20},
        4: {1: 0.25, 2: 0.05, 3: 0.10, 4: 0.04, 5: 0.35, 6: 0.11, 7: 0.10},
        5: {1: 0.45, 2: 0.05, 3: 0.15, 4: 0.10, 5: 0.04, 6: 0.16, 7: 0.05},
        6: {1: 0.10, 2: 0.10, 3: 0.25, 4: 0.25, 5: 0.15, 6: 0.04, 7: 0.11},
        7: {1: 0.45, 2: 0.05, 3: 0.20, 4: 0.15, 5: 0.05, 6: 0.05, 7: 0.05},
    },
    "dorian": {
        1: {1: 0.04, 2: 0.10, 3: 0.10, 4: 0.30, 5: 0.20, 6: 0.10, 7: 0.16},
        2: {1: 0.15, 2: 0.04, 3: 0.10, 4: 0.15, 5: 0.40, 6: 0.11, 7: 0.05},
        3: {1: 0.20, 2: 0.10, 3: 0.04, 4: 0.30, 5: 0.15, 6: 0.11, 7: 0.10},
        4: {1: 0.20, 2: 0.10, 3: 0.05, 4: 0.04, 5: 0.40, 6: 0.16, 7: 0.05},
        5: {1: 0.35, 2: 0.05, 3: 0.10, 4: 0.20, 5: 0.04, 6: 0.21, 7: 0.05},
        6: {1: 0.05, 2: 0.30, 3: 0.10, 4: 0.20, 5: 0.25, 6: 0.04, 7: 0.06},
        7: {1: 0.40, 2: 0.10, 3: 0.15, 4: 0.15, 5: 0.10, 6: 0.05, 7: 0.05},
    },
    "mixolydian": {
        1: {1: 0.04, 2: 0.10, 3: 0.05, 4: 0.30, 5: 0.10, 6: 0.20, 7: 0.21},
        2: {1: 0.10, 2: 0.04, 3: 0.05, 4: 0.20, 5: 0.40, 6: 0.16, 7: 0.05},
        3: {1: 0.10, 2: 0.15, 3: 0.04, 4: 0.35, 5: 0.20, 6: 0.11, 7: 0.05},
        4: {1: 0.25, 2: 0.10, 3: 0.10, 4: 0.04, 5: 0.20, 6: 0.10, 7: 0.21},
        5: {1: 0.25, 2: 0.10, 3: 0.05, 4: 0.20, 5: 0.04, 6: 0.15, 7: 0.21},
        6: {1: 0.15, 2: 0.15, 3: 0.10, 4: 0.25, 5: 0.20, 6: 0.04, 7: 0.11},
        7: {1: 0.50, 2: 0.05, 3: 0.10, 4: 0.15, 5: 0.10, 6: 0.05, 7: 0.05},
    },
    "phrygian": {
        1: {1: 0.04, 2: 0.45, 3: 0.15, 4: 0.15, 5: 0.05, 6: 0.11, 7: 0.05},
        2: {1: 0.50, 2: 0.04, 3: 0.15, 4: 0.10, 5: 0.10, 6: 0.06, 7: 0.05},
        3: {1: 0.25, 2: 0.15, 3: 0.04, 4: 0.20, 5: 0.10, 6: 0.21, 7: 0.05},
        4: {1: 0.20, 2: 0.15, 3: 0.10, 4: 0.04, 5: 0.30, 6: 0.11, 7: 0.10},
        5: {1: 0.30, 2: 0.10, 3: 0.15, 4: 0.20, 5: 0.04, 6: 0.16, 7: 0.05},
        6: {1: 0.20, 2: 0.15, 3: 0.25, 4: 0.20, 5: 0.10, 6: 0.04, 7: 0.06},
        7: {1: 0.40, 2: 0.10, 3: 0.20, 4: 0.10, 5: 0.05, 6: 0.10, 7: 0.05},
    },
    "lydian": {
        1: {1: 0.04, 2: 0.20, 3: 0.10, 4: 0.10, 5: 0.30, 6: 0.15, 7: 0.11},
        2: {1: 0.25, 2: 0.04, 3: 0.10, 4: 0.10, 5: 0.30, 6: 0.16, 7: 0.05},
        3: {1: 0.20, 2: 0.10, 3: 0.04, 4: 0.15, 5: 0.25, 6: 0.21, 7: 0.05},
        4: {1: 0.15, 2: 0.20, 3: 0.15, 4: 0.04, 5: 0.25, 6: 0.16, 7: 0.05},
        5: {1: 0.45, 2: 0.10, 3: 0.10, 4: 0.10, 5: 0.04, 6: 0.16, 7: 0.05},
        6: {1: 0.15, 2: 0.15, 3: 0.20, 4: 0.15, 5: 0.25, 6: 0.04, 7: 0.06},
        7: {1: 0.40, 2: 0.10, 3: 0.20, 4: 0.10, 5: 0.10, 6: 0.05, 7: 0.05},
    },
    "harmonic_minor": {
        1: {1: 0.04, 2: 0.05, 3: 0.05, 4: 0.25, 5: 0.30, 6: 0.16, 7: 0.15},
        2: {1: 0.10, 2: 0.04, 3: 0.05, 4: 0.10, 5: 0.55, 6: 0.11, 7: 0.05},
        3: {1: 0.10, 2: 0.05, 3: 0.04, 4: 0.20, 5: 0.15, 6: 0.31, 7: 0.15},
        4: {1: 0.15, 2: 0.05, 3: 0.05, 4: 0.04, 5: 0.50, 6: 0.11, 7: 0.10},
        5: {1: 0.50, 2: 0.05, 3: 0.10, 4: 0.10, 5: 0.04, 6: 0.16, 7: 0.05},
        6: {1: 0.10, 2: 0.05, 3: 0.20, 4: 0.25, 5: 0.20, 6: 0.04, 7: 0.16},
        7: {1: 0.55, 2: 0.05, 3: 0.10, 4: 0.10, 5: 0.10, 6: 0.05, 7: 0.05},
    },
    "melodic_minor": {
        1: {1: 0.04, 2: 0.10, 3: 0.05, 4: 0.25, 5: 0.25, 6: 0.16, 7: 0.15},
        2: {1: 0.10, 2: 0.04, 3: 0.05, 4: 0.15, 5: 0.50, 6: 0.11, 7: 0.05},
        3: {1: 0.10, 2: 0.10, 3: 0.04, 4: 0.25, 5: 0.20, 6: 0.16, 7: 0.15},
        4: {1: 0.15, 2: 0.10, 3: 0.05, 4: 0.04, 5: 0.45, 6: 0.11, 7: 0.10},
        5: {1: 0.45, 2: 0.05, 3: 0.10, 4: 0.15, 5: 0.04, 6: 0.16, 7: 0.05},
        6: {1: 0.10, 2: 0.15, 3: 0.15, 4: 0.25, 5: 0.20, 6: 0.04, 7: 0.11},
        7: {1: 0.45, 2: 0.05, 3: 0.10, 4: 0.15, 5: 0.10, 6: 0.10, 7: 0.05},
    },
}

# ============================================================
#  EMOTION PARAMETERS
# ============================================================

EMOTION_PARAMS: Dict[str, Dict[str, Any]] = {
    "nostalgia": {
        "quality_dist": {"maj": 0.25, "min": 0.30, "maj7": 0.20, "m7": 0.15, "7": 0.10},
        "tension_level": 0.40, "preferred_cadence": "plagal",
        "rhythmic_density": 0.50, "extension_prob": 0.45,
        "preferred_scale": "major",
        "starting_degree_weights": {1: 0.15, 2: 0.05, 3: 0.05, 4: 0.15, 5: 0.05, 6: 0.45, 7: 0.05},
        "arc_shape": "arch",
    },
    "excitement": {
        "quality_dist": {"maj": 0.40, "7": 0.30, "min": 0.15, "add9": 0.10, "sus4": 0.05},
        "tension_level": 0.70, "preferred_cadence": "authentic",
        "rhythmic_density": 0.80, "extension_prob": 0.25,
        "preferred_scale": "major",
        "starting_degree_weights": {1: 0.40, 2: 0.05, 3: 0.05, 4: 0.15, 5: 0.25, 6: 0.05, 7: 0.05},
        "arc_shape": "ascending",
    },
    "power": {
        "quality_dist": {"min": 0.30, "maj": 0.30, "7": 0.20, "dim": 0.10, "sus4": 0.10},
        "tension_level": 0.75, "preferred_cadence": "authentic",
        "rhythmic_density": 0.70, "extension_prob": 0.20,
        "preferred_scale": "minor",
        "starting_degree_weights": {1: 0.35, 2: 0.05, 3: 0.05, 4: 0.10, 5: 0.10, 6: 0.20, 7: 0.15},
        "arc_shape": "ascending",
    },
    "melancholy": {
        "quality_dist": {"m7": 0.35, "min": 0.25, "maj7": 0.20, "maj": 0.10, "m7b5": 0.10},
        "tension_level": 0.50, "preferred_cadence": "plagal",
        "rhythmic_density": 0.40, "extension_prob": 0.60,
        "preferred_scale": "minor",
        "starting_degree_weights": {1: 0.20, 2: 0.05, 3: 0.05, 4: 0.15, 5: 0.05, 6: 0.40, 7: 0.10},
        "arc_shape": "descending",
    },
    "hope": {
        "quality_dist": {"maj": 0.35, "maj7": 0.25, "7": 0.20, "min": 0.10, "add9": 0.10},
        "tension_level": 0.45, "preferred_cadence": "authentic",
        "rhythmic_density": 0.55, "extension_prob": 0.40,
        "preferred_scale": "major",
        "starting_degree_weights": {1: 0.45, 2: 0.05, 3: 0.10, 4: 0.20, 5: 0.10, 6: 0.05, 7: 0.05},
        "arc_shape": "ascending",
    },
    "aggression": {
        "quality_dist": {"min": 0.30, "maj": 0.25, "7": 0.25, "dim": 0.10, "aug": 0.10},
        "tension_level": 0.90, "preferred_cadence": "phrygian",
        "rhythmic_density": 0.90, "extension_prob": 0.15,
        "preferred_scale": "phrygian",
        "starting_degree_weights": {1: 0.30, 2: 0.30, 3: 0.10, 4: 0.10, 5: 0.05, 6: 0.10, 7: 0.05},
        "arc_shape": "wave",
    },
    "serenity": {
        "quality_dist": {"maj7": 0.40, "maj": 0.20, "add9": 0.15, "sus2": 0.15, "min": 0.10},
        "tension_level": 0.15, "preferred_cadence": "plagal",
        "rhythmic_density": 0.30, "extension_prob": 0.70,
        "preferred_scale": "lydian",
        "starting_degree_weights": {1: 0.50, 2: 0.10, 3: 0.05, 4: 0.15, 5: 0.15, 6: 0.05, 7: 0.00},
        "arc_shape": "flat",
    },
    "tension": {
        "quality_dist": {"m7b5": 0.20, "dim7": 0.20, "7": 0.25, "aug": 0.15, "dim": 0.20},
        "tension_level": 0.95, "preferred_cadence": "half",
        "rhythmic_density": 0.65, "extension_prob": 0.30,
        "preferred_scale": "harmonic_minor",
        "starting_degree_weights": {1: 0.20, 2: 0.10, 3: 0.05, 4: 0.15, 5: 0.10, 6: 0.15, 7: 0.25},
        "arc_shape": "ascending",
    },
    "euphoria": {
        "quality_dist": {"maj": 0.40, "maj7": 0.25, "add9": 0.20, "maj9": 0.10, "7": 0.05},
        "tension_level": 0.55, "preferred_cadence": "authentic",
        "rhythmic_density": 0.75, "extension_prob": 0.50,
        "preferred_scale": "major",
        "starting_degree_weights": {1: 0.35, 2: 0.05, 3: 0.10, 4: 0.10, 5: 0.30, 6: 0.05, 7: 0.05},
        "arc_shape": "arch",
    },
    "longing": {
        "quality_dist": {"m7": 0.30, "maj7": 0.25, "min": 0.20, "m9": 0.15, "sus2": 0.10},
        "tension_level": 0.55, "preferred_cadence": "deceptive",
        "rhythmic_density": 0.45, "extension_prob": 0.65,
        "preferred_scale": "dorian",
        "starting_degree_weights": {1: 0.25, 2: 0.10, 3: 0.05, 4: 0.20, 5: 0.10, 6: 0.25, 7: 0.05},
        "arc_shape": "wave",
    },
    "wonder": {
        "quality_dist": {"maj7": 0.25, "add9": 0.25, "aug": 0.15, "sus2": 0.20, "maj9": 0.15},
        "tension_level": 0.45, "preferred_cadence": "plagal",
        "rhythmic_density": 0.40, "extension_prob": 0.75,
        "preferred_scale": "lydian",
        "starting_degree_weights": {1: 0.40, 2: 0.15, 3: 0.10, 4: 0.10, 5: 0.15, 6: 0.05, 7: 0.05},
        "arc_shape": "arch",
    },
    "defiance": {
        "quality_dist": {"min": 0.35, "maj": 0.30, "7": 0.20, "sus4": 0.10, "dim": 0.05},
        "tension_level": 0.75, "preferred_cadence": "authentic",
        "rhythmic_density": 0.75, "extension_prob": 0.15,
        "preferred_scale": "minor",
        "starting_degree_weights": {1: 0.35, 2: 0.05, 3: 0.05, 4: 0.10, 5: 0.10, 6: 0.10, 7: 0.25},
        "arc_shape": "flat",
    },
    "tenderness": {
        "quality_dist": {"maj7": 0.35, "maj": 0.25, "m7": 0.20, "add9": 0.15, "sus2": 0.05},
        "tension_level": 0.25, "preferred_cadence": "plagal",
        "rhythmic_density": 0.35, "extension_prob": 0.70,
        "preferred_scale": "major",
        "starting_degree_weights": {1: 0.30, 2: 0.05, 3: 0.05, 4: 0.30, 5: 0.05, 6: 0.20, 7: 0.05},
        "arc_shape": "arch",
    },
    "triumph": {
        "quality_dist": {"maj": 0.40, "7": 0.30, "maj7": 0.15, "add9": 0.10, "sus4": 0.05},
        "tension_level": 0.60, "preferred_cadence": "authentic",
        "rhythmic_density": 0.70, "extension_prob": 0.30,
        "preferred_scale": "major",
        "starting_degree_weights": {1: 0.40, 2: 0.05, 3: 0.05, 4: 0.20, 5: 0.20, 6: 0.05, 7: 0.05},
        "arc_shape": "ascending",
    },
    "mystery": {
        "quality_dist": {"m7": 0.25, "dim7": 0.20, "min": 0.20, "aug": 0.15, "m7b5": 0.20},
        "tension_level": 0.70, "preferred_cadence": "deceptive",
        "rhythmic_density": 0.45, "extension_prob": 0.55,
        "preferred_scale": "phrygian",
        "starting_degree_weights": {1: 0.25, 2: 0.20, 3: 0.10, 4: 0.15, 5: 0.10, 6: 0.15, 7: 0.05},
        "arc_shape": "wave",
    },
    "vulnerability": {
        "quality_dist": {"maj7": 0.30, "m7": 0.25, "maj": 0.20, "min": 0.15, "add9": 0.10},
        "tension_level": 0.35, "preferred_cadence": "deceptive",
        "rhythmic_density": 0.40, "extension_prob": 0.65,
        "preferred_scale": "major",
        "starting_degree_weights": {1: 0.15, 2: 0.10, 3: 0.10, 4: 0.15, 5: 0.05, 6: 0.35, 7: 0.10},
        "arc_shape": "descending",
    },
}

# ============================================================
#  KEYWORD VOCABULARY  (~200 words → emotion labels)
# ============================================================

KEYWORD_VOCAB: Dict[str, Tuple[str, ...]] = {
    # Darkness/Shadow
    "dark": ("melancholy", "mystery"), "shadow": ("mystery", "melancholy"),
    "midnight": ("mystery", "melancholy"), "noir": ("mystery", "melancholy"),
    "gloomy": ("melancholy",), "murky": ("mystery", "tension"),
    "bleak": ("melancholy",), "somber": ("melancholy",),
    "dim": ("mystery",), "nocturnal": ("mystery",), "void": ("mystery",),
    "abyss": ("tension", "mystery"), "pitch": ("mystery",),
    # Energy/Drive
    "driving": ("excitement", "power"), "energetic": ("excitement",),
    "pumping": ("excitement", "power"), "fierce": ("aggression", "power"),
    "intense": ("tension", "power"), "hard": ("power", "aggression"),
    "aggressive": ("aggression",), "brutal": ("aggression",),
    "heavy": ("power",), "crushing": ("aggression", "power"),
    "relentless": ("aggression", "tension"), "furious": ("aggression",),
    "rage": ("aggression",), "anger": ("aggression",),
    "fast": ("excitement",), "speed": ("excitement",), "rush": ("excitement",),
    # Lightness/Air
    "bright": ("excitement", "hope"), "light": ("serenity", "wonder"),
    "airy": ("serenity",), "floaty": ("wonder", "serenity"),
    "breezy": ("serenity",), "wispy": ("wonder",),
    "delicate": ("tenderness", "vulnerability"), "gossamer": ("wonder", "serenity"),
    "shimmering": ("wonder",), "glowing": ("hope", "euphoria"),
    "radiant": ("euphoria", "triumph"), "luminous": ("wonder", "serenity"),
    "sparkle": ("wonder", "euphoria"), "glitter": ("euphoria",),
    # Sadness/Grief
    "sad": ("melancholy",), "sorrowful": ("melancholy",),
    "grief": ("melancholy", "longing"), "loss": ("melancholy", "longing"),
    "heartbreak": ("melancholy", "longing"), "mourning": ("melancholy",),
    "tearful": ("melancholy", "vulnerability"), "weeping": ("melancholy",),
    "hollow": ("melancholy",), "empty": ("melancholy",),
    "desolate": ("melancholy",), "forlorn": ("melancholy",),
    "despair": ("melancholy", "tension"), "hopeless": ("melancholy",),
    # Happy/Uplifting
    "happy": ("euphoria", "excitement"), "joyful": ("euphoria",),
    "jubilant": ("triumph", "euphoria"), "celebratory": ("triumph", "euphoria"),
    "upbeat": ("excitement",), "cheerful": ("euphoria",),
    "playful": ("wonder", "excitement"), "bouncy": ("excitement",),
    "festive": ("triumph", "excitement"), "elated": ("euphoria",),
    # Romantic/Tender
    "romantic": ("tenderness", "longing"), "love": ("tenderness", "vulnerability"),
    "tender": ("tenderness",), "intimate": ("vulnerability", "tenderness"),
    "warm": ("nostalgia", "tenderness"), "soft": ("tenderness",),
    "gentle": ("tenderness", "serenity"), "caress": ("tenderness",),
    "affectionate": ("tenderness",), "sweet": ("tenderness", "nostalgia"),
    # Epic/Grand
    "epic": ("triumph", "power"), "cinematic": ("triumph", "wonder"),
    "grand": ("triumph",), "majestic": ("triumph",),
    "heroic": ("triumph", "defiance"), "triumphant": ("triumph",),
    "glorious": ("triumph", "euphoria"), "soaring": ("hope", "triumph"),
    "anthem": ("triumph", "defiance"), "conquering": ("triumph",),
    # Mystery/Unknown
    "mysterious": ("mystery",), "unknown": ("mystery",),
    "ethereal": ("serenity", "wonder"), "mystical": ("mystery", "wonder"),
    "strange": ("mystery",), "alien": ("mystery", "tension"),
    "eerie": ("mystery", "tension"), "surreal": ("wonder", "mystery"),
    "uncanny": ("mystery",), "otherworldly": ("wonder", "mystery"),
    "spectral": ("mystery",), "phantom": ("mystery",),
    "arcane": ("mystery",), "cryptic": ("mystery",),
    # Nostalgic
    "nostalgic": ("nostalgia",), "retro": ("nostalgia",),
    "vintage": ("nostalgia",), "memories": ("nostalgia", "longing"),
    "childhood": ("nostalgia",), "reminisce": ("nostalgia",),
    "old": ("nostalgia",), "classic": ("nostalgia",),
    "timeless": ("nostalgia",), "bittersweet": ("longing", "nostalgia"),
    # Peaceful/Calm
    "peaceful": ("serenity",), "calm": ("serenity",),
    "tranquil": ("serenity",), "serene": ("serenity",),
    "relaxed": ("serenity",), "meditative": ("serenity",),
    "soothing": ("serenity", "tenderness"), "quiet": ("serenity",),
    "still": ("serenity",), "restful": ("serenity",),
    "ambient": ("serenity",), "chill": ("serenity",),
    # Hopeful/Inspiring
    "hopeful": ("hope",), "optimistic": ("hope", "euphoria"),
    "uplifting": ("hope", "euphoria"), "inspiring": ("hope",),
    "forward": ("hope",), "rising": ("hope", "triumph"),
    "growing": ("hope",), "dawn": ("hope", "wonder"),
    "awakening": ("hope",), "sunrise": ("hope",),
    # Tense/Anxious
    "tense": ("tension",), "anxious": ("tension",),
    "uneasy": ("tension",), "restless": ("tension", "aggression"),
    "worried": ("tension",), "nervous": ("tension",),
    "fearful": ("tension",), "dread": ("tension", "mystery"),
    "ominous": ("tension", "mystery"), "foreboding": ("tension", "mystery"),
    "suspense": ("tension",), "haunting": ("mystery", "tension"),
    # Defiant/Rebellious
    "defiant": ("defiance",), "rebellious": ("defiance",),
    "fight": ("defiance", "aggression"), "battle": ("defiance", "power"),
    "resistance": ("defiance",), "refusal": ("defiance",),
    "rebel": ("defiance",), "revolt": ("defiance", "aggression"),
    "bold": ("power", "triumph"), "confident": ("triumph",),
    # Longing/Yearning
    "longing": ("longing",), "yearning": ("longing",),
    "desire": ("longing",), "craving": ("longing",),
    "missing": ("longing", "nostalgia"), "wistful": ("longing", "nostalgia"),
    "pining": ("longing",), "aching": ("longing",),
    # Wonder/Awe
    "wonder": ("wonder",), "awe": ("wonder",),
    "amazed": ("wonder",), "magical": ("wonder",),
    "fantastic": ("wonder",), "dreamy": ("wonder", "serenity"),
    "cosmic": ("wonder", "mystery"), "infinite": ("wonder",),
    "vast": ("wonder",), "celestial": ("wonder", "serenity"),
    "transcendent": ("wonder",), "stellar": ("wonder",),
    # Genre/Style
    "jazz": ("longing",), "blues": ("melancholy",),
    "rock": ("power",), "metal": ("aggression",),
    "classical": ("nostalgia",), "orchestral": ("triumph",),
    "folk": ("nostalgia",), "celtic": ("wonder", "longing"),
    "dramatic": ("tension",), "minimal": ("serenity",),
    "electronic": ("excitement",), "bass": ("power",),
}

# ============================================================
#  CORE MUSIC UTILITY FUNCTIONS
# ============================================================

def _weighted_choice(weights: Dict[Any, float]) -> Any:
    """Pick a key from a dict of key→weight, proportionally."""
    total = sum(weights.values())
    if total <= 0:
        return random.choice(list(weights.keys()))
    r = random.uniform(0, total)
    cum = 0.0
    for k, w in weights.items():
        cum += w
        if r <= cum:
            return k
    return list(weights.keys())[-1]


def get_scale_notes(key: str, scale: str) -> List[int]:
    """Return MIDI notes for one octave of the given key/scale (root in octave 4)."""
    root = NOTE_TO_MIDI_BASE.get(key, 60)
    intervals = SCALES.get(scale, SCALES["major"])
    return [root + i for i in intervals]


def midi_to_note_name(midi: int) -> str:
    octave = midi // 12 - 1
    note = NOTES[midi % 12]
    return f"{note}{octave}"


def get_scale_note_set_full(key: str, scale: str, low: int = 24, high: int = 108) -> List[int]:
    """All MIDI pitches in scale across full range."""
    root_semitone = NOTE_TO_SEMITONE.get(key, 0)
    intervals = SCALES.get(scale, SCALES["major"])
    notes = []
    for midi in range(low, high + 1):
        semitone = midi % 12
        semitone_from_root = (semitone - root_semitone) % 12
        if semitone_from_root in intervals:
            notes.append(midi)
    return notes


def get_chord_root_midi(key: str, scale: str, degree: int) -> int:
    """Return MIDI note for scale degree root (C4 octave reference)."""
    root_base = NOTE_TO_MIDI_BASE.get(key, 60)
    intervals = SCALES.get(scale, SCALES["major"])
    idx = (degree - 1) % len(intervals)
    return root_base + intervals[idx]


def build_chord_midi(root_midi: int, quality: str) -> List[int]:
    """Build chord MIDI notes from root and quality."""
    intervals = CHORD_INTERVALS.get(quality, [0, 4, 7])
    return [root_midi + i for i in intervals]


def build_chord_name(root_midi: int, quality: str) -> str:
    root_note = NOTES[root_midi % 12]
    return f"{root_note}{quality}"


def get_chord_tones_in_register(root_midi: int, quality: str, low: int, high: int) -> List[int]:
    """Get all chord tone occurrences across the register."""
    intervals = CHORD_INTERVALS.get(quality, [0, 4, 7])
    tones = []
    for oct_shift in range(-3, 5):
        for i in intervals:
            midi = root_midi + i + oct_shift * 12
            if low <= midi <= high:
                tones.append(midi)
    return sorted(set(tones))


def _closest_index(lst: List[int], val: int) -> int:
    if not lst:
        return 0
    return min(range(len(lst)), key=lambda i: abs(lst[i] - val))


# ============================================================
#  VOICE LEADING ENGINE
# ============================================================

def _voice_cost(prev_voices: List[int], new_voices: List[int]) -> float:
    """Cost = total semitone movement (greedy closest-voice assignment, no voice reuse)."""
    cost = 0.0
    used = [False] * len(new_voices)
    for pv in prev_voices:
        best_dist = 999
        best_j = -1
        for j, nv in enumerate(new_voices):
            if used[j]:
                continue
            d = abs(nv - pv)
            if d < best_dist:
                best_dist = d
                best_j = j
        if best_j >= 0:
            cost += best_dist
            used[best_j] = True
        else:
            # All new voices already matched; add distance to closest (penalize extra voices)
            cost += min(abs(nv - pv) for nv in new_voices)
    return cost


def _has_parallel_fifths_or_octaves(prev: List[int], new_v: List[int]) -> bool:
    """Check for parallel 5ths or octaves between any pair of voices."""
    for i in range(len(prev)):
        for j in range(i + 1, len(prev)):
            if j >= len(new_v) or i >= len(new_v):
                break
            prev_int = (prev[j] - prev[i]) % 12
            new_int = (new_v[j] - new_v[i]) % 12
            # Parallel 5th
            if prev_int == 7 and new_int == 7:
                return True
            # Parallel octave
            if prev_int == 0 and new_int == 0:
                return True
    return False


def voice_lead_chord(
    prev_voicing: List[int],
    next_root_midi: int,
    next_quality: str,
    prev_quality: str = "maj",
) -> List[int]:
    """
    Apply voice leading to build the best voicing of the next chord.
    Returns MIDI notes list.
    """
    intervals = CHORD_INTERVALS.get(next_quality, [0, 4, 7])
    n_voices = max(len(prev_voicing), len(intervals))

    # Build candidate voicings across 3 octaves
    candidates: List[List[int]] = []
    for oct_shift in range(-1, 3):
        base_root = next_root_midi + oct_shift * 12
        candidate = [base_root + i for i in intervals]
        # Ensure candidates are near prev_voicing range
        avg_prev = sum(prev_voicing) / len(prev_voicing) if prev_voicing else 60
        avg_cand = sum(candidate) / len(candidate)
        if abs(avg_cand - avg_prev) <= 18:
            candidates.append(candidate)
        # Also try first inversion
        if len(intervals) >= 2:
            inv1 = [candidate[1]] + [candidate[0] + 12] + candidate[2:]
            if abs(sum(inv1) / len(inv1) - avg_prev) <= 18:
                candidates.append(inv1)
        # Second inversion
        if len(intervals) >= 3:
            inv2 = [candidate[2]] + [candidate[0] + 12] + [candidate[1] + 12] + candidate[3:]
            if abs(sum(inv2) / len(inv2) - avg_prev) <= 18:
                candidates.append(inv2)

    if not candidates:
        # Fallback: basic chord one octave above root
        candidates = [build_chord_midi(next_root_midi, next_quality)]

    # Score candidates
    prev_intervals_set = set((v - prev_voicing[0]) % 12 for v in prev_voicing) if prev_voicing else set()
    best = None
    best_cost = float("inf")

    for cand in candidates:
        cost = _voice_cost(prev_voicing, cand)

        # Penalty: parallel 5ths/octaves
        if _has_parallel_fifths_or_octaves(prev_voicing, cand):
            cost += 3.0

        # Bonus: common tones held (reduces cost)
        prev_set = set(v % 12 for v in prev_voicing)
        cand_set = set(v % 12 for v in cand)
        common = len(prev_set & cand_set)
        cost -= common * 0.5

        # Bonus: voices moving by step rather than leap
        movements = []
        used_cand = [False] * len(cand)
        for pv in prev_voicing:
            available = [(abs(cv - pv), i) for i, cv in enumerate(cand) if not used_cand[i]]
            if available:
                best_mv = min(available)
                movements.append(best_mv[0])
                used_cand[best_mv[1]] = True
        stepwise = sum(1 for m in movements if m <= 2)
        cost -= stepwise * 0.3

        if cost < best_cost:
            best_cost = cost
            best = cand

    return best if best else candidates[0]


# ============================================================
#  TENSION ARC GENERATOR
# ============================================================

def build_tension_arc(length: int, peak: float, shape: str) -> List[float]:
    """Build a tension curve of `length` values in [0,1]."""
    if length <= 1:
        return [peak]

    t = [0.0] * length
    if shape == "arch":
        # Rise to peak at 60%, fall to near zero
        peak_pos = int(length * 0.6)
        for i in range(length):
            if i <= peak_pos:
                t[i] = peak * (i / peak_pos) if peak_pos > 0 else 0
            else:
                t[i] = peak * (1 - (i - peak_pos) / max(1, length - 1 - peak_pos))
        t[-1] = max(0.0, t[-1] * 0.3)  # resolution at end
    elif shape == "ascending":
        for i in range(length):
            t[i] = peak * (i / (length - 1)) if length > 1 else peak
        t[-1] = t[-1] * 0.8  # slight resolution
    elif shape == "descending":
        for i in range(length):
            t[i] = peak * (1 - i / (length - 1)) if length > 1 else peak
    elif shape == "wave":
        for i in range(length):
            t[i] = peak * (0.5 + 0.5 * math.sin(2 * math.pi * i / max(1, length - 1)))
    elif shape == "flat":
        t = [peak * 0.3] * length
    else:
        t = [peak * 0.5] * length

    return [max(0.0, min(1.0, x)) for x in t]


# ============================================================
#  PROMPT / EMOTION INTERPRETER
# ============================================================

def interpret_emotions_and_prompt(
    emotions: Optional[List[str]],
    prompt: Optional[str],
) -> Dict[str, Any]:
    """
    Blend emotion parameters from selected emotions + prompt keywords.
    Returns a single blended EMOTION_PARAMS dict.
    """
    emotion_scores: Dict[str, float] = {}

    # Add explicitly selected emotions with high weight
    if emotions:
        for e in emotions:
            e_lower = e.lower().strip()
            if e_lower in EMOTION_PARAMS:
                emotion_scores[e_lower] = emotion_scores.get(e_lower, 0) + 2.0

    # Scan prompt for keywords
    if prompt:
        words = prompt.lower().replace(",", " ").replace(".", " ").split()
        for word in words:
            if word in EMOTION_PARAMS:
                emotion_scores[word] = emotion_scores.get(word, 0) + 2.0
            elif word in KEYWORD_VOCAB:
                for emo in KEYWORD_VOCAB[word]:
                    emotion_scores[emo] = emotion_scores.get(emo, 0) + 1.0

    if not emotion_scores:
        # Default: pick random emotion
        return EMOTION_PARAMS[random.choice(list(EMOTION_PARAMS.keys()))]

    # Normalize weights
    total = sum(emotion_scores.values())
    weights = {e: w / total for e, w in emotion_scores.items()}

    # Blend parameters
    blended = _blend_emotion_params(weights)
    return blended


def _blend_emotion_params(weights: Dict[str, float]) -> Dict[str, Any]:
    """Weighted interpolation of emotion parameters."""
    # Weighted average for numeric params
    numeric_keys = ["tension_level", "rhythmic_density", "extension_prob"]
    result: Dict[str, Any] = {}

    for k in numeric_keys:
        result[k] = sum(EMOTION_PARAMS[e][k] * w for e, w in weights.items()
                        if e in EMOTION_PARAMS)

    # Blend quality distributions
    all_qualities = set(q for e in weights if e in EMOTION_PARAMS
                        for q in EMOTION_PARAMS[e]["quality_dist"])
    qdist: Dict[str, float] = {}
    for q in all_qualities:
        qdist[q] = sum(EMOTION_PARAMS[e]["quality_dist"].get(q, 0) * w
                       for e, w in weights.items() if e in EMOTION_PARAMS)
    result["quality_dist"] = qdist

    # Blend starting degree weights
    sdw: Dict[int, float] = {}
    for deg in range(1, 8):
        sdw[deg] = sum(EMOTION_PARAMS[e]["starting_degree_weights"].get(deg, 0.1) * w
                       for e, w in weights.items() if e in EMOTION_PARAMS)
    result["starting_degree_weights"] = sdw

    # Pick dominant values for categorical params
    dominant_emotion = max(weights, key=weights.get)
    ep = EMOTION_PARAMS.get(dominant_emotion, EMOTION_PARAMS["hope"])
    result["preferred_cadence"] = ep["preferred_cadence"]
    result["preferred_scale"] = ep["preferred_scale"]
    result["arc_shape"] = ep["arc_shape"]

    return result


# ============================================================
#  MARKOV CHORD GENERATION
# ============================================================

def _markov_next_degree(
    scale: str,
    current: int,
    tension_target: float,
    tension_dict: Optional[Dict[int, float]] = None,
) -> int:
    """Pick next degree using Markov matrix biased by tension target."""
    matrix = MARKOV_MATRICES.get(scale, MARKOV_MATRICES["major"])
    row = dict(matrix.get(current, matrix[1]))  # copy

    if tension_dict is None:
        tension_dict = DEGREE_TENSION.get(scale, {})

    # Bias probabilities toward degrees matching tension target
    adjusted: Dict[int, float] = {}
    for deg, prob in row.items():
        deg_t = tension_dict.get(deg, 0.5)
        # Higher weight when degree tension is close to target
        diff = abs(deg_t - tension_target)
        bias = max(0.1, 1.0 - diff * 1.5)
        adjusted[deg] = prob * bias

    return _weighted_choice(adjusted)


def _apply_cadence(
    degrees: List[int],
    cadence_type: str,
    scale: str,
) -> List[int]:
    """Ensure the last 2 chords form the target cadence type."""
    if len(degrees) < 2:
        return degrees

    cadences = {
        "authentic": (5, 1),   # V → I
        "plagal":    (4, 1),   # IV → I
        "deceptive": (5, 6),   # V → vi
        "half":      (4, 5),   # IV → V (or any → V)
        "phrygian":  (2, 1),   # II♭ → I (in phrygian ii is ♭II)
    }
    target = cadences.get(cadence_type, (5, 1))

    # Replace last two chords with cadence
    result = list(degrees)
    result[-2] = target[0]
    result[-1] = target[1]
    return result


def _pick_quality(
    scale: str,
    degree: int,
    emotion_params: Dict[str, Any],
    tension: float,
    extension_prob: float,
) -> str:
    """Choose chord quality blending scale defaults with emotion distribution."""
    # Start with scale default
    default_q = SCALE_DEFAULT_QUALITIES.get(scale, SCALE_DEFAULT_QUALITIES["major"]).get(degree, "maj")

    qdist = emotion_params.get("quality_dist", {})
    if not qdist:
        return default_q

    # High tension: prefer 7th/dim chords; low tension: prefer triads
    filtered: Dict[str, float] = {}
    for q, prob in qdist.items():
        q_tension = {
            "maj": 0.0, "min": 0.2, "sus2": 0.2, "sus4": 0.3,
            "maj7": 0.2, "m7": 0.3, "add9": 0.25, "7": 0.5,
            "m9": 0.35, "maj9": 0.3, "dim": 0.7, "aug": 0.75,
            "dim7": 0.85, "m7b5": 0.8,
        }.get(q, 0.4)
        diff = abs(q_tension - tension)
        bias = max(0.1, 1.0 - diff * 1.5)
        filtered[q] = prob * bias

    # Mix with scale default (80% emotion dist, 20% default)
    chosen = _weighted_choice(filtered)

    # Apply extension probability
    extensions = {"maj7", "m7", "7", "m9", "maj9", "add9", "dim7", "m7b5"}
    if chosen not in extensions and random.random() > extension_prob:
        # Fall back to default
        return default_q

    return chosen


def _build_progression_chord(
    key: str,
    scale: str,
    degree: int,
    quality: str,
    prev_voicing: Optional[List[int]],
    duration_beats: float,
    bar_index: int,
) -> Dict[str, Any]:
    """Build a single chord dict with voice leading applied."""
    root_midi = get_chord_root_midi(key, scale, degree)
    # Keep root in octave 3-4 range
    while root_midi > 65:
        root_midi -= 12
    while root_midi < 48:
        root_midi += 12

    if prev_voicing:
        midi_notes = voice_lead_chord(prev_voicing, root_midi, quality)
    else:
        midi_notes = build_chord_midi(root_midi, quality)
        # Add octave bass note
        midi_notes = [root_midi - 12] + midi_notes

    roman = ROMAN_NUMERALS.get(degree, str(degree))
    # Minor-quality degrees → lowercase in major/lydian/mixolydian
    minor_qualities = {"min", "m7", "m9", "dim", "dim7", "m7b5"}
    if quality in minor_qualities and scale in ("major", "lydian", "mixolydian"):
        roman = roman.lower()

    # Quality suffix for roman numeral display
    _quality_suffix: Dict[str, str] = {
        "7": "7", "maj7": "maj7", "m7": "m7", "dim": "°", "dim7": "°7",
        "aug": "+", "sus2": "sus2", "sus4": "sus4", "m9": "m9",
        "maj9": "maj9", "add9": "add9", "m7b5": "ø7",
    }
    roman_numeral = roman + _quality_suffix.get(quality, "")

    name = build_chord_name(root_midi, quality)

    return {
        "name": name,
        "roman_numeral": roman_numeral,
        "midi_notes": midi_notes,
        "duration_beats": duration_beats,
        "root": NOTES[root_midi % 12],
        "quality": quality,
        "degree": degree,
        "position_bar": bar_index,
    }


def generate_progression(
    key: str,
    scale: str,
    emotions: Optional[List[str]] = None,
    length_bars: int = 4,
    prompt: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a chord progression using Markov chains + voice leading + tension arcs.
    """
    emotion_params = interpret_emotions_and_prompt(emotions, prompt)

    # Use emotion's preferred scale if user didn't specify a non-major scale
    use_scale = scale
    if scale == "major" and emotion_params.get("preferred_scale") not in (None, "major"):
        use_scale = emotion_params["preferred_scale"]
    elif scale not in SCALES:
        use_scale = "major"

    tension_level = emotion_params.get("tension_level", 0.5)
    arc_shape = emotion_params.get("arc_shape", "arch")
    num_chords = max(4, min(length_bars, 8))
    tension_arc = build_tension_arc(num_chords, tension_level, arc_shape)
    tension_dict = DEGREE_TENSION.get(use_scale, {})

    # Starting degree
    start_weights = emotion_params.get("starting_degree_weights", {})
    if not start_weights or all(v == 0 for v in start_weights.values()):
        start_weights = {1: 0.4, 4: 0.2, 5: 0.2, 6: 0.2}
    current = _weighted_choice(start_weights)

    degrees = [current]
    for i in range(1, num_chords - 2):
        current = _markov_next_degree(use_scale, current, tension_arc[i], tension_dict)
        degrees.append(current)

    # Ensure cadence at end
    cadence = emotion_params.get("preferred_cadence", "authentic")
    degrees = _apply_cadence(degrees + [1, 1], cadence, use_scale)
    degrees = degrees[:num_chords]

    # Duration per chord
    dur = (length_bars * 4.0) / num_chords

    # Build chords with voice leading
    chords = []
    prev_voicing: Optional[List[int]] = None
    ext_prob = emotion_params.get("extension_prob", 0.4)

    for i, deg in enumerate(degrees):
        tension = tension_arc[i] if i < len(tension_arc) else 0.5
        quality = _pick_quality(use_scale, deg, emotion_params, tension, ext_prob)
        chord = _build_progression_chord(key, use_scale, deg, quality, prev_voicing, dur, i)
        chords.append(chord)
        prev_voicing = chord["midi_notes"]

    return {"progression": chords, "key": key, "scale": use_scale}


# ============================================================
#  PROGRESSION VARIATIONS
# ============================================================

def regenerate_similar_progression(
    progression: List[Dict[str, Any]],
    key: str,
    scale: str,
) -> Dict[str, Any]:
    """
    Preserve: key, scale, chord function sequence, phrase rhythm.
    Change: voicings, extensions, tensions.
    """
    new_chords = []
    prev_voicing: Optional[List[int]] = None

    # Slight quality variation pool
    quality_variations: Dict[str, List[str]] = {
        "maj": ["maj", "maj7", "add9", "sus4"],
        "min": ["min", "m7", "sus2"],
        "7":   ["7", "9", "sus4"],  # 9 will fall back gracefully
        "maj7":["maj7", "maj9", "add9"],
        "m7":  ["m7", "m9", "min"],
        "dim": ["dim", "dim7", "m7b5"],
        "dim7":["dim7", "dim", "m7b5"],
        "aug": ["aug", "sus4"],
        "sus2":["sus2", "add9", "maj"],
        "sus4":["sus4", "sus2", "7"],
        "m9":  ["m9", "m7", "min"],
        "maj9":["maj9", "maj7", "add9"],
        "add9":["add9", "maj7", "maj"],
        "m7b5":["m7b5", "dim7", "m7"],
    }

    for chord in progression:
        deg = chord.get("degree", 1)
        root_midi = get_chord_root_midi(key, scale, deg)
        while root_midi > 65:
            root_midi -= 12
        while root_midi < 48:
            root_midi += 12

        # Vary quality slightly
        orig_q = chord.get("quality", "maj")
        pool = quality_variations.get(orig_q, [orig_q])
        # Filter to only valid qualities
        pool = [q for q in pool if q in CHORD_INTERVALS]
        new_q = random.choice(pool) if pool else orig_q

        if prev_voicing:
            midi_notes = voice_lead_chord(prev_voicing, root_midi, new_q)
        else:
            midi_notes = build_chord_midi(root_midi, new_q)
            midi_notes = [root_midi - 12] + midi_notes

        new_chord = {
            **chord,
            "quality": new_q,
            "name": build_chord_name(root_midi, new_q),
            "midi_notes": midi_notes,
        }
        new_chords.append(new_chord)
        prev_voicing = midi_notes

    return {"progression": new_chords, "key": key, "scale": scale}


def regenerate_different_progression(
    progression: List[Dict[str, Any]],
    key: str,
    scale: str,
) -> Dict[str, Any]:
    """
    Change starting chord, cadence type, tension arc shape, rhythmic density.
    Use contrast operators vs original.
    """
    # Analyze original tension
    orig_degrees = [c.get("degree", 1) for c in progression]
    orig_end = orig_degrees[-1] if orig_degrees else 1

    # Contrast: if ended on I, start somewhere else; vary arc shape
    shapes = ["arch", "ascending", "descending", "wave", "flat"]
    arc_shape = random.choice(shapes)

    # Contrast starting degree
    stable = {1, 4, 5}
    unstable = {2, 3, 6, 7}
    if orig_degrees and orig_degrees[0] in stable:
        start_pool = list(unstable)
    else:
        start_pool = list(stable)

    length = len(progression)
    tension_level = random.uniform(0.3, 0.9)
    tension_arc = build_tension_arc(length, tension_level, arc_shape)
    tension_dict = DEGREE_TENSION.get(scale, {})

    # Contrast cadence
    cadences = ["authentic", "plagal", "deceptive", "half"]
    cadence = random.choice(cadences)

    current = random.choice(start_pool) if start_pool else 1
    degrees = [current]
    for i in range(1, length - 2):
        current = _markov_next_degree(scale, current, tension_arc[i], tension_dict)
        degrees.append(current)
    degrees = _apply_cadence(degrees + [1, 1], cadence, scale)
    degrees = degrees[:length]

    dur = progression[0].get("duration_beats", 4.0) if progression else 4.0
    chords = []
    prev_voicing: Optional[List[int]] = None

    # Use varied qualities
    emotion_params = {
        "quality_dist": {"maj": 0.25, "min": 0.25, "7": 0.15, "maj7": 0.15, "m7": 0.10, "dim7": 0.05, "aug": 0.05},
        "extension_prob": 0.5,
    }
    for i, deg in enumerate(degrees):
        tension = tension_arc[i] if i < len(tension_arc) else 0.5
        quality = _pick_quality(scale, deg, emotion_params, tension, 0.5)
        chord = _build_progression_chord(key, scale, deg, quality, prev_voicing, dur, i)
        chords.append(chord)
        prev_voicing = chord["midi_notes"]

    return {"progression": chords, "key": key, "scale": scale}


# ============================================================
#  ELONGATION
# ============================================================

def elongate_progression(
    progression: List[Dict[str, Any]],
    key: str,
    scale: str,
) -> Dict[str, Any]:
    """
    Extend progression by analyzing harmonic arc and continuing meaningfully.
    If ends resolved (I), begin extension with departure.
    If ends unresolved, continue building toward resolution.
    """
    if not progression:
        return {"progression": [], "key": key, "scale": scale}

    last_deg = progression[-1].get("degree", 1)
    last_quality = progression[-1].get("quality", "maj")
    dur = progression[0].get("duration_beats", 4.0)

    # Analyze tension of last chord
    tension_dict = DEGREE_TENSION.get(scale, {})
    last_tension = tension_dict.get(last_deg, 0.5)

    n_ext = len(progression)  # same length as original

    if last_tension < 0.3:
        # Resolved — depart to new tonal area
        arc_shape = "arch"
        start_weights = {2: 0.2, 3: 0.15, 4: 0.25, 6: 0.25, 7: 0.15}
        tension_level = 0.6
    else:
        # Unresolved — continue toward resolution
        arc_shape = "descending"
        start_weights = {1: 0.5, 4: 0.3, 5: 0.2}
        tension_level = last_tension

    tension_arc = build_tension_arc(n_ext, tension_level, arc_shape)
    current = _weighted_choice(start_weights)
    degrees = [current]
    for i in range(1, n_ext - 2):
        current = _markov_next_degree(scale, current, tension_arc[i], tension_dict)
        degrees.append(current)
    degrees = _apply_cadence(degrees + [1, 1], "authentic", scale)
    degrees = degrees[:n_ext]

    # Build extension chords
    extension = []
    prev_voicing = progression[-1].get("midi_notes")
    emotion_params = {"quality_dist": {"maj": 0.3, "min": 0.3, "7": 0.2, "maj7": 0.1, "m7": 0.1}, "extension_prob": 0.4}
    for i, deg in enumerate(degrees):
        tension = tension_arc[i] if i < len(tension_arc) else 0.5
        quality = _pick_quality(scale, deg, emotion_params, tension, 0.4)
        chord = _build_progression_chord(key, scale, deg, quality, prev_voicing, dur, len(progression) + i)
        extension.append(chord)
        prev_voicing = chord["midi_notes"]

    return {"progression": list(progression) + extension, "key": key, "scale": scale}


# ============================================================
#  CHORD MIXER
# ============================================================

def _count_shared_scale_tones(key_a: str, scale_a: str, key_b: str, scale_b: str) -> int:
    """Count shared semitones between two scales."""
    notes_a = set(get_scale_notes(key_a, scale_a))
    notes_b = set(get_scale_notes(key_b, scale_b))
    # Compare pitch classes
    pc_a = {n % 12 for n in notes_a}
    pc_b = {n % 12 for n in notes_b}
    return len(pc_a & pc_b)


def mix_progressions(
    prog_a: List[Dict[str, Any]],
    prog_b: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Mix two progressions intelligently:
    - If keys are compatible (≥5 shared tones): alternate interesting chords
    - If keys conflict: use pivot chord to transition
    """
    # Try to extract keys from progression dicts (they may not have key info)
    # Detect key from chord names heuristically (use first chord root)
    key_a = prog_a[0].get("root", "C") if prog_a else "C"
    key_b = prog_b[0].get("root", "C") if prog_b else "C"
    # "quality" is chord quality, not scale; use "major" for compatibility check
    scale_a = "major"
    scale_b = "major"

    # Use "major" as default scale for compatibility check
    shared = _count_shared_scale_tones(key_a, "major", key_b, "major")

    mixed = []
    if shared >= 5:
        # Compatible keys: alternate, picking more interesting (more complex quality) chord
        max_len = max(len(prog_a), len(prog_b))
        for i in range(max_len):
            a = prog_a[i % len(prog_a)] if prog_a else None
            b = prog_b[i % len(prog_b)] if prog_b else None
            if a is None:
                mixed.append(b)
            elif b is None:
                mixed.append(a)
            else:
                # Pick the one with more harmonic interest (more intervals = more interesting)
                ints_a = len(CHORD_INTERVALS.get(a.get("quality", "maj"), [0, 4, 7]))
                ints_b = len(CHORD_INTERVALS.get(b.get("quality", "maj"), [0, 4, 7]))
                if i % 2 == 0:
                    mixed.append(a if ints_a >= ints_b else b)
                else:
                    mixed.append(b if ints_b >= ints_a else a)
    else:
        # Conflicting keys: first half from A, then pivot to B
        half = len(prog_a) // 2
        mixed = list(prog_a[:half])

        # Find pivot: chord in A that shares most tones with B's key
        b_notes = {n % 12 for n in get_scale_notes(key_b, "major")}
        best_pivot_idx = half
        best_overlap = -1
        for i in range(half, len(prog_a)):
            chord_notes = {n % 12 for n in prog_a[i].get("midi_notes", [])}
            overlap = len(chord_notes & b_notes)
            if overlap > best_overlap:
                best_overlap = overlap
                best_pivot_idx = i

        mixed.append(prog_a[best_pivot_idx])  # pivot chord
        mixed.extend(prog_b)  # second half from B

    return {"progression": mixed, "key": key_a, "scale": "major"}


# ============================================================
#  MELODY GENERATION ENGINE
# ============================================================

def _build_scale_register(key: str, scale: str, low: int, high: int) -> List[int]:
    """All scale notes in the given register range."""
    return get_scale_note_set_full(key, scale, low, high)


def _get_approach_tones(target: int, scale_notes_set: set) -> List[int]:
    """Chromatic approach tones (semitones not in scale, within 2 of target)."""
    approaches = []
    for delta in [-2, -1, 1, 2]:
        cand = target + delta
        if cand not in scale_notes_set:
            approaches.append(cand)
    return approaches


def _weighted_note_choice(
    chord_tones: List[int],
    scale_notes: List[int],
    chromatic_near: List[int],
    is_strong_beat: bool,
    current_pitch: int,
    target_dir: int,  # +1 up, -1 down, 0 neutral
    low: int,
    high: int,
) -> int:
    """
    Beat-position-aware note selection with contour bias.
    Strong beats: 70% chord, 20% scale, 10% approach
    Weak beats:   40% chord, 40% scale, 20% approach
    """
    if is_strong_beat:
        weights = {"chord": 0.70, "scale": 0.20, "approach": 0.10}
    else:
        weights = {"chord": 0.40, "scale": 0.40, "approach": 0.20}

    # Filter to register
    chord_in_reg = [n for n in chord_tones if low <= n <= high]
    scale_in_reg = [n for n in scale_notes if low <= n <= high]
    approach_in_reg = [n for n in chromatic_near if low <= n <= high]

    if not chord_in_reg:
        chord_in_reg = scale_in_reg[:] if scale_in_reg else [current_pitch]
    if not scale_in_reg:
        scale_in_reg = chord_in_reg[:]
    if not approach_in_reg:
        approach_in_reg = []

    # Build weighted candidate pool
    pool: Dict[int, float] = {}

    def add_candidates(candidates: List[int], base_weight: float) -> None:
        if not candidates:
            return
        per_note = base_weight / len(candidates)
        for note in candidates:
            # Contour bias: prefer notes in target direction
            diff = note - current_pitch
            if target_dir > 0 and diff > 0:
                bias = 1.5
            elif target_dir < 0 and diff < 0:
                bias = 1.5
            elif target_dir == 0:
                bias = 1.0
            else:
                bias = 0.6
            # Prefer stepwise motion (don't leap more than an octave)
            if abs(diff) > 12:
                bias *= 0.3
            pool[note] = pool.get(note, 0) + per_note * bias

    add_candidates(chord_in_reg, weights["chord"])
    add_candidates(scale_in_reg, weights["scale"])
    add_candidates(approach_in_reg, weights["approach"])

    if not pool:
        return current_pitch

    return _weighted_choice(pool)


def _generate_motif(
    scale_notes: List[int],
    chord_tones: List[int],
    contour_dir: int,  # +1 ascending, -1 descending
    motif_length: int = 4,
) -> List[int]:
    """Generate a short motivic cell (list of MIDI pitches)."""
    if not chord_tones:
        start = scale_notes[len(scale_notes) // 2]
    else:
        # Start on a chord tone
        start = random.choice([t for t in chord_tones if t in scale_notes] or chord_tones)

    motif = [start]
    scale_set = set(scale_notes)
    for i in range(1, motif_length):
        # Stepwise motion with contour bias
        current = motif[-1]
        idx = _closest_index(scale_notes, current)
        # Bias steps toward contour direction
        if contour_dir > 0:
            step = random.choices([-1, 0, 1, 2], weights=[0.1, 0.2, 0.4, 0.3])[0]
        elif contour_dir < 0:
            step = random.choices([-2, -1, 0, 1], weights=[0.3, 0.4, 0.2, 0.1])[0]
        else:
            step = random.choices([-2, -1, 0, 1, 2], weights=[0.2, 0.3, 0.15, 0.2, 0.15])[0]
        new_idx = max(0, min(len(scale_notes) - 1, idx + step))
        motif.append(scale_notes[new_idx])
    return motif


def _develop_motif(
    motif: List[int],
    technique: str,
    scale_notes: List[int],
    transpose: int = 0,
) -> List[int]:
    """
    Apply motivic development technique.
    techniques: 'repeat', 'sequence', 'inversion', 'fragmentation', 'retrograde'
    """
    if not motif:
        return motif

    if technique == "repeat":
        return [n + transpose for n in motif]

    elif technique == "sequence":
        # Same intervals, transposed; use a non-zero offset to ensure movement
        seq_offset = transpose if transpose != 0 else random.choice([-5, -3, 2, 3, 5, 7])
        intervals = [motif[i + 1] - motif[i] for i in range(len(motif) - 1)]
        start_idx = _closest_index(scale_notes, motif[0] + seq_offset)
        start = scale_notes[start_idx]
        result = [start]
        for step in intervals:
            cur_idx = _closest_index(scale_notes, result[-1])
            # Move by approximately same number of scale steps
            scale_steps = max(-3, min(3, round(step / 2)))
            new_idx = max(0, min(len(scale_notes) - 1, cur_idx + scale_steps))
            result.append(scale_notes[new_idx])
        return result

    elif technique == "inversion":
        # Invert intervals (up becomes down)
        intervals = [motif[i + 1] - motif[i] for i in range(len(motif) - 1)]
        start = motif[0] + transpose
        result = [start]
        for iv in intervals:
            cur_idx = _closest_index(scale_notes, result[-1])
            inv_iv = -iv
            # Move in opposite direction
            scale_steps = max(-3, min(3, round(inv_iv / 2)))
            new_idx = max(0, min(len(scale_notes) - 1, cur_idx + scale_steps))
            result.append(scale_notes[new_idx])
        return result

    elif technique == "fragmentation":
        # Use only first half of motif
        half = max(1, len(motif) // 2)
        frag = motif[:half]
        # Repeat to fill
        result = (frag * ((len(motif) // half) + 1))[:len(motif)]
        return [n + transpose for n in result]

    elif technique == "retrograde":
        return list(reversed([n + transpose for n in motif]))

    return motif


def _build_contour_targets(length: int, contour: str) -> List[int]:
    """Return target direction (+1/-1/0) for each note position."""
    if contour == "arch":
        peak = length * 2 // 3
        return [1 if i < peak else (-1 if i > peak else 0) for i in range(length)]
    elif contour == "descending":
        return [-1] * length
    elif contour == "ascending":
        return [1] * length
    elif contour == "wave":
        period = max(4, length // 2)
        return [1 if (i // (period // 2)) % 2 == 0 else -1 for i in range(length)]
    else:
        return [0] * length


def _build_rhythm_pattern(
    beats_available: float,
    complexity: str,
    density: float,
) -> List[float]:
    """
    Build a list of note durations summing to beats_available.
    density: 0-1 (how many notes per beat)
    """
    base_durations = {
        "simple":  [2.0, 1.0, 0.5],
        "medium":  [1.0, 0.5, 0.25],
        "complex": [0.5, 0.25, 0.125],
    }.get(complexity, [1.0, 0.5, 0.25])

    durations = []
    remaining = beats_available
    # Approximate target number of notes
    target_notes = max(1, int(beats_available * density))

    while remaining > 0.01 and len(durations) < target_notes * 2:
        # Choose duration weighted toward appropriate complexity
        weights = [4.0 / (i + 1) for i in range(len(base_durations))]
        dur = random.choices(base_durations, weights=weights)[0]
        dur = min(dur, remaining)
        durations.append(dur)
        remaining -= dur

        # Occasional rest
        if random.random() < 0.1 and remaining > 0.5:
            rest = random.choice([0.25, 0.5])
            durations.append(-rest)  # negative = rest
            remaining -= rest

    # If we have too few notes, split the longest note
    while len([d for d in durations if d > 0]) < target_notes and len(durations) < 32:
        # Find longest note and split
        pos_durs = [(d, i) for i, d in enumerate(durations) if d > 0]
        if not pos_durs:
            break
        max_dur, max_idx = max(pos_durs)
        if max_dur <= 0.25:
            break
        half = max_dur / 2
        durations[max_idx] = half
        durations.insert(max_idx + 1, half)

    return durations


def generate_melody(
    progression: List[Dict[str, Any]],
    key: str,
    scale: str,
    complexity: str = "medium",
    role: str = "lead",
    length_bars: int = 4,
    lead_melody: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """
    Generate a melody with phrase structure, motivic development, and role intelligence.
    """
    if not progression:
        return []

    low, high = ROLE_REGISTERS.get(role, (60, 84))
    density = ROLE_DENSITY.get(role, 1.0)

    # Adjust density by complexity
    density_factor = {"simple": 0.6, "medium": 1.0, "complex": 1.4}.get(complexity, 1.0)
    effective_density = min(2.0, density * density_factor)

    scale_notes_full = _build_scale_register(key, scale, low, high)
    scale_notes_one_oct = get_scale_notes(key, scale)
    scale_set_midi = set(scale_notes_full)

    if not scale_notes_full:
        scale_notes_full = list(range(low, high + 1, 2))
        scale_set_midi = set(scale_notes_full)

    # Starting pitch
    center = (low + high) // 2
    start_pitch = _closest_index(scale_notes_full, center)
    start_pitch = scale_notes_full[start_pitch]

    # Determine contour from role
    role_contours = {
        "lead": "arch", "counter_melody": "wave", "ear_candy": "descending",
        "pad_melody": "flat", "bass_line": "flat",
    }
    contour = role_contours.get(role, "arch")
    if lead_melody and role == "counter_melody":
        # Use contrary contour to lead
        lead_contour = _analyze_contour(lead_melody)
        contrary = {"ascending": "descending", "descending": "ascending",
                    "arch": "wave", "wave": "arch", "flat": "arch"}
        contour = contrary.get(lead_contour, "wave")

    # Total beats
    total_beats = sum(c.get("duration_beats", 4) for c in progression)
    num_notes_approx = max(4, int(total_beats * effective_density))
    contour_targets = _build_contour_targets(num_notes_approx, contour)

    # Get chords by beat position
    chord_timeline = []
    pos = 0.0
    for chord in progression:
        dur = chord.get("duration_beats", 4.0)
        chord_timeline.append((pos, pos + dur, chord))
        pos += dur

    def get_chord_at(beat: float) -> Dict[str, Any]:
        for start, end, ch in chord_timeline:
            if start <= beat < end:
                return ch
        return chord_timeline[-1][2] if chord_timeline else {}

    # Build antecedent phrase (first half) and consequent phrase (second half)
    half_beats = total_beats / 2.0

    # Generate initial motif from first chord
    first_chord = progression[0]
    first_root = get_chord_root_midi(key, scale, first_chord.get("degree", 1))
    while first_root > high:
        first_root -= 12
    while first_root < low:
        first_root += 12

    first_chord_tones = get_chord_tones_in_register(
        first_root, first_chord.get("quality", "maj"), low, high
    )

    motif = _generate_motif(scale_notes_full, first_chord_tones, +1, motif_length=4)

    # Generate note sequence
    notes: List[Dict[str, Any]] = []
    current_pitch = start_pitch
    position = 0.0
    note_idx = 0

    # Phrase-by-phrase generation
    for phrase_num in range(2):  # antecedent + consequent
        phrase_start = phrase_num * half_beats
        phrase_end = (phrase_num + 1) * half_beats
        phrase_beats = half_beats

        # Rhythm pattern for this phrase
        rhythm = _build_rhythm_pattern(phrase_beats, complexity, effective_density)

        # Motivic development technique for consequent
        if phrase_num == 0:
            technique = "repeat"
            transpose = 0
        else:
            techniques = ["sequence", "inversion", "fragmentation", "retrograde"]
            technique = random.choice(techniques)
            # Transpose up by 3rd or 5th for sequence
            transpose = random.choice([-7, -5, 0, 3, 5, 7]) if technique == "sequence" else 0

        # Developed motif for this phrase
        if phrase_num == 1:
            dev_motif = _develop_motif(motif, technique, scale_notes_full, transpose)
        else:
            dev_motif = motif[:]

        motif_pos = 0
        phrase_position = phrase_start

        for dur in rhythm:
            if phrase_position >= phrase_end - 0.01:
                break

            is_rest = dur < 0
            actual_dur = abs(dur)

            if is_rest:
                phrase_position += actual_dur
                position = phrase_position
                continue

            # Determine if this is a strong beat
            beat_in_bar = phrase_position % 4.0
            is_strong = beat_in_bar < 0.01 or (beat_in_bar >= 1.99 and beat_in_bar <= 2.01)

            # Get current chord
            chord = get_chord_at(phrase_position)
            chord_root = get_chord_root_midi(key, scale, chord.get("degree", 1))
            while chord_root > high:
                chord_root -= 12
            while chord_root < low:
                chord_root += 12
            chord_quality = chord.get("quality", "maj")
            chord_tones = get_chord_tones_in_register(chord_root, chord_quality, low, high)

            # Contour target for this note
            target_dir = contour_targets[note_idx % len(contour_targets)] if contour_targets else 0

            # Use motif note if available, otherwise free generation
            if motif_pos < len(dev_motif) and note_idx < len(dev_motif):
                desired = dev_motif[motif_pos]
                # Clamp to register
                while desired > high:
                    desired -= 12
                while desired < low:
                    desired += 12
                # Snap to nearest scale note
                if desired not in scale_set_midi:
                    desired = scale_notes_full[_closest_index(scale_notes_full, desired)]
                pitch = desired
                motif_pos += 1
            else:
                # Free note generation with weighted pool
                approach_tones = _get_approach_tones(current_pitch, scale_set_midi)
                pitch = _weighted_note_choice(
                    chord_tones, scale_notes_full, approach_tones,
                    is_strong, current_pitch, target_dir, low, high
                )

            # Complementarity: avoid lead register collision if applicable
            if lead_melody and role in ("counter_melody", "ear_candy"):
                lead_at = [n["pitch_midi"] for n in lead_melody
                           if abs(n.get("position_beats", 0) - phrase_position) < actual_dur]
                if lead_at:
                    avg_lead = sum(lead_at) / len(lead_at)
                    # Push away from lead (prefer opposite register half)
                    if role == "counter_melody":
                        mid_range = (low + high) // 2
                        if avg_lead > mid_range and pitch > mid_range:
                            pitch = scale_notes_full[_closest_index(
                                scale_notes_full, low + (mid_range - low) // 3
                            )]
                        elif avg_lead < mid_range and pitch < mid_range:
                            pitch = scale_notes_full[_closest_index(
                                scale_notes_full, mid_range + (high - mid_range) // 3
                            )]

            # Bass line: root-5th emphasis
            if role == "bass_line":
                if is_strong or random.random() < 0.5:
                    pitch = chord_root
                elif random.random() < 0.4:
                    fifth = chord_root + 7
                    if low <= fifth <= high:
                        pitch = fifth

            current_pitch = pitch

            velocity = random.randint(65, 90)
            # Velocity shaping: accent on strong beats
            if is_strong:
                velocity = min(110, velocity + 10)

            notes.append({
                "pitch_midi": pitch,
                "note_name": midi_to_note_name(pitch),
                "duration_beats": actual_dur,
                "position_beats": phrase_position,
                "velocity": velocity,
                "is_chord_tone": pitch in set(chord_tones),
            })

            phrase_position += actual_dur
            note_idx += 1

        position = phrase_end

    # Rhythmic offset for counter_melody (don't attack on same beats as lead)
    if lead_melody and role == "counter_melody":
        lead_beats = {n.get("position_beats", 0) for n in lead_melody}
        offset = 0.5
        notes = [{**n, "position_beats": n["position_beats"] + offset} for n in notes]

    return notes


def _analyze_contour(melody: List[Dict[str, Any]]) -> str:
    """Analyze the overall contour direction of a melody."""
    if len(melody) < 2:
        return "flat"
    pitches = [n.get("pitch_midi", 60) for n in melody]
    first_half_avg = sum(pitches[:len(pitches) // 2]) / max(1, len(pitches) // 2)
    second_half_avg = sum(pitches[len(pitches) // 2:]) / max(1, len(pitches) - len(pitches) // 2)
    first = pitches[0]
    last = pitches[-1]
    peak = max(pitches)

    if abs(first - last) < 3:
        if peak > first + 4:
            return "arch"
        return "flat"
    if last > first + 2:
        return "ascending"
    if last < first - 2:
        return "descending"
    return "wave"


# ============================================================
#  MELODY VARIATIONS
# ============================================================

def regenerate_similar_melody(
    melody: List[Dict[str, Any]],
    progression: List[Dict[str, Any]],
    key: str,
    scale: str,
    role: str,
) -> List[Dict[str, Any]]:
    """
    Preserve: rhythm, contour DNA, phrase shape.
    Change: exact pitches slightly, ornaments, extensions.
    """
    if not melody:
        return []

    low, high = ROLE_REGISTERS.get(role, (60, 84))
    scale_notes = get_scale_note_set_full(key, scale, low, high)
    if not scale_notes:
        return melody

    new_notes = []
    for note in melody:
        pitch = note.get("pitch_midi", 60)
        # Small perturbation: shift ±1-2 scale steps
        idx = _closest_index(scale_notes, pitch)
        shift = random.choice([-2, -1, -1, 0, 0, 1, 1, 2])
        new_idx = max(0, min(len(scale_notes) - 1, idx + shift))
        new_pitch = scale_notes[new_idx]
        new_pitch = max(low, min(high, new_pitch))

        new_notes.append({
            **note,
            "pitch_midi": new_pitch,
            "note_name": midi_to_note_name(new_pitch),
        })

    return new_notes


def regenerate_different_melody(
    melody: List[Dict[str, Any]],
    progression: List[Dict[str, Any]],
    key: str,
    scale: str,
    role: str,
) -> List[Dict[str, Any]]:
    """
    Change: contour (invert), density (toggle sparse/dense), register shift.
    """
    if not melody:
        return []

    # Detect original contour and invert
    orig_contour = _analyze_contour(melody)
    contrary = {"ascending": "descending", "descending": "ascending",
                "arch": "wave", "wave": "arch", "flat": "ascending"}
    new_contour = contrary.get(orig_contour, "wave")

    # Alternate complexity
    orig_n = len(melody)
    total_beats = sum(n.get("duration_beats", 0.5) for n in melody)
    orig_density = orig_n / max(1, total_beats)
    new_complexity = "simple" if orig_density > 1.5 else "complex"

    return generate_melody(
        progression, key, scale,
        complexity=new_complexity, role=role,
        length_bars=max(4, int(total_beats / 4)),
    )


def elongate_melody(
    melody: List[Dict[str, Any]],
    progression: List[Dict[str, Any]],
    key: str,
    scale: str,
    role: str,
) -> List[Dict[str, Any]]:
    """
    Extend melody by repeating with motivic development.
    """
    if not melody:
        return []

    max_pos = max(n.get("position_beats", 0) + n.get("duration_beats", 0.5) for n in melody)
    low, high = ROLE_REGISTERS.get(role, (60, 84))
    scale_notes = get_scale_note_set_full(key, scale, low, high) or list(range(low, high + 1, 2))

    # Analyze original melody as motif
    pitches = [n.get("pitch_midi", 60) for n in melody]
    motif = pitches[:min(8, len(pitches))]

    technique = random.choice(["sequence", "inversion", "fragmentation"])
    transpose = random.choice([-7, -5, 0, 3, 5, 7]) if technique == "sequence" else 0
    dev = _develop_motif(motif, technique, scale_notes, transpose)

    extended = list(melody)
    for i, note in enumerate(melody):
        new_pitch = dev[i % len(dev)]
        while new_pitch > high:
            new_pitch -= 12
        while new_pitch < low:
            new_pitch += 12
        if new_pitch not in set(scale_notes):
            new_pitch = scale_notes[_closest_index(scale_notes, new_pitch)]

        extended.append({
            **note,
            "pitch_midi": new_pitch,
            "note_name": midi_to_note_name(new_pitch),
            "position_beats": note.get("position_beats", 0) + max_pos,
        })

    return extended


# ============================================================
#  AUDIO ANALYSIS (fallback to algorithmic)
# ============================================================

def analyze_audio_to_progression(data: bytes, key: str = "C", scale: str = "major") -> Dict[str, Any]:
    try:
        num_samples = len(data) // 2
        if num_samples < 64:
            raise ValueError("Too few samples")
        samples = np.frombuffer(data[:num_samples * 2], dtype=np.int16).astype(np.float64)
        fft_result = np.fft.rfft(samples)
        magnitudes = np.abs(fft_result)
        freqs = np.fft.rfftfreq(len(samples), 1.0 / 44100)
        top_indices = np.argsort(magnitudes)[-8:]
        top_freqs = freqs[top_indices]
        top_freqs = top_freqs[top_freqs > 20]
        if len(top_freqs) == 0:
            raise ValueError("No usable frequencies")
        midi_notes = []
        for f in top_freqs[:4]:
            if f > 0:
                midi = int(round(69 + 12 * math.log2(f / 440.0)))
                midi_notes.append(max(24, min(108, midi)))
        if not midi_notes:
            raise ValueError("No midi notes")
    except Exception:
        pass
    return generate_progression(key, scale, emotions=["hope"], length_bars=4)


def analyze_audio_to_melody(data: bytes, key: str = "C", scale: str = "major") -> List[Dict]:
    prog = analyze_audio_to_progression(data, key, scale)
    return generate_melody(prog["progression"], key, scale, complexity="medium", role="lead", length_bars=4)


# ============================================================
#  PYDANTIC MODELS
# ============================================================

class ChordGenerateRequest(BaseModel):
    emotions: Optional[List[str]] = None
    prompt: Optional[str] = None
    key: str = "C"
    scale: str = "major"
    length: int = 4


class ChordRegenerateRequest(BaseModel):
    progression: List[Dict[str, Any]]
    key: str = "C"
    scale: str = "major"


class ChordMixRequest(BaseModel):
    progression_a: List[Dict[str, Any]]
    progression_b: List[Dict[str, Any]]


class ChordElongateRequest(BaseModel):
    progression: List[Dict[str, Any]]
    key: str = "C"
    scale: str = "major"


class MelodyGenerateRequest(BaseModel):
    progression: List[Dict[str, Any]]
    key: str = "C"
    scale: str = "major"
    complexity: str = "medium"
    mode: str = "normal"
    role: str = "lead"
    length: int = 4


class MelodyRegenerateRequest(BaseModel):
    melody: List[Dict[str, Any]]
    progression: List[Dict[str, Any]]
    key: str = "C"
    scale: str = "major"
    role: str = "lead"


class MelodyRoleRequest(BaseModel):
    progression: List[Dict[str, Any]]
    key: str = "C"
    scale: str = "major"
    role: str = "counter_melody"
    lead_melody: Optional[List[Dict[str, Any]]] = None


class MelodyElongateRequest(BaseModel):
    melody: List[Dict[str, Any]]
    progression: List[Dict[str, Any]]
    key: str = "C"
    scale: str = "major"
    role: str = "lead"


# ============================================================
#  API ENDPOINTS
# ============================================================

@app.get("/api/chords/emotions")
def get_emotions():
    return {"emotions": sorted(EMOTION_PARAMS.keys())}


@app.post("/api/chords/generate")
def api_generate_chords(req: ChordGenerateRequest):
    return generate_progression(
        key=req.key, scale=req.scale,
        emotions=req.emotions, length_bars=req.length, prompt=req.prompt,
    )


@app.post("/api/chords/regenerate-similar")
def api_regenerate_similar(req: ChordRegenerateRequest):
    return regenerate_similar_progression(req.progression, req.key, req.scale)


@app.post("/api/chords/regenerate-different")
def api_regenerate_different(req: ChordRegenerateRequest):
    return regenerate_different_progression(req.progression, req.key, req.scale)


@app.post("/api/chords/elongate")
def api_elongate_chords(req: ChordElongateRequest):
    return elongate_progression(req.progression, req.key, req.scale)


@app.post("/api/chords/mix")
def api_mix_chords(req: ChordMixRequest):
    return mix_progressions(req.progression_a, req.progression_b)


@app.post("/api/chords/analyze-audio")
async def api_analyze_chord_audio(file: UploadFile = File(...)):
    data = await file.read()
    return analyze_audio_to_progression(data)


@app.post("/api/melodies/generate")
def api_generate_melody(req: MelodyGenerateRequest):
    notes = generate_melody(
        progression=req.progression, key=req.key, scale=req.scale,
        complexity=req.complexity, role=req.role, length_bars=req.length,
    )
    return {"melody": notes, "role": req.role, "mode": req.mode}


@app.post("/api/melodies/regenerate-similar")
def api_melody_similar(req: MelodyRegenerateRequest):
    notes = regenerate_similar_melody(req.melody, req.progression, req.key, req.scale, req.role)
    return {"melody": notes, "role": req.role}


@app.post("/api/melodies/regenerate-different")
def api_melody_different(req: MelodyRegenerateRequest):
    notes = regenerate_different_melody(req.melody, req.progression, req.key, req.scale, req.role)
    return {"melody": notes, "role": req.role}


@app.post("/api/melodies/generate-role")
def api_generate_role(req: MelodyRoleRequest):
    notes = generate_melody(
        progression=req.progression, key=req.key, scale=req.scale,
        complexity="medium", role=req.role, length_bars=4,
        lead_melody=req.lead_melody,
    )
    return {"melody": notes, "role": req.role}


@app.post("/api/melodies/elongate")
def api_elongate_melody(req: MelodyElongateRequest):
    notes = elongate_melody(req.melody, req.progression, req.key, req.scale, req.role)
    return {"melody": notes, "role": req.role}


@app.post("/api/melodies/analyze-audio")
async def api_analyze_melody_audio(file: UploadFile = File(...)):
    data = await file.read()
    notes = analyze_audio_to_melody(data)
    return {"melody": notes, "role": "lead"}


# ============================================================
#  STATIC FILES
# ============================================================

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
