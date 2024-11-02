import json
import shutil
import os
from pathlib import Path

def copy_matching_videos():
    # Create paths
    jsonl_path = "annotation/data/small_msrvtt_ret/msrvtt_test.jsonl"
    source_dir = "video_data"
    dest_dir = "small_video_data"
    
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    # Read clip names from JSONL file
    clip_names = set()
    with open(jsonl_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            clip_names.add(data['clip_name'])
    
    # Copy matching video files
    copied_count = 0
    for clip_name in clip_names:
        # Assuming videos are mp4 files
        source_file = os.path.join(source_dir, f"{clip_name}.mp4")
        dest_file = os.path.join(dest_dir, f"{clip_name}.mp4")
        
        if os.path.exists(source_file):
            shutil.copy2(source_file, dest_file)
            copied_count += 1
            print(f"Copied: {clip_name}.mp4")
        else:
            print(f"Warning: Source file not found: {clip_name}.mp4")
    
    print(f"\nCopying complete. Copied {copied_count} files.")

if __name__ == "__main__":
    copy_matching_videos()
