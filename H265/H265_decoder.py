import subprocess
import argparse
from pathlib import Path
import os

def encode_video(input_file, crf=23, preset='medium'):
    input_path = Path(input_file)
    output_path = os.path.join('/home/atin/congnt/record_video/video_decoder',input_path.name)

    command = [
        'ffmpeg',
        '-i', str(input_path),
        '-c:v', 'libx265',  # Sử dụng codec H.265
        '-crf', str(crf),   # Constant Rate Factor (CRF)
        '-preset', preset,  # Preset cho tốc độ mã hóa
        '-c:a', 'copy',     # Copy audio stream
        '-tag:v', 'hvc1',   # Thêm tag hvc1 để tương thích với một số player
        str(output_path)
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Encoding completed: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Encoding failed: {e}")
        print(f"Error output: {e.stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode video using H.265 codec")
    parser.add_argument("--input", default='/home/atin/congnt/record_video/video_encoder/onnx.mkv' ,help="Path to input video file")
    parser.add_argument("--crf", type=int, default=23, help="CRF value (0-51, default: 23)")
    parser.add_argument("--preset", default="medium", choices=['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'], help="Encoding preset (default: medium)")

    args = parser.parse_args()

    encode_video(args.input,args.crf, args.preset)