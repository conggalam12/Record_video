import subprocess
import argparse
from pathlib import Path
import os

def encode_video(input_file, crf=40, speed=4):
    input_path = Path(input_file)
    output_path = os.path.join('/home/atin/congnt/record_video/video_encoder', input_path.stem + '_av1.mp4')

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    command = [
        'ffmpeg',
        '-i', str(input_path),
        '-c:v', 'libaom-av1',
        '-crf', str(crf),
        '-b:v', '0',
        '-b:a', '64k',         # Giảm bitrate audio
        '-ac', '1',            # Chuyển sang mono audio
        '-vf', 'scale=iw*0.5:-1',  # Giảm kích thước video xuống 75%
        '-cpu-used', str(speed),
        '-row-mt', '1',
        '-tile-columns', '2',
        '-tile-rows', '2',
        '-strict', 'experimental',
        str(output_path)
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Encoding completed: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Encoding failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode video using AV1 codec with high compression")
    parser.add_argument("--input", default='/home/atin/congnt/test/onnx.mkv')
    parser.add_argument("--crf", type=int, default=40, help="CRF value (0-63, default: 40)")
    parser.add_argument("--speed", type=int, default=4, choices=range(9), help="Encoding speed (0-8, default: 4)")

    args = parser.parse_args()

    encode_video(args.input, args.crf, args.speed)