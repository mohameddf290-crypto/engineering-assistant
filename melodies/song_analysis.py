"""
OPERATING SYSTEM BRAIN: Song Analysis Engine (Melodies)
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

Purpose: Analyzes a full song (no vocals/drums) and extracts melodic DNA:
contour, rhythm, phrasing, intervals, emotional arc.

Default AI thinking says "extract melodic fragments from the analyzed song and
use them as templates." That is copying, not inspiration. This brain extracts
the underlying melodic *principles* — the contour shape, rhythmic tendencies,
phrasing length, interval preferences, syncopation profile, emotional arc —
and uses those abstract principles as a creation blueprint. The actual melodic
content of the source is never used or recalled.

Contour is mapped as a directional shape over time — rising, falling, arching,
cascading — not as a sequence of pitch values. Rhythmic DNA is extracted as
onset density and syncopation patterns, not note durations. This abstraction
ensures that the melody created from this analysis will be inspired by the
source without sharing any of its content.

Protocols:
  1. Analysis extracts melodic principles, not melodic content. The source
     pitches are never stored or forwarded to the creation step.
  2. Contour is mapped as a directional shape over time, not as pitch values.
     The shape has direction (up/down) and rate (step/leap) as its vocabulary.
  3. Rhythmic DNA is extracted as onset density and syncopation patterns, not
     note durations. This captures the rhythmic feel without copying the rhythm.
"""

# TODO: Design this brain with Cursor — define the contour extraction
# algorithm (directional encoding of pitch movement), the rhythmic DNA
# model (onset density windows + syncopation scoring), the phrasing
# structure detection logic, interval preference histogram construction,
# and the emotional arc mapping approach.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class MelodicDNA:
    """
    Abstract melodic principles extracted from a song — no pitch content.

    Attributes:
        file_path: Path to the analysed audio file.
        contour_shape: Directional contour encoding (e.g. "arch", "cascading descent").
        rhythmic_density: Average note onset density per beat.
        phrasing_length_bars: Typical phrase length in bars.
        interval_preferences: Histogram of preferred interval sizes (semitones).
        syncopation_level: Syncopation score 0.0 (grid-locked) to 1.0 (highly syncopated).
        emotional_arc: Per-section emotional arc description.
        peak_moments: List of (bar, beat) positions where melodic climaxes occur.
    """

    file_path: str
    contour_shape: str
    rhythmic_density: float
    phrasing_length_bars: float
    interval_preferences: Dict[int, float] = field(default_factory=dict)
    syncopation_level: float = 0.0
    emotional_arc: List[str] = field(default_factory=list)
    peak_moments: List[Tuple[int, float]] = field(default_factory=list)


class SongAnalysisEngine:
    """
    Brain M2 — Song Analysis Engine (Melodies).

    Analyses a full song to extract melodic DNA: abstract principles that
    inform melody creation without copying any melodic content.

    Audio loading uses numpy/scipy when available; if the file cannot be
    loaded the engine falls back to musically reasonable defaults.
    """

    _CONTOUR_SHAPES = ["arch", "ascending", "descending", "wave", "inverted_arch"]
    _EMOTION_VOCAB = ["tense", "bright", "melancholic", "energetic", "calm", "dramatic"]

    def __init__(self) -> None:
        self._analysis_cache: Dict[str, MelodicDNA] = {}

    # ── Public API ─────────────────────────────────────────────────────────

    def analyse_song(self, audio_path: str) -> MelodicDNA:
        """Full melodic DNA extraction pipeline (no pitch content retained)."""
        if audio_path in self._analysis_cache:
            return self._analysis_cache[audio_path]

        contour = self.extract_contour_shape(audio_path)
        density, syncopation = self.extract_rhythmic_dna(audio_path)
        phrasing = self.map_phrasing_structure(audio_path)
        intervals = self.extract_interval_preferences(audio_path)
        arc = self.map_emotional_arc(audio_path)
        peaks = self._estimate_peak_moments(phrasing, arc)

        dna = MelodicDNA(
            file_path=audio_path,
            contour_shape=contour,
            rhythmic_density=density,
            phrasing_length_bars=phrasing,
            interval_preferences=intervals,
            syncopation_level=syncopation,
            emotional_arc=arc,
            peak_moments=peaks,
        )
        self._analysis_cache[audio_path] = dna
        return dna

    # Alias matching task-spec naming
    def analyze(self, audio_path: str) -> MelodicDNA:
        """Alias for analyse_song."""
        return self.analyse_song(audio_path)

    def extract_contour_shape(self, audio_path: str) -> str:
        """
        Analyse pitch movement directions and return a contour-shape label.
        Uses ZCR proxy via numpy FFT when audio is available.
        """
        samples, sr = self._load_audio(audio_path)
        if samples is None:
            return "arch"
        try:
            import numpy as np
            # Split into 8 equal segments, estimate dominant frequency per segment
            n_segs = 8
            seg_len = len(samples) // n_segs
            if seg_len == 0:
                return "arch"
            freqs: List[float] = []
            for i in range(n_segs):
                seg = samples[i * seg_len: (i + 1) * seg_len]
                if len(seg) == 0:
                    freqs.append(0.0)
                    continue
                fft = np.abs(np.fft.rfft(seg))
                bin_hz = sr / len(seg)
                # Focus on melodic range: 80–2000 Hz
                lo_bin = max(1, int(80 / bin_hz))
                hi_bin = min(len(fft) - 1, int(2000 / bin_hz))
                if hi_bin <= lo_bin:
                    freqs.append(0.0)
                    continue
                dominant_bin = lo_bin + int(np.argmax(fft[lo_bin: hi_bin + 1]))
                freqs.append(float(dominant_bin))
            return self._classify_contour(freqs)
        except Exception:
            return "arch"

    def extract_rhythmic_dna(self, audio_path: str) -> Tuple[float, float]:
        """
        Return (onset_density_per_beat, syncopation_score) as abstract values.
        Uses energy-based onset detection when numpy is available.
        """
        samples, sr = self._load_audio(audio_path)
        if samples is None:
            return (2.0, 0.3)
        try:
            import numpy as np
            frame_len = int(sr * 0.02)   # 20 ms frames
            hop = frame_len // 2
            frames = [samples[i: i + frame_len] for i in range(0, len(samples) - frame_len, hop)]
            energies = np.array([np.sum(f ** 2) for f in frames])
            if len(energies) < 4:
                return (2.0, 0.3)
            # Onset = energy peak (local max > mean * 1.5)
            threshold = float(np.mean(energies)) * 1.5
            onsets = [i for i in range(1, len(energies) - 1)
                      if energies[i] > threshold and energies[i] >= energies[i - 1] and energies[i] >= energies[i + 1]]
            duration_s = len(samples) / sr
            bpm = 120.0  # assumed
            beats = duration_s / (60.0 / bpm)
            density = len(onsets) / max(beats, 1.0)
            # Syncopation: fraction of onsets that fall off the quarter-beat grid
            frames_per_beat = (sr / bpm * 60) / hop
            on_beat = sum(1 for o in onsets if (o % max(1, int(frames_per_beat))) < (frames_per_beat * 0.1))
            syncopation = 1.0 - (on_beat / max(len(onsets), 1))
            return (round(min(density, 8.0), 2), round(min(syncopation, 1.0), 2))
        except Exception:
            return (2.0, 0.3)

    def map_phrasing_structure(self, audio_path: str) -> float:
        """
        Estimate typical phrase length in bars by detecting energy valleys
        that suggest phrase boundaries.
        """
        samples, sr = self._load_audio(audio_path)
        if samples is None:
            return 4.0
        try:
            import numpy as np
            bar_len_s = 2.0   # assumed at ~120 bpm, 4/4
            bar_samples = int(sr * bar_len_s)
            if bar_samples == 0:
                return 4.0
            n_bars = max(1, len(samples) // bar_samples)
            bar_energies = [
                float(np.mean(samples[i * bar_samples: (i + 1) * bar_samples] ** 2))
                for i in range(n_bars)
            ]
            if len(bar_energies) < 2:
                return 4.0
            mean_e = float(np.mean(bar_energies))
            valleys = [i for i, e in enumerate(bar_energies) if e < mean_e * 0.7]
            if len(valleys) < 2:
                return 4.0
            diffs = [valleys[i + 1] - valleys[i] for i in range(len(valleys) - 1)]
            avg_phrase = sum(diffs) / len(diffs)
            # Round to nearest common phrase length
            for pl in [2, 4, 8, 16]:
                if abs(avg_phrase - pl) <= 1.5:
                    return float(pl)
            return round(avg_phrase, 1)
        except Exception:
            return 4.0

    def extract_interval_preferences(self, audio_path: str) -> Dict[int, float]:
        """
        Interval preference histogram (semitone → relative frequency).
        Derived from dominant-frequency deltas across short windows.
        """
        samples, sr = self._load_audio(audio_path)
        if samples is None:
            return {2: 0.35, 1: 0.20, 3: 0.15, 4: 0.10, 5: 0.07, 7: 0.08, 12: 0.05}
        try:
            import numpy as np
            window = int(sr * 0.1)   # 100 ms windows
            hop = window
            freqs_hz: List[float] = []
            for i in range(0, len(samples) - window, hop):
                seg = samples[i: i + window]
                fft = np.abs(np.fft.rfft(seg))
                bin_hz = sr / len(seg)
                lo = max(1, int(80 / bin_hz))
                hi = min(len(fft) - 1, int(2000 / bin_hz))
                if hi <= lo:
                    continue
                dom = lo + int(np.argmax(fft[lo: hi + 1]))
                freq_hz = dom * bin_hz
                freqs_hz.append(freq_hz)
            if len(freqs_hz) < 2:
                return {2: 0.35, 1: 0.20, 3: 0.15, 4: 0.10, 5: 0.07, 7: 0.08, 12: 0.05}
            # Convert to semitone intervals
            intervals: List[int] = []
            for a, b in zip(freqs_hz, freqs_hz[1:]):
                if a > 0 and b > 0:
                    semi = abs(round(12 * np.log2(b / a)))
                    if 0 < semi <= 24:
                        intervals.append(int(semi))
            if not intervals:
                return {2: 0.35, 1: 0.20, 3: 0.15, 4: 0.10, 5: 0.07, 7: 0.08, 12: 0.05}
            counts: Dict[int, int] = {}
            for iv in intervals:
                counts[iv] = counts.get(iv, 0) + 1
            total = sum(counts.values())
            return {iv: round(cnt / total, 3) for iv, cnt in sorted(counts.items())}
        except Exception:
            return {2: 0.35, 1: 0.20, 3: 0.15, 4: 0.10, 5: 0.07, 7: 0.08, 12: 0.05}

    def map_emotional_arc(self, audio_path: str) -> List[str]:
        """
        Map emotional arc labels per section using RMS energy trajectory.
        """
        samples, sr = self._load_audio(audio_path)
        if samples is None:
            return ["calm", "energetic", "dramatic", "calm"]
        try:
            import numpy as np
            n_sections = 4
            sec_len = len(samples) // n_sections
            if sec_len == 0:
                return ["calm", "energetic", "dramatic", "calm"]
            rms_vals = [
                float(np.sqrt(np.mean(samples[i * sec_len: (i + 1) * sec_len] ** 2)))
                for i in range(n_sections)
            ]
            max_rms = max(rms_vals) or 1.0
            arc: List[str] = []
            for rms in rms_vals:
                ratio = rms / max_rms
                if ratio > 0.8:
                    arc.append("dramatic")
                elif ratio > 0.5:
                    arc.append("energetic")
                elif ratio > 0.25:
                    arc.append("bright")
                else:
                    arc.append("calm")
            return arc
        except Exception:
            return ["calm", "energetic", "dramatic", "calm"]

    # ── Private helpers ────────────────────────────────────────────────────

    def _load_audio(self, path: str) -> Tuple[Optional[object], int]:
        """
        Attempt to load audio from *path* using scipy or numpy.
        Returns (samples_array, sample_rate) or (None, 0) on failure.
        """
        try:
            try:
                from scipy.io import wavfile
                import numpy as np
                rate, data = wavfile.read(path)
                if data.ndim > 1:
                    data = data[:, 0]
                samples = data.astype(np.float32)
                if samples.max() > 1.0:
                    samples = samples / 32768.0
                return samples, int(rate)
            except ImportError:
                pass
            try:
                import numpy as np
                data = np.frombuffer(open(path, "rb").read(), dtype=np.int16)
                return data.astype(np.float32) / 32768.0, 44100
            except Exception:
                pass
        except Exception:
            pass
        return None, 0

    def _classify_contour(self, freq_segments: List[float]) -> str:
        """Given frequency proxy values per segment, return a contour label."""
        if not freq_segments or len(freq_segments) < 3:
            return "arch"
        mid = len(freq_segments) // 2
        first_half_avg = sum(freq_segments[:mid]) / mid
        second_half_avg = sum(freq_segments[mid:]) / (len(freq_segments) - mid)
        overall_start = freq_segments[0]
        overall_end = freq_segments[-1]
        peak_pos = freq_segments.index(max(freq_segments)) / len(freq_segments)
        trough_pos = freq_segments.index(min(freq_segments)) / len(freq_segments)
        if 0.3 <= peak_pos <= 0.75 and freq_segments[0] < max(freq_segments) * 0.8:
            return "arch"
        if 0.25 <= trough_pos <= 0.7 and freq_segments[0] > min(freq_segments) * 1.2:
            return "inverted_arch"
        if second_half_avg > first_half_avg * 1.1:
            return "ascending"
        if second_half_avg < first_half_avg * 0.9:
            return "descending"
        return "wave"

    def _estimate_peak_moments(
        self, phrasing: float, arc: List[str]
    ) -> List[Tuple[int, float]]:
        """Estimate (bar, beat) peak positions from phrasing and emotional arc."""
        peaks: List[Tuple[int, float]] = []
        n_sections = max(1, len(arc))
        bars_per_section = max(1, int(phrasing))
        for s_idx, label in enumerate(arc):
            if label in ("dramatic", "energetic"):
                bar = s_idx * bars_per_section + max(1, bars_per_section // 2)
                peaks.append((bar, 1.0))
        return peaks


# Alias matching task spec
MelodicDNABlueprint = MelodicDNA

