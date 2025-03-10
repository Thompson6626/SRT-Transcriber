import vlc
import time

# Create an instance of VLC media player
player = vlc.MediaPlayer()

# Load an MKV file with embedded or external subtitles
media = vlc.Media("Ish.mkv")  # Replace with your MKV file path
player.set_media(media)

# Start playing the video
player.play()

# Wait for VLC to load and start the media
time.sleep(3)

# Get the number of available subtitle tracks
subtitle_tracks = player.video_get_spu()

if subtitle_tracks == -1:
    print("No subtitles available.")
else:
    print("Available subtitle tracks:")
    # Loop through the available tracks and print their descriptions (names)
    for track_id in range(subtitle_tracks):
        description = player.video_get_spu_description()
        print(f"Track {track_id}: {description}")

    # Optionally, select a specific subtitle (for example, track 0)
    player.set_spu(0)

# Let the video play for a few seconds
time.sleep(5)

# Stop the player
player.stop()
