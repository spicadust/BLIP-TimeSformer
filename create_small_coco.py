import json
import random
import os
import shutil
from pathlib import Path
from tqdm import tqdm

def create_small_coco(ratio, dataset_name):
    # Paths
    base_dir = Path('.')
    annotation_dir = base_dir / 'annotation/data/coco'
    coco_dir = base_dir / 'coco'
    small_coco_dir = base_dir / dataset_name
    
    # Create directories if they don't exist
    small_coco_dir.mkdir(exist_ok=True)
    (small_coco_dir / 'train2014').mkdir(exist_ok=True)
    (small_coco_dir / 'val2014').mkdir(exist_ok=True)
    (small_coco_dir / 'test2014').mkdir(exist_ok=True)
    
    # Process each split
    splits = ['train', 'val', 'test']
    for split in splits:
        # Read annotations
        with open(f'{annotation_dir}/full/coco_karpathy_{split}.json', 'r') as f:
            data = json.load(f)
        
        # Randomly select subset
        print(f'Selecting {int(len(data) * ratio)} samples for {split} split from {len(data)} samples')
        num_samples = int(len(data) * ratio)
        selected_data = random.sample(data, num_samples)
        
        # Save new annotations
        # create a new directory for the small dataset
        small_annotation_dir = annotation_dir / dataset_name
        small_annotation_dir.mkdir(exist_ok=True)
        with open(small_annotation_dir / f'coco_karpathy_{split}.json', 'w') as f:
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
    
    dataset_name = 'coco_small'
    create_small_coco(ratio=0.1, dataset_name=dataset_name)
    
    print(f"Small COCO dataset {dataset_name} created successfully!")
