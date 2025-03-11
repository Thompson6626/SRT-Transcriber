import subprocess

def embed_subtitles(video_file, subtitle_file, output_file):
    command = [
        "ffmpeg",
        "-i", video_file,      # Input video file
        "-f", "srt",           # Subtitle format
        "-i", subtitle_file,   # Input subtitle file
        "-map", "0:0",         # Map video stream
        "-map", "0:1",         # Map audio stream
        "-map", "1:0",         # Map subtitle stream
        "-c:v", "copy",        # Copy video (no re-encoding)
        "-c:a", "copy",        # Copy audio (no re-encoding)
        "-c:s", "srt",         # Convert subtitles to SRT format
        output_file            # Output MKV file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"✅ Subtitles embedded successfully into {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")

# Example usage:
embed_subtitles("input.mp4", "input.srt", "output.mkv")
