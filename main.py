import whisper

print("Loading model...")
model = whisper.load_model("turbo", device="cuda")
print("Model loaded. Starting transcription...")

result = model.transcribe("Ishura.mp3", language="ja", verbose=True)

print("Transcription completed. Saving to file...")

with open("transcriptions/transcriptionishura.txt", "w", encoding="utf-8") as f:
    for segment in result["segments"]:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        f.write(f"[{start:.2f} --> {end:.2f}] {text}\n")

print("Transcription saved.")
