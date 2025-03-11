from pathlib import Path

import whisper
from io import BytesIO

# Models can be "base" , "medium" , "large" , "turbo"
model = whisper.load_model("base", device="cuda")

TRANSCRIPTIONS_DIR = Path("static/transcriptions")
TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)

import tempfile
import os


def transcribeMp3File(mp3_file: BytesIO, filename: str, language_code: str) -> Path:
    """Transcribes an MP3 file using Whisper and saves the output in SRT format."""

    # Ensure we start reading from the beginning
    mp3_file.seek(0)

    # Create a temporary MP3 file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_mp3_file:
        tmp_mp3_file.write(mp3_file.read())  # Write content
        tmp_mp3_file_path = tmp_mp3_file.name  # Store path

    try:
        # Transcribe using Whisper
        result = model.transcribe(audio=tmp_mp3_file_path, language=language_code)

        # Ensure segments exist
        if "segments" not in result:
            raise ValueError("Transcription failed: No segments returned.")

        # Generate the transcription file path
        saved_file_path = write_on_srt_format(result, filename)
        return saved_file_path

    finally:
        os.remove(tmp_mp3_file_path)  # Cleanup temp file


type Whisper_Result = dict[str, str | list[dict[str, int]]]


def write_on_srt_format(result: Whisper_Result, filename: str) -> Path:
    transcription_file_path = TRANSCRIPTIONS_DIR / f"{filename}.srt"

    # Write the transcription to an SRT file
    with open(transcription_file_path, "w", encoding="utf-8") as f:
        for idx, segment in enumerate(result["segments"], start=1):
            start_time = format_time_to_srt(segment["start"])
            end_time = format_time_to_srt(segment["end"])
            text = segment["text"].strip()
            f.write(f"{idx}\n{start_time} --> {end_time}\n{text}\n\n")

    print(f"Transcription saved: {transcription_file_path}")

    return transcription_file_path


def format_time_to_srt(seconds: float) -> str:
    """Convert seconds to SRT time format (HH:MM:SS,MMM)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_int = int(seconds % 60)
    milliseconds = round((seconds - int(seconds)) * 1000)  # Rounded to avoid floating-point issues

    return f"{hours:02}:{minutes:02}:{seconds_int:02},{milliseconds:03}"
