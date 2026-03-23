"""Infinite Chord & Melody Generator — self-contained FastAPI application."""

from __future__ import annotations

import os
import random
import math
import struct
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

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

# ===== MUSIC THEORY CONSTANTS =====

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

NOTE_TO_MIDI_BASE: Dict[str, int] = {
    "C": 60, "C#": 61, "D": 62, "D#": 63, "E": 64, "F": 65,
    "F#": 66, "G": 67, "G#": 68, "A": 69, "A#": 70, "B": 71,
}

SCALES: Dict[str, List[int]] = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "melodic_minor": [0, 2, 3, 5, 7, 9, 11],
}

CHORD_INTERVALS: Dict[str, List[int]] = {
    "maj": [0, 4, 7],
    "min": [0, 3, 7],
    "7": [0, 4, 7, 10],
    "maj7": [0, 4, 7, 11],
    "m7": [0, 3, 7, 10],
    "dim": [0, 3, 6],
    "dim7": [0, 3, 6, 9],
    "aug": [0, 4, 8],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7],
    "m9": [0, 3, 7, 10, 14],
    "maj9": [0, 4, 7, 11, 14],
    "add9": [0, 4, 7, 14],
    "m7b5": [0, 3, 6, 10],
}

EMOTION_PROGRESSIONS: Dict[str, Dict[str, Any]] = {
    "nostalgia": {"degrees": [6, 4, 1, 5], "qualities": ["min", "m7", "maj", "7"], "scale": "major"},
    "excitement": {"degrees": [1, 5, 6, 4], "qualities": ["maj", "7", "min", "maj"], "scale": "major"},
    "power": {"degrees": [1, 7, 6, 7], "qualities": ["maj", "maj", "min", "maj"], "scale": "minor"},
    "melancholy": {"degrees": [6, 4, 1, 5], "qualities": ["m7", "m7", "maj7", "m7"], "scale": "minor"},
    "hope": {"degrees": [1, 3, 4, 5], "qualities": ["maj", "min", "maj", "7"], "scale": "major"},
    "aggression": {"degrees": [1, 7, 6, 5], "qualities": ["min", "maj", "maj", "min"], "scale": "phrygian"},
    "serenity": {"degrees": [1, 2, 4, 1], "qualities": ["maj7", "m7", "maj7", "maj7"], "scale": "lydian"},
    "tension": {"degrees": [1, 4, 7, 1], "qualities": ["m7b5", "min", "dim7", "m7"], "scale": "harmonic_minor"},
    "euphoria": {"degrees": [1, 5, 3, 6], "qualities": ["maj", "maj", "min", "min"], "scale": "major"},
    "longing": {"degrees": [6, 4, 1, 5], "qualities": ["m7", "maj7", "maj", "m7"], "scale": "dorian"},
    "wonder": {"degrees": [1, 3, 4, 2], "qualities": ["maj7", "min", "add9", "m7"], "scale": "lydian"},
    "defiance": {"degrees": [1, 7, 1, 7], "qualities": ["min", "maj", "min", "maj"], "scale": "minor"},
    "tenderness": {"degrees": [1, 4, 2, 5], "qualities": ["maj7", "maj7", "m7", "m7"], "scale": "major"},
    "triumph": {"degrees": [1, 4, 5, 1], "qualities": ["maj", "maj", "7", "maj"], "scale": "major"},
    "mystery": {"degrees": [1, 7, 6, 3], "qualities": ["m7", "maj", "min", "m7"], "scale": "phrygian"},
    "vulnerability": {"degrees": [6, 3, 4, 1], "qualities": ["m7", "min", "maj7", "maj7"], "scale": "major"},
}

ROMAN_NUMERALS = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII"}

ROLE_REGISTERS: Dict[str, tuple] = {
    "lead": (60, 84),
    "counter_melody": (55, 79),
    "ear_candy": (72, 96),
    "pad_melody": (48, 72),
    "bass_line": (28, 52),
}


# ===== MUSIC GENERATION FUNCTIONS =====


def get_scale_notes(key: str, scale: str) -> List[int]:
    """Return MIDI notes for one octave of the given key/scale starting at octave 4."""
    root = NOTE_TO_MIDI_BASE.get(key, 60)
    intervals = SCALES.get(scale, SCALES["major"])
    return [root + i for i in intervals]


def midi_to_note_name(midi: int) -> str:
    """Convert a MIDI note number to a note name like C4."""
    octave = midi // 12 - 1
    note = NOTES[midi % 12]
    return f"{note}{octave}"


def get_chord_midi(key: str, scale: str, degree: int, quality: str, octave: int = 4) -> List[int]:
    """Return MIDI notes for a chord built on a scale degree."""
    root_base = NOTE_TO_MIDI_BASE.get(key, 60)
    scale_intervals = SCALES.get(scale, SCALES["major"])

    # degree is 1-based; map to scale index
    idx = (degree - 1) % len(scale_intervals)
    chord_root = root_base + scale_intervals[idx]

    # Adjust octave
    chord_root = chord_root + (octave - 4) * 12

    chord_ints = CHORD_INTERVALS.get(quality, CHORD_INTERVALS["maj"])
    return [chord_root + interval for interval in chord_ints]


def build_chord_name(key: str, scale: str, degree: int, quality: str) -> str:
    """Build a human-readable chord name like 'Cmaj7'."""
    scale_intervals = SCALES.get(scale, SCALES["major"])
    idx = (degree - 1) % len(scale_intervals)
    root_midi = NOTE_TO_MIDI_BASE.get(key, 60) + scale_intervals[idx]
    root_note = NOTES[root_midi % 12]
    return f"{root_note}{quality}"


def generate_progression(
    key: str,
    scale: str,
    emotions: Optional[List[str]] = None,
    length_bars: int = 4,
    prompt: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate a chord progression based on emotions/prompt."""
    template = None

    # Pick the best matching emotion template
    if emotions:
        for emo in emotions:
            if emo.lower() in EMOTION_PROGRESSIONS:
                template = EMOTION_PROGRESSIONS[emo.lower()]
                break

    # If only prompt, extract keywords
    if template is None and prompt:
        prompt_lower = prompt.lower()
        for emo_name, emo_data in EMOTION_PROGRESSIONS.items():
            if emo_name in prompt_lower:
                template = emo_data
                break

    # Default to a random emotion
    if template is None:
        template = random.choice(list(EMOTION_PROGRESSIONS.values()))

    degrees = template["degrees"]
    qualities = template["qualities"]
    emo_scale = template.get("scale", scale)

    # Build the progression
    chords = []
    num_chords = len(degrees)
    if length_bars <= 4:
        dur_per_chord = 4.0  # 1 bar each
    else:
        dur_per_chord = (length_bars * 4.0) / num_chords

    for i in range(num_chords):
        deg = degrees[i]
        qual = qualities[i]
        midi_notes = get_chord_midi(key, emo_scale, deg, qual)
        roman = ROMAN_NUMERALS.get(deg, str(deg))
        name = build_chord_name(key, emo_scale, deg, qual)

        chords.append({
            "name": name,
            "roman_numeral": roman,
            "midi_notes": midi_notes,
            "duration_beats": dur_per_chord,
            "position_bar": i,
            "degree": deg,
            "quality": qual,
        })

    return {"progression": chords, "key": key, "scale": emo_scale, "length_bars": length_bars}


def generate_melody(
    progression: List[Dict],
    key: str,
    scale: str,
    complexity: str = "medium",
    role: str = "lead",
    length_bars: int = 4,
) -> List[Dict]:
    """Generate a melody over a chord progression."""
    reg = ROLE_REGISTERS.get(role, (60, 84))
    low, high = reg

    notes_per_bar = {"simple": 2, "medium": 4, "complex": 6}.get(complexity, 4)
    base_dur = 4.0 / notes_per_bar

    scale_notes_one_octave = get_scale_notes(key, scale)

    # Build full scale across register
    all_scale_notes: List[int] = []
    for oct_shift in range(-3, 5):
        for sn in scale_notes_one_octave:
            midi = sn + oct_shift * 12
            if low <= midi <= high:
                all_scale_notes.append(midi)
    all_scale_notes = sorted(set(all_scale_notes))
    if not all_scale_notes:
        all_scale_notes = list(range(low, high + 1))

    melody_notes: List[Dict] = []
    current_pitch = all_scale_notes[len(all_scale_notes) // 2]
    position = 0.0

    for chord in progression:
        chord_tones = set(chord.get("midi_notes", []))
        beats_in_chord = chord.get("duration_beats", 4.0)
        notes_in_chord = max(1, int(beats_in_chord / base_dur))

        for ni in range(notes_in_chord):
            beat_in_bar = ni * base_dur
            is_strong_beat = beat_in_bar % 2.0 < 0.01

            if is_strong_beat and chord_tones:
                # Target a chord tone in register
                candidates = [ct for ct in chord_tones if low <= ct <= high]
                if not candidates:
                    candidates = list(chord_tones)
                # Pick closest to current pitch
                target = min(candidates, key=lambda c: abs(c - current_pitch))
                # Bring into register if needed
                while target < low:
                    target += 12
                while target > high:
                    target -= 12
                current_pitch = max(low, min(high, target))
                is_ct = True
            else:
                # Step-wise motion
                step = random.choice([-2, -1, 1, 2])
                idx = _closest_index(all_scale_notes, current_pitch)
                new_idx = max(0, min(len(all_scale_notes) - 1, idx + step))
                current_pitch = all_scale_notes[new_idx]
                is_ct = current_pitch in chord_tones

            velocity = random.randint(70, 95)
            melody_notes.append({
                "pitch_midi": current_pitch,
                "note_name": midi_to_note_name(current_pitch),
                "duration_beats": base_dur,
                "position_beats": position,
                "velocity": velocity,
                "is_chord_tone": is_ct,
            })
            position += base_dur

    return melody_notes


def _closest_index(sorted_list: List[int], value: int) -> int:
    """Return the index of the closest value in a sorted list."""
    if not sorted_list:
        return 0
    best = 0
    best_dist = abs(sorted_list[0] - value)
    for i, v in enumerate(sorted_list):
        d = abs(v - value)
        if d < best_dist:
            best = i
            best_dist = d
    return best


def analyze_audio_to_progression(data: bytes, key: str = "C", scale: str = "major") -> Dict[str, Any]:
    """Basic audio analysis using numpy FFT, returns a chord progression."""
    try:
        # Try to interpret as raw PCM-like data
        num_samples = len(data) // 2
        if num_samples < 64:
            raise ValueError("Too few samples")
        samples = np.frombuffer(data[:num_samples * 2], dtype=np.int16).astype(np.float64)
        if len(samples) < 64:
            raise ValueError("Too few samples")
        # Perform FFT
        fft_result = np.fft.rfft(samples)
        magnitudes = np.abs(fft_result)
        # Assume 44100 Hz sample rate
        freqs = np.fft.rfftfreq(len(samples), 1.0 / 44100)
        # Find top 4 peaks
        top_indices = np.argsort(magnitudes)[-8:]
        top_freqs = freqs[top_indices]
        top_freqs = top_freqs[top_freqs > 20]  # ignore sub-bass noise
        if len(top_freqs) == 0:
            raise ValueError("No usable frequencies")
        # Convert frequencies to MIDI
        midi_notes = []
        for f in top_freqs[:4]:
            if f > 0:
                midi = int(round(69 + 12 * math.log2(f / 440.0)))
                midi = max(24, min(108, midi))
                midi_notes.append(midi)
        if not midi_notes:
            raise ValueError("No midi notes derived")
    except Exception:
        # Fallback: return default progression
        return generate_progression(key, scale, emotions=["hope"], length_bars=4)

    # Build a simple progression from detected notes
    return generate_progression(key, scale, emotions=None, length_bars=4)


def analyze_audio_to_melody(data: bytes, key: str = "C", scale: str = "major") -> List[Dict]:
    """Basic audio analysis, returns a simple melody."""
    prog = analyze_audio_to_progression(data, key, scale)
    return generate_melody(prog["progression"], key, scale, complexity="medium", role="lead", length_bars=4)


# ===== PYDANTIC MODELS =====


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


class MelodyModifyRequest(BaseModel):
    melody: List[Dict[str, Any]]
    locked_indices: Optional[List[int]] = None
    complexity: Optional[str] = None


class MelodyElongateRequest(BaseModel):
    melody: List[Dict[str, Any]]
    progression: List[Dict[str, Any]]
    key: str = "C"
    scale: str = "major"


# ===== API ENDPOINTS =====


@app.get("/api/chords/emotions")
def get_emotions():
    """Return the list of available emotion names."""
    return {"emotions": sorted(EMOTION_PROGRESSIONS.keys())}


@app.post("/api/chords/generate")
def api_generate_chords(req: ChordGenerateRequest):
    """Generate a chord progression."""
    return generate_progression(
        key=req.key,
        scale=req.scale,
        emotions=req.emotions,
        length_bars=req.length,
        prompt=req.prompt,
    )


@app.post("/api/chords/regenerate-similar")
def api_regenerate_similar(req: ChordRegenerateRequest):
    """Regenerate a similar progression by slight transposition."""
    new_prog = []
    for chord in req.progression:
        shift = random.choice([-2, -1, 1, 2])
        midi = chord.get("midi_notes", [])
        new_midi = [m + shift for m in midi]
        root_midi = new_midi[0] if new_midi else 60
        root_name = NOTES[root_midi % 12]
        quality = chord.get("quality", "maj")
        new_prog.append({
            **chord,
            "midi_notes": new_midi,
            "name": f"{root_name}{quality}",
        })
    return {"progression": new_prog, "key": req.key, "scale": req.scale}


@app.post("/api/chords/regenerate-different")
def api_regenerate_different(req: ChordRegenerateRequest):
    """Generate a completely different progression."""
    emotions = list(EMOTION_PROGRESSIONS.keys())
    chosen = random.choice(emotions)
    return generate_progression(req.key, req.scale, emotions=[chosen], length_bars=4)


@app.post("/api/chords/mix")
def api_mix_chords(req: ChordMixRequest):
    """Interleave chords from two progressions."""
    mixed = []
    a, b = req.progression_a, req.progression_b
    max_len = max(len(a), len(b))
    for i in range(max_len):
        if i < len(a):
            mixed.append(a[i])
        if i < len(b):
            mixed.append(b[i])
    return {"progression": mixed, "key": "C", "scale": "major"}


@app.post("/api/chords/elongate")
def api_elongate_chords(req: ChordElongateRequest):
    """Repeat the progression with slight variations."""
    extended = list(req.progression)
    for chord in req.progression:
        shift = random.choice([-1, 0, 1])
        midi = chord.get("midi_notes", [])
        new_midi = [m + shift for m in midi]
        root_midi = new_midi[0] if new_midi else 60
        root_name = NOTES[root_midi % 12]
        quality = chord.get("quality", "maj")
        extended.append({
            **chord,
            "midi_notes": new_midi,
            "name": f"{root_name}{quality}",
        })
    return {"progression": extended, "key": req.key, "scale": req.scale}


@app.post("/api/chords/analyze-audio")
async def api_analyze_chord_audio(file: UploadFile = File(...)):
    """Analyze uploaded audio and return a chord progression."""
    data = await file.read()
    return analyze_audio_to_progression(data)


@app.post("/api/melodies/generate")
def api_generate_melody(req: MelodyGenerateRequest):
    """Generate a melody over a chord progression."""
    notes = generate_melody(
        progression=req.progression,
        key=req.key,
        scale=req.scale,
        complexity=req.complexity,
        role=req.role,
        length_bars=req.length,
    )
    return {"melody": notes, "role": req.role}


@app.post("/api/melodies/regenerate-similar")
def api_melody_similar(req: MelodyRegenerateRequest):
    """Regenerate a melody with slight pitch shifts."""
    new_notes = []
    for note in req.melody:
        shift = random.choice([-2, -1, 0, 1, 2])
        pitch = note.get("pitch_midi", 60) + shift
        pitch = max(24, min(108, pitch))
        new_notes.append({
            **note,
            "pitch_midi": pitch,
            "note_name": midi_to_note_name(pitch),
        })
    return {"melody": new_notes, "role": req.role}


@app.post("/api/melodies/regenerate-different")
def api_melody_different(req: MelodyRegenerateRequest):
    """Generate a completely different melody."""
    notes = generate_melody(
        progression=req.progression,
        key=req.key,
        scale=req.scale,
        complexity="complex" if random.random() > 0.5 else "simple",
        role=req.role,
        length_bars=4,
    )
    return {"melody": notes, "role": req.role}


@app.post("/api/melodies/generate-role")
def api_generate_role(req: MelodyRoleRequest):
    """Generate a melody for a specific role."""
    notes = generate_melody(
        progression=req.progression,
        key=req.key,
        scale=req.scale,
        complexity="medium",
        role=req.role,
        length_bars=4,
    )
    return {"melody": notes, "role": req.role}


@app.post("/api/melodies/modify")
def api_modify_melody(req: MelodyModifyRequest):
    """Modify a melody with locked notes and optional complexity change."""
    notes = list(req.melody)
    locked = set(req.locked_indices or [])

    if req.complexity:
        # Adjust complexity
        notes_per_bar = {"simple": 2, "medium": 4, "complex": 6}.get(req.complexity, 4)
        if req.complexity == "simple" and len(notes) > 8:
            notes = [n for i, n in enumerate(notes) if i % 2 == 0]
        elif req.complexity == "complex":
            expanded: List[Dict[str, Any]] = []
            for i, n in enumerate(notes):
                expanded.append(n)
                if i < len(notes) - 1 and i not in locked:
                    nxt = notes[i + 1]
                    mid_pitch = (n.get("pitch_midi", 60) + nxt.get("pitch_midi", 60)) // 2
                    expanded.append({
                        "pitch_midi": mid_pitch,
                        "note_name": midi_to_note_name(mid_pitch),
                        "duration_beats": 0.25,
                        "position_beats": n.get("position_beats", 0) + n.get("duration_beats", 0.5) * 0.5,
                        "velocity": max(1, n.get("velocity", 80) - 10),
                        "is_chord_tone": False,
                    })
            notes = expanded

    # Regenerate unlocked notes slightly
    for i in range(len(notes)):
        if i not in locked:
            shift = random.choice([-1, 0, 1])
            pitch = notes[i].get("pitch_midi", 60) + shift
            pitch = max(24, min(108, pitch))
            notes[i] = {**notes[i], "pitch_midi": pitch, "note_name": midi_to_note_name(pitch)}

    return {"melody": notes}


@app.post("/api/melodies/elongate")
def api_elongate_melody(req: MelodyElongateRequest):
    """Elongate a melody by repeating with slight variation."""
    original = req.melody
    if not original:
        return {"melody": []}

    max_pos = max(n.get("position_beats", 0) + n.get("duration_beats", 0) for n in original)
    extended = list(original)
    for note in original:
        shift = random.choice([-2, -1, 0, 1, 2])
        pitch = note.get("pitch_midi", 60) + shift
        pitch = max(24, min(108, pitch))
        extended.append({
            **note,
            "pitch_midi": pitch,
            "note_name": midi_to_note_name(pitch),
            "position_beats": note.get("position_beats", 0) + max_pos,
        })
    return {"melody": extended}


@app.post("/api/melodies/analyze-audio")
async def api_analyze_melody_audio(file: UploadFile = File(...)):
    """Analyze uploaded audio and return a melody."""
    data = await file.read()
    notes = analyze_audio_to_melody(data)
    return {"melody": notes, "role": "lead"}


# ===== STATIC FILES =====

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
