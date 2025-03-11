import cutlet

def seconds_to_min(text_secs: str) -> str:
    left_num = text_secs[1:text_secs.find("-") - 1]
    right_num = text_secs[text_secs.find(">") + 2:text_secs.find("]")]

    return f"[{convert_time(left_num)} --> {convert_time(right_num)}]"


def convert_time(time: str) -> str:
    # First, convert the time to a float, as it can contain a decimal part
    time_float = float(time)

    # Split the seconds and milliseconds
    seconds = int(time_float)

    # Convert seconds to minutes and remaining seconds
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    # Return the formatted string
    return f"{minutes:02}:{remaining_seconds:02}"


cut = cutlet.Cutlet(system="hepburn")
cut.use_foreign_spelling = False

# Read the transcription file
with open("transcriptions/transcriptionishura.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Process each line and convert to romaji
time_lines = []
romaji_lines = []
for line in lines:
    # Split the text to remove timestamps and process only the Japanese text
    split = line.split("]")
    time, text = split  # Separating time and text
    time_lines.append(time)
    if text:  # Skip empty lines
        romaji = cut.romaji(text)
        romaji_lines.append(romaji)

# Print or save the romaji lines
with open("transcriptions/transcription_romaji_ishura.txt", "w", encoding="utf-8") as file:
    for tim, romaji in zip(time_lines, romaji_lines):
        file.write(f"{seconds_to_min(tim)}  {romaji}\n")

print("Romaji conversion completed and saved to 'transcription_romaji.txt'.")
