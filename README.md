# Audio Transcription and Translation API

This project is a FastAPI-based web service that allows you to transcribe audio files (e.g., MP3) into subtitles (SRT format), with optional translation and transcription features. It also supports converting transcription results to Romaji.

## Features

- **Transcribe audio to SRT:** Converts audio to subtitle format (`.srt`), including timestamps.
- **Transcribe to Romaji:** Transcribes Japanese audio into SRT with Romaji characters.
- **Translate Transcription:** Translates the transcription into a specified target language, providing subtitles in the translated language.
- **Future Features (Planned):** 
  - SRT-to-Romaji transformation (not yet implemented)

## Requirements

- **Python 3.7+**
- **FastAPI**
- **Uvicorn** (for running the server)
- **Faster-Whisper** a reimplementation of OpenAI's Whisper model using CTranslate2,
- **MarianMT** (Hugging Face's translation model) for translation
- **Cutlet** for japanese to romaji conversion

## Installation

## Important Notice

Unlike openai-whisper, FFmpeg does not need to be installed on the system. The audio is decoded with the Python library PyAV which bundles the FFmpeg libraries in its package.

### GPU

GPU execution requires the following NVIDIA libraries to be installed:

* [cuBLAS for CUDA 12](https://developer.nvidia.com/cublas)
* [cuDNN 9 for CUDA 12](https://developer.nvidia.com/cudnn)

For more information see faster-whisper's repository https://github.com/SYSTRAN/faster-whisper.

### Clone the repository

```bash
git clone https://github.com/Thompson6626/SRT-Transcriber.git
cd your-repo-name
```

### Set up the environment

1. **Create a virtual environment** (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate  # For Windows
```

2. **Install the required dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables** (if applicable) for any external services you are using like Whisper or MarianMT.


---

## Endpoints

### 1. **transcribe/srt** (POST)
Transcribe an audio file into SRT subtitle format using the Whisper model.

#### Request:
- **file** (required): The audio file (MP3) to transcribe.
- **origin_language**: The language of the audio file (e.g., `ja` for Japanese).

#### Response:
Returns a `.srt` file with transcribed subtitles.

### 2. **transcribe/srt-romaji** (POST)
Transcribe a Japanese audio file into SRT subtitles with Romaji text.

#### Request:
- **file** (required): The audio file (MP3) to transcribe.

#### Response:
Returns a `.srt` file with Romaji subtitles.

### 3. **transcribe/srt-translated** (POST)
Transcribe an audio file into SRT subtitles, then translate the transcription to a specified target language.

#### Request:
- **file** (required): The audio file (MP3) to transcribe.
- **origin_language** (required): The language of the audio file (e.g., `ja` for Japanese).
- **destination_language_code** (required): The target language code for translation (e.g., `en` for English).

#### Response:
Returns a `.srt` file with translated subtitles.

### 4. **/srt-to-romaji** (Planned)
Convert SRT subtitles into Romaji for Japanese audio.

#### Request:
- **file** (required): The SRT file to transform into Romaji.

#### Response:
Returns a `.srt` file with Romaji subtitles (coming soon).
|

---

## Example Requests

### Example for `transcribe/srt` endpoint:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/transcribe/srt?origin_language=ja' \
  -F 'file=@path_to_audio.mp3'
```

### Example for `transcribe/srt-translated` endpoint:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/transcribe/srt-translated?origin_language=ja&destination_language_code=en' \
  -F 'file=@path_to_audio.mp3'
```

Or just use postman or any other API client

## Running the Application

To start the FastAPI server:

```bash
fastapi dev app/main.py
```

By default, the API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

You can check the automatic API documentation by visiting [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
"""

---

## Testing the Application

You can test the application using any HTTP client (e.g., [Postman](https://www.postman.com/) or [curl](https://curl.se/)) to send POST requests to the available endpoints. For example, to test the `transcribe/srt` endpoint, you can use the `curl` command from above.

# TODO

Planning to add srt specific endpoint and add the Deepl api as translator too.
And of course improving it further.
