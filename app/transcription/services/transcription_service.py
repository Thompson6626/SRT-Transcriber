import os
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Callable
import whisper
import torch

from .text_converter_service import TextConverterService
from .translator_service import TranslatorService

TRANSCRIPTIONS_DIR = Path("static/transcriptions")
TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)

# Result of Whi
type Whisper_Result = dict[str, str | list[dict[str, int]]]

class TranscriptionService:

    def __init__(self, text_converter_service: TextConverterService, translator: TranslatorService):
        # Models are found here https://github.com/openai/whisper
        
        # Check if CUDA is available; fallback to CPU if not
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load the Whisper model
        self.model = whisper.load_model("base", device=device)

        # Note: If you don't have an NVIDIA GPU with CUDA installed, 
        # forcing 'cuda' will result in an error. This setup automatically 
        # falls back to CPU when CUDA isn't available.
        
        self.text_converter = text_converter_service
        self.text_translator = translator

    def transcribe_to_normal_srt(self, mp3_file: BytesIO, filename: str, language_code: str) -> Path:
        return self.__transcribe_mp3_file(mp3_file, filename, language_code, self.write_normal_srt)

    def transcribe_to_romaji_srt(self, mp3_file: BytesIO, filename: str, language_code: str) -> Path:
        return self.__transcribe_mp3_file(mp3_file, filename, language_code, self.write_romaji_srt)

    def transcribe_to_translated_srt(self, mp3_file: BytesIO, filename: str, language_code: str, destination_language_code: str) -> Path:
        return self.__transcribe_mp3_file(mp3_file, filename, language_code, self.write_translated_srt, destination_language_code)

    def __transcribe_mp3_file(
        self,
        mp3_file: BytesIO,
        filename: str,
        language_code: str,
        save_format: Callable[..., Path],
        destination_language_code: str = None
) -> Path:
        """Transcribes an MP3 file and saves it in the specified format."""
        mp3_file.seek(0)  # Reset file pointer

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_mp3:
            tmp_mp3.write(mp3_file.read())
            tmp_mp3_path = tmp_mp3.name

        try:
            # Check if tmp_mp3_path is valid
            if not tmp_mp3_path or not os.path.exists(tmp_mp3_path):
                raise ValueError("Temporary MP3 file path is invalid.")

            result = self.model.transcribe(audio=tmp_mp3_path, language=language_code)

            if "segments" not in result:
                raise ValueError("Transcription failed: No segments returned.")

            # More pythonic way using the dictionary unpacking operator

            saved_file = save_format(result, filename, **(
                {"destination_language_code": destination_language_code} if destination_language_code else {}))
            return saved_file
        
        except Exception as e:
            # Log the exception (you can use a logging library or print the error message)
            print(f"An error occurred during transcription: {e}")
            raise e  # Re-raise the exception to propagate it if necessary

        finally:
            # Ensure the temporary file is deleted
            if os.path.exists(tmp_mp3_path):
                os.remove(tmp_mp3_path)



    def write_normal_srt(self, result: Whisper_Result, filename: str) -> Path:
        return self.__write_srt_file(result, filename)

    def write_romaji_srt(self, result: Whisper_Result, filename: str) -> Path:
        return self.__write_srt_file(result, filename, self.text_converter.to_romaji)

    def write_translated_srt(self, result: Whisper_Result, filename: str, destination_language_code: str) -> Path:
        return self.__write_srt_file(
            result,
            filename,
            lambda text: self.text_translator.translate(text, result["language"], destination_language_code))

    def __write_srt_file(
            self,
            result: Whisper_Result,
            filename: str,
            text_modif: Callable[[str], str] = None,
    ) -> Path:
        """
        SRT (SubRip Subtitle) Format:

        1. **Subtitle Index** - A sequential number starting from 1.
        2. **Time Range** - A timestamp indicating when the subtitle appears and disappears,
           formatted as `HH:MM:SS,mmm --> HH:MM:SS,mmm` (hours, minutes, seconds, milliseconds).
        3. **Subtitle Text** - The actual content of the subtitle.
        4. **Blank Line** - A blank line separates each subtitle entry.
        """
        srt_file_path = TRANSCRIPTIONS_DIR / f"{filename}.srt"
        with open(srt_file_path, "w", encoding="utf-8") as f:

            for index, segment in enumerate(result["segments"], start=1):
                start_time = self.__format_time_to_srt(float(segment["start"]))
                end_time = self.__format_time_to_srt(float(segment["end"]))
                text = segment["text"].strip()

                if text_modif: text = text_modif(text)

                f.write(f"{index}\n{start_time} --> {end_time}\n{text}\n\n")

        return srt_file_path



    def __format_time_to_srt(self, seconds: float) -> str:
        """Convert seconds to SRT time format (HH:MM:SS,MMM)."""

        SECONDS_PER_HOUR = 3600
        SECONDS_PER_MINUTE = 60
        MILLISECONDS_MULTIPLIER = 1000  # To convert fraction to milliseconds

        hours = int(seconds // SECONDS_PER_HOUR)
        minutes = int((seconds % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE)
        seconds_int = int(seconds % SECONDS_PER_MINUTE)
        milliseconds = round((seconds - int(seconds)) * MILLISECONDS_MULTIPLIER)

        return f"{hours:02}:{minutes:02}:{seconds_int:02},{milliseconds:03}"

