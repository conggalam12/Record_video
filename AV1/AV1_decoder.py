import subprocess
import argparse
from pathlib import Path
import os

def decode_video(input_file, output_format='mp4'):
    input_path = Path(input_file)
    output_path = os.path.join('/home/atin/congnt/record_video/video_decoder', input_path.stem + f'_decoded.{output_format}')

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    command = [
        'ffmpeg',
        '-i', str(input_path),
        '-c:v', 'libx265',  # Sử dụng H.264 cho đầu ra để đảm bảo tương thích rộng rãi
        '-crf', '23',       # Chất lượng đầu ra tốt
        '-preset', 'medium',
        '-c:a', 'aac',      # Sử dụng AAC cho audio
        '-b:a', '128k',     # Bitrate audio
        str(output_path)
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Decoding completed: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Decoding failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decode AV1 video to a more compatible format")
    parser.add_argument("--input", default='/home/atin/congnt/record_video/video_encoder/onnx_av1.mp4', help="Path to the input AV1 video file")
    parser.add_argument("--format", default='mp4', choices=['mp4', 'mkv', 'avi'], help="Output format (default: mp4)")

    args = parser.parse_args()

    decode_video(args.input, args.format)