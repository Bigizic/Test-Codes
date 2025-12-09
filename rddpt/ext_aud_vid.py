import ffmpeg
import os

def extract_audio(video_path):
    """
    extract audio from a video file and saves it as an MP3 file.
    the output file will have the same name as the video file but with .mp3 extension.
    """
    try:
        # determine output path
        base_name = os.path.splitext(video_path)[0]
        output_path = f"{base_name}.mp3"
        
        print(f"extracting audio from {video_path} to {output_path}...")
        
        # Run ffmpeg command
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(stream, output_path)
        ffmpeg.run(stream, overwrite_output=True)
        
        print("audio extraction successful!")
        return output_path
    except (ffmpeg.Error, Exception) as e:
        print(f"an error occurred: {e.stderr.decode() if e.stderr else str(e)}")
        raise
