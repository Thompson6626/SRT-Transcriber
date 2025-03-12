from io import BytesIO
from pathlib import Path

import ffmpeg
from fastapi import UploadFile, HTTPException

class FileConverterService:

    async def convert_to_mp3(self, input_file: UploadFile) -> BytesIO:
        """
        Converts an uploaded audio file to MP3 format.

        If the file is already in MP3 format, it is returned as is.
        Otherwise, FFmpeg is used for conversion.
        """
        # Read file content into memory
        file_content = await input_file.read()
        inp_file = BytesIO(file_content)

        # Extract file extension using pathlib
        file_extension = Path(input_file.filename).suffix.lower()

        if file_extension == ".mp3":
            # Return the file as is, no conversion needed
            inp_file.seek(0)  # Reset to beginning before returning
            return inp_file

        try:
            # Output buffer to store the converted MP3 file in memory
            output_buffer = BytesIO()

            # FFmpeg conversion: input from stdin (pipe:0), output to stdout (pipe:1)
            process = (
                ffmpeg
                .input("pipe:0")
                .output("pipe:1", format="mp3", acodec="libmp3lame", audio_bitrate="192k")
                .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
            )

            # Write input file to FFmpeg stdin
            stdout, stderr = process.communicate(input=inp_file.read())

            if process.returncode != 0:
                raise RuntimeError(f"FFmpeg conversion failed: {stderr.decode()}")

            # Write converted data to output buffer
            output_buffer.write(stdout)
            output_buffer.seek(0)  # Reset to beginning before returning

            return output_buffer
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during MP3 conversion: {str(e)}")