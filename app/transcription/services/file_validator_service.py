import mimetypes
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {
    ".mp3",  # MP3
    ".wav",  # WAV
    ".flac", # FLAC
    ".aac",  # AAC
    ".ogg",  # OGG
    ".m4a",  # M4A (Apple AAC)
    ".opus", # Opus
    ".wma",  # WMA
    ".mp4",  # MP4 (if it contains audio)
    ".avi",  # AVI (if it contains audio)
    ".mkv",  # MKV (if it contains audio)
    ".mov",  # MOV (if it contains audio)
}

ALLOWED_MIME_TYPES = {
    "audio/mpeg",      # MP3
    "audio/wav",       # WAV
    "audio/x-wav",     # WAV alternative
    "audio/flac",      # FLAC
    "audio/x-flac",    # FLAC alternative
    "audio/aac",       # AAC
    "audio/x-aac",     # AAC alternative
    "audio/ogg",       # OGG
    "audio/x-ogg",     # OGG alternative
    "audio/mp4",       # MP4 audio
    "audio/x-m4a",     # M4A (Apple AAC)
    "audio/opus",      # Opus
    "audio/x-opus",    # Opus alternative
    "audio/x-ms-wma",  # WMA
    "video/mp4",       # MP4 (if audio track exists)
    "video/x-msvideo", # AVI (if audio track exists)
    "video/x-matroska",# MKV (if audio track exists)
    "video/quicktime", # MOV (if audio track exists)
}


class FileValidatorService:

    async def can_be_transformed_to_mp3(self, file: UploadFile):
        mime_type, _ = mimetypes.guess_type(file.filename)

        if mime_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400,
                                detail=f"Invalid file format. Allowed: {', '.join(ALLOWED_MIME_TYPES)}")

        extension_with_dot = f".{file.filename.rsplit(".", maxsplit=1)[-1]}"

        if extension_with_dot not in ALLOWED_EXTENSIONS:
            return HTTPException(status_code=400,
                                 detail=f"Invalid file format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")


    def is_srt(self, file: UploadFile):
        return None
