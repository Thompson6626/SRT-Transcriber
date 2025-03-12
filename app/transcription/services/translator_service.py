from functools import lru_cache

from transformers import MarianMTModel, MarianTokenizer

# Dictionary of available translation models
AVAILABLE_MODELS = {
    # Available
    "en-es": "Helsinki-NLP/opus-mt-en-es",
    "es-en": "Helsinki-NLP/opus-mt-es-en",
    "en-fr": "Helsinki-NLP/opus-mt-en-fr",
    "fr-en": "Helsinki-NLP/opus-mt-fr-en",
    "ja-en": "Helsinki-NLP/opus-mt-ja-en",
    "ru-en": "Helsinki-NLP/opus-mt-ru-en",
    # May not be available
    "ru-es": "Helsinki-NLP/opus-mt-ru-es",
    "ja-es": "Helsinki-NLP/opus-mt-ja-es",
}

class TranslatorService:

    @lru_cache(maxsize=3)  # Cache up to 10 language pairs
    def __load_model(self, language_pair: str):
        """Load the correct MarianMT model and tokenizer dynamically."""
        if language_pair not in AVAILABLE_MODELS:
            raise ValueError(f"Unsupported translation pair: {language_pair}")

        model_name = AVAILABLE_MODELS[language_pair]
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        return model, tokenizer

    def translate(self, text: str, origin_language: str, destination_language: str):
        """Translate text using the selected language pair."""
        language_pair = f"{origin_language}-{destination_language}"
        model, tokenizer = self.__load_model(language_pair)

        # Tokenize input text
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

        # Generate translation
        translated_tokens = model.generate(**inputs)

        # Decode the output
        return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]