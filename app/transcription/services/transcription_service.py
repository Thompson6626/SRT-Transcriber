import logging
import os
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Callable
import torch
from faster_whisper import WhisperModel

from .text_converter_service import TextConverterService
from .translator_service import TranslatorService

TRANSCRIPTIONS_DIR = Path("static/transcriptions")
TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class TranscriptionService:
    def __init__(self, text_converter_service: TextConverterService, translator: TranslatorService):
        
        # Check if CUDA is available; fallback to CPU if not
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load the Whisper model
        self.model = WhisperModel("medium", device=device, compute_type="float16" if device == "cuda" else "float32")
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
        mp3_file.seek(0)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_mp3:
            tmp_mp3.write(mp3_file.read())
            tmp_mp3_path = tmp_mp3.name
        
        try:
            segments, _ = self.model.transcribe(tmp_mp3_path, language=language_code, word_timestamps=True,beam_size=5)
            result = [{"start": segment.start, "end": segment.end, "text": segment.text} for segment in segments]
            
            saved_file = save_format(result, filename, **(
                {"destination_language_code": destination_language_code} if destination_language_code else {}
            ))
            return saved_file
        
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            raise e
        
        finally:
            if os.path.exists(tmp_mp3_path):
                os.remove(tmp_mp3_path)

    def write_normal_srt(self, result: list[dict], filename: str) -> Path:
        return self.__write_srt_file(result, filename)

    def write_romaji_srt(self, result: list[dict], filename: str) -> Path:
        return self.__write_srt_file(result, filename, self.text_converter.to_romaji)

    def write_translated_srt(self, result: list[dict], filename: str, destination_language_code: str) -> Path:
        return self.__write_srt_file(
            result,
            filename,
            lambda text: self.text_translator.translate(text, "auto", destination_language_code)
        )

    def __write_srt_file(self, result: list[dict], filename: str, text_modif: Callable[[str], str] = None) -> Path:
        srt_file_path = TRANSCRIPTIONS_DIR / f"{filename}.srt"

        with open(srt_file_path, "w", encoding="utf-8") as f:

            for index, segment in enumerate(result, start=1):
                start_time = self.__format_time_to_srt(float(segment["start"]))
                end_time = self.__format_time_to_srt(float(segment["end"]))
                text = segment["text"].strip()
                

                if text_modif: text = text_modif(text)

                f.write(f"{index}\n{start_time} --> {end_time}\n{text}\n\n")

        return srt_file_path

    def __format_time_to_srt(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds_int = int(seconds % 60)
        milliseconds = round((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{seconds_int:02},{milliseconds:03}"
