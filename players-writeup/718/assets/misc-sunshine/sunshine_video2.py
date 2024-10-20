import os
import subprocess

file_format = "udp16_{}.bin"
file_range = range(1360, 1408)
valid_files = []


def analyze_file(file_name):
    try:
        result = subprocess.run(
            ["ffprobe", file_name],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

        if "Invalid data" in result.stderr or "Invalid data" in result.stdout:
            return False
    except Exception as e:
        print(f"Error analyzing {file_name}: {e}")
        return False

    return True


def convert_to_mp4(file_name):
    output_file = file_name.replace(".bin", ".mp4")
    try:
        subprocess.run(
            ["ffmpeg", "-i", file_name, "-c:v", "libx264", "-f", "mp4", output_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Converted {file_name} to {output_file}")
    except Exception as e:
        print(f"Error converting {file_name}: {e}")


for i in file_range:
    file_name = file_format.format(i)
    if os.path.exists(file_name):
        if analyze_file(file_name):
            valid_files.append(file_name)
            convert_to_mp4(file_name)

if valid_files:
    print("Valid files without 'Invalid data':")
    for valid_file in valid_files:
        print(valid_file)
else:
    print("No valid files found.")
