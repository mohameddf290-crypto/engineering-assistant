"""
Stem Handler — Full songs, individual stems, and bus stems.
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This module manages the ingestion, validation, and organisation of all
audio submissions from the user: full mix files, individual instrument
stems, and bus stems. It ensures that every checkpoint and analysis
pipeline receives properly formatted, validated audio data.

Protocol:
  1. Accept audio file paths from the user for full mixes, stems, and
     bus stems.
  2. Validate each file: exists, readable, correct format, expected
     sample rate, non-zero duration.
  3. Organise into a structured StemBundle for use by analysis pipelines.
  4. Support re-submission of individual stems (for verification loops).
  5. Log every acceptance and rejection explicitly.
"""

# TODO: Design this brain with Cursor — define the validation rules,
# the StemBundle schema, and the re-submission handling before writing
# any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class StemBundle:
    """
    A validated set of audio files for a single checkpoint or analysis run.

    Attributes:
        full_mix_path: Path to the full mix audio file.
        stem_paths: Dict of instrument_name → individual stem path.
        bus_stem_paths: Dict of bus_name → bus stem path.
        sample_rate: Sample rate of all files in this bundle (must match).
        duration: Duration of the full mix in seconds.
        submission_type: "checkpoint_1", "checkpoint_2", "verification",
            or "source_check".
    """

    full_mix_path: str
    stem_paths: Dict[str, str] = field(default_factory=dict)
    bus_stem_paths: Dict[str, str] = field(default_factory=dict)
    sample_rate: int = 44100
    duration: float = 0.0
    submission_type: str = "checkpoint_1"


class StemHandler:
    """
    Handles ingestion, validation, and organisation of all audio
    submissions from the user.
    """

    SUPPORTED_FORMATS = {".wav", ".aiff", ".flac", ".mp3"}

    def __init__(self, expected_sample_rate: int = 44100) -> None:
        self.expected_sample_rate = expected_sample_rate

    # ── Bundle creation ───────────────────────────────────────────────────────

    def create_bundle(
        self,
        full_mix_path: str,
        stem_paths: Dict[str, str],
        bus_stem_paths: Dict[str, str],
        submission_type: str = "checkpoint_1",
    ) -> StemBundle:
        """
        Validate all provided audio paths and assemble a StemBundle.

        TODO: Validate every file path (exists, readable, supported format,
        correct sample rate). Raise a descriptive error for any validation
        failure — do not silently skip invalid files. Return the assembled
        StemBundle.
        """
        raise NotImplementedError(
            "TODO: Implement stem bundle creation with full validation."
        )

    # ── Single stem submission (for verification loops) ───────────────────────

    def submit_single_stem(
        self, instrument_name: str, stem_path: str
    ) -> Dict[str, str]:
        """
        Validate and return a single stem submission for a verification
        loop re-submission.

        TODO: Validate the file, return a single-entry dict suitable for
        passing to the VerificationSystem.
        """
        raise NotImplementedError(
            "TODO: Implement single stem re-submission validation."
        )

    # ── Validation ────────────────────────────────────────────────────────────

    def validate_audio_file(self, file_path: str) -> bool:
        """
        Validate a single audio file: exists, readable, supported format,
        and correct sample rate.

        TODO: Implement full validation. Return True if valid. Raise a
        descriptive ValueError if invalid — do not return False silently.
        """
        raise NotImplementedError(
            "TODO: Implement audio file validation."
        )

    def get_audio_metadata(self, file_path: str) -> Dict:
        """
        Return metadata for an audio file: sample rate, duration,
        number of channels, bit depth.

        TODO: Use librosa or soundfile to extract metadata.
        """
        raise NotImplementedError(
            "TODO: Implement audio metadata extraction."
        )
