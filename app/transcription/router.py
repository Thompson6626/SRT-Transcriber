from io import BytesIO
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, Query, HTTPException
from fastapi.responses import FileResponse

from .dependencies import get_file_validator_service, get_file_converter_service, get_transcription_service
from .services import FileValidatorService, FileConverterService, TranscriptionService

import logging

# Set up logger
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/transcribe",
    tags=["transcription"]
)

AVAILABLE_MODEL_PAIRS = {
    ("en", "es"), ("es", "en"), ("en", "fr"), ("fr", "en"),
    ("ja", "en"), ("ru", "en"), ("ru", "es"), ("ja", "es")
}

@router.post("/srt")
async def transcribe_to_srt(
        file: UploadFile,
        file_validator: FileValidatorService = Depends(get_file_validator_service),
        file_converter: FileConverterService = Depends(get_file_converter_service),
        transcriber: TranscriptionService = Depends(get_transcription_service),
        origin_language: str = Query(..., min_length=2, max_length=5, regex="^[a-z]{2,5}$")
):
    """Endpoint to transcribe an audio file to SRT format using Whisper."""

    await file_validator.can_be_transformed_to_mp3(file)

    # Convert file to MP3 (await since it's an async operation)
    mp3_file: BytesIO = await file_converter.convert_to_mp3(file)

    # Extract filename without extension
    filename = Path(file.filename).stem

    # Perform transcription
    transcribed_file_path = transcriber.transcribe_to_normal_srt(mp3_file, filename, origin_language)

    return FileResponse(
        path=transcribed_file_path,
        filename=f"{filename}.srt",
        media_type="application/x-subrip"  # Correct MIME type for .srt files
    )

@router.post("/srt-romaji")
async def transcribe_to_srt_romaji(
        file: UploadFile,
        file_validator: FileValidatorService = Depends(get_file_validator_service),
        file_converter: FileConverterService = Depends(get_file_converter_service),
        transcriber: TranscriptionService = Depends(get_transcription_service),
):
    """Endpoint to transcribe an audio file to SRT format on romaji using Whisper."""

    await file_validator.can_be_transformed_to_mp3(file)

    # Convert file to MP3 (await since it's an async operation)
    mp3_file: BytesIO = await file_converter.convert_to_mp3(file)

    # Extract filename without extension
    filename = Path(file.filename).stem

    # Perform transcription
    transcribed_file_path = transcriber.transcribe_to_romaji_srt(mp3_file, filename, "ja")

    return FileResponse(
        path=transcribed_file_path,
        filename=f"{filename}.srt",
        media_type="application/x-subrip"  # Correct MIME type for .srt files
    )


@router.post("/srt-translated")
async def transcribe_to_srt_translated(
    file: UploadFile,
    destination_language_code: str = Query(..., min_length=2, max_length=5, regex="^[a-z]{2,5}$"),
    origin_language: str = Query(..., min_length=2, max_length=5, regex="^[a-z]{2,5}$"),
    file_validator: FileValidatorService = Depends(get_file_validator_service),
    file_converter: FileConverterService = Depends(get_file_converter_service),
    transcriber: TranscriptionService = Depends(get_transcription_service),
):
    if (origin_language, destination_language_code) not in AVAILABLE_MODEL_PAIRS:
        raise HTTPException(status_code=400, detail="Unsupported translation pair")
    
    await file_validator.can_be_transformed_to_mp3(file)  # Error

    # Convert file to MP3 (await since it's an async operation)
    mp3_file: BytesIO = await file_converter.convert_to_mp3(file)

    # Extract filename without extension
    filename = Path(file.filename).stem

    transcribed_file_path = transcriber.transcribe_to_translated_srt(mp3_file, filename, origin_language, destination_language_code)

    return FileResponse(
        path=transcribed_file_path,
        filename=f"{filename}.srt",
        media_type="application/x-subrip"  # Correct MIME type for .srt files
    )
