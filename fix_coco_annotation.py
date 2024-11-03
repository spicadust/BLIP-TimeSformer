import json
import os
from pathlib import Path

def filter_annotations_by_existing_images():
    # Paths
    base_dir = Path('.')
    annotation_dir = base_dir / 'annotation/data/coco/full'
    coco_dir = base_dir / 'coco'
    
    # Create set of existing image files
    existing_images = set()
    for split in ['train2014', 'val2014', 'test2014']:
        split_dir = coco_dir / split
        if split_dir.exists():
            for img_file in split_dir.glob('*.jpg'):
                # Store relative path as it appears in annotations
                existing_images.add(f'{split}/{img_file.name}')
    
    print(f"Found {len(existing_images)} existing images")
    
    # Process each split
    splits = ['train', 'val', 'test']
    for split in splits:
        annotation_file = annotation_dir / f'coco_karpathy_{split}.json'
        if not annotation_file.exists():
            print(f"Warning: {annotation_file} not found")
            continue
            
        # Read annotations
        with open(annotation_file, 'r') as f:
            data = json.load(f)
        
        # Filter annotations
        original_count = len(data)
        filtered_data = [item for item in data if item['image'] in existing_images]
        filtered_count = len(filtered_data)
        
        # Save filtered annotations
        output_file = annotation_dir / f'coco_karpathy_{split}_filtered.json'
        with open(output_file, 'w') as f:
            json.dump(filtered_data, f)
            
        print(f"\n{split} split:")
        print(f"Original annotations: {original_count}")
        print(f"Filtered annotations: {filtered_count}")
        print(f"Removed {original_count - filtered_count} entries")
        print(f"Saved to {output_file}")

if __name__ == "__main__":
    filter_annotations_by_existing_images()
