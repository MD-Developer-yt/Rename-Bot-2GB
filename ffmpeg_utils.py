# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
import ffmpeg
import os

def add_metadata(input_path, output_path, title="", author="", artist="", audio="", subtitle="", video=""):
    try:
        stream = ffmpeg.input(input_path)

        metadata_args = []

        if title:
            metadata_args += ["-metadata", f"title={title}"]
        if author:
            metadata_args += ["-metadata", f"artist={author}"]
        if artist:
            metadata_args += ["-metadata", f"album_artist={artist}"]
        if audio:
            metadata_args += ["-metadata", f"comment={audio}"]
        if subtitle:
            metadata_args += ["-metadata", f"subtitle={subtitle}"]
        if video:
            metadata_args += ["-metadata", f"description={video}"]

        stream = ffmpeg.output(
            stream,
            output_path,
            vcodec="copy",
            acodec="copy"
        )

        stream = stream.global_args(*metadata_args)

        ffmpeg.run(stream, overwrite_output=True, quiet=True)

        return output_path

    except Exception as e:
        print("FFmpeg Error:", e)
        return input_path

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
