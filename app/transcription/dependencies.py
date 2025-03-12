from .services import FileValidatorService, FileConverterService, TranscriptionService, TextConverterService, \
    TranslatorService

file_validator_service = FileValidatorService()

async def get_file_validator_service():
    return file_validator_service

async def get_file_converter_service():
    return FileConverterService()

text_converter_service = TextConverterService()
text_translator_service = TranslatorService()
transcription_service = TranscriptionService(text_converter_service,text_translator_service)

async def get_text_converter_service() -> TextConverterService:
    return text_converter_service

async def get_transcription_service() -> TranscriptionService:
    return transcription_service
