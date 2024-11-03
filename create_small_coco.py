import json
import random
import os
import shutil
from pathlib import Path
from tqdm import tqdm

def create_small_coco(ratio=0.1):
    # Paths
    base_dir = Path('.')
    annotation_dir = base_dir / 'annotation'
    coco_dir = base_dir / 'coco'
    small_coco_dir = base_dir / 'coco_small'
    
    # Create directories if they don't exist
    small_coco_dir.mkdir(exist_ok=True)
    (small_coco_dir / 'train2014').mkdir(exist_ok=True)
    (small_coco_dir / 'val2014').mkdir(exist_ok=True)
    
    # Process each split
    splits = ['train', 'val', 'test']
    for split in splits:
        # Read annotations
        with open(annotation_dir / f'coco_karpathy_{split}.json', 'r') as f:
            data = json.load(f)
        
        # Randomly select subset
        num_samples = int(len(data) * ratio)
        selected_data = random.sample(data, num_samples)
        
        # Save new annotations
        with open(annotation_dir / f'coco_karpathy_{split}_small.json', 'w') as f:
            json.dump(selected_data, f)
        
        # Copy corresponding images
        print(f'Copying {len(selected_data)} images for {split} split')
        for item in tqdm(selected_data):
            img_path = item['image']  # e.g., 'val2014/COCO_val2014_000000184613.jpg'
            src_path = coco_dir / img_path
            dst_path = small_coco_dir / img_path
            
            if src_path.exists():
                shutil.copy2(src_path, dst_path)
            else:
                print(f"Warning: {src_path} not found")

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    
    # Create small dataset with 10% of original data
    create_small_coco(ratio=0.1)
    
    print("Small COCO dataset created successfully!")
