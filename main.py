import subprocess
import argparse
import os

def encode_rtsp_video(input_rtsp, output_file, gpu_type="nvidia", crf=23, preset='medium'):
    """
    Encode video from RTSP stream using H.265 GPU acceleration.

    :param input_rtsp: RTSP stream URL.
    :param output_file: Path to the output video file (e.g., "output.mp4").
    :param gpu_type: Type of GPU ('nvidia' for NVIDIA or 'amd' for AMD).
    :param crf: CRF value (0-51), lower values mean higher quality.
    :param preset: Encoding speed (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow).
    """

    # Select the encoder based on GPU type
    if gpu_type.lower() == "nvidia":
        video_codec = "hevc_nvenc"
    elif gpu_type.lower() == "amd":
        video_codec = "hevc_amf"
    else:
        raise ValueError("Unsupported GPU type. Please use 'nvidia' or 'amd'.")

    # Build the FFmpeg command
    command = [
        "ffmpeg",
        "-rtsp_transport", "tcp",  # Use TCP as the transport protocol for RTSP
        "-i", input_rtsp,
        "-t","180",
        "-c:v", video_codec,       # Use H.265 encoding with GPU acceleration
        "-crf", str(crf),          # Set the CRF value
        "-preset", preset,         # Set the encoding speed
        "-c:a", "copy",            # Copy the audio without re-encoding
        "-f", "mp4",               # Set the output format to MP4
        output_file
    ]

    # Execute the FFmpeg command
    try:
        subprocess.run(command, check=True)
        print(f"Encoding completed: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Encoding failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode video from RTSP using GPU H.265")
    parser.add_argument("--input", default='rtsp://admin:T4123456@192.168.1.13:554/Streaming/Channels/1/', help="RTSP stream URL")
    parser.add_argument("--output", default="output.mp4", help="Path to the output video file")
    parser.add_argument("--gpu_type", default="nvidia", choices=["nvidia", "amd"], help="Type of GPU (nvidia or amd)")
    parser.add_argument("--crf", type=int, default=26, help="CRF value (0-51)")
    parser.add_argument("--preset", default="slow", choices=['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'], help="Encoding speed")

    args = parser.parse_args()

    encode_rtsp_video(args.input, args.output, args.gpu_type, args.crf, args.preset)
