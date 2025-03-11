from io import BytesIO
from pathlib import Path

from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse

from .whisper_transcribe import transcribeMp3File
from .validators import is_valid_transformable
from .converter import convert_to_mp3

router = APIRouter(
    prefix="/transcribe",
    tags=["transcription"]
)

@router.post("/srt")
async def transcribe_to_srt(file: UploadFile, language_code: str = None):
    """Endpoint to transcribe an audio file to SRT format using Whisper."""

    is_valid_transformable(file)

    # Convert file to MP3 (await since it's async)
    mp3_file: BytesIO = await convert_to_mp3(file)

    # Extract filename without extension
    filename = Path(file.filename).stem

    # Perform transcription
    transcribed_file_path = transcribeMp3File(mp3_file, filename, language_code)

    return FileResponse(
        path=transcribed_file_path,
        filename=f"{filename}.srt",
        media_type="application/x-subrip"  # Correct MIME type for .srt files
    )

@router.post("/srt-romaji")
async def transcribe_to_srt_romaji(file: UploadFile):
    # It will check if its japanese first (i'll perhaps add for other non latin writing systems)

    return None

@router.post("/srt-translated")
async def transcribe_to_srt_translated(file: UploadFile, language_code: str = None, destination_language_code: str = None):

    return None

@router.post("/txt")
async def transcribe_to_txt(language_code: str, file: UploadFile):

    return None
