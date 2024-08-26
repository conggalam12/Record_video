import subprocess
import argparse
from pathlib import Path
import os
import json

def encode_video(input_file, crf=23, preset='medium'):
    input_path = Path(input_file)
    output_path = os.path.join('/home/atin/congnt/record_video/video_encoder', input_path.stem + '_h265.mp4')

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    command = [
        'ffmpeg',
        '-i', str(input_path),
        '-c:v', 'libx265',
        '-crf', str(crf),
        '-preset', preset,
        '-c:a', 'copy',
        '-tag:v', 'hvc1',
        str(output_path)
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Encoding completed: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Encoding failed: {e}")
        return None

def calculate_bitrate(video_path):
    command = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        str(video_path)
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        video_info = json.loads(result.stdout)

        # Lấy bitrate từ thông tin format
        bitrate = int(video_info['format']['bit_rate'])
        
        # Chuyển đổi từ bits/second sang Mbps
        bitrate_mbps = bitrate / 1_000_000

        return bitrate_mbps

    except subprocess.CalledProcessError as e:
        print(f"Failed to get video information: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode video using H.265 codec and calculate bitrate")
    parser.add_argument("--input", default='/home/atin/congnt/record_video/rtsp/video/output_2.mp4')
    parser.add_argument("--crf", type=int, default=25, help="CRF value (0-51)")
    parser.add_argument("--preset", default="veryslow", choices=['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'], help="Encoding preset")

    args = parser.parse_args()

    output_path = encode_video(args.input, args.crf, args.preset)
    if output_path:
        bitrate = calculate_bitrate(output_path)
        if bitrate:
            print(f"Encoded video bitrate: {bitrate:.2f} Mbps")