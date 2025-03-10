import ffmpeg

def convert_mkv_to_mp3(input_file, output_file):
    
    try:
        ffmpeg.input(input_file).output(output_file, acodec='libmp3lame', audio_bitrate='192k').run()
        print(f"Conversion successful: {output_file}")
    except ffmpeg.Error as e:
        print("Error during conversion:", e)

# Example usage
input_file = "ish.mkv"
output_file = "Ishura.mp3"
convert_mkv_to_mp3(input_file, output_file)
