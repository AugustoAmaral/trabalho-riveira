from pathlib import Path
import cv2
import numpy as np

class DataHandler:
    def __init__(self, base_path="~/hand_dataset"):
        self.dataset_path = Path(base_path).expanduser()
        self._setup_directories()
        
    def _setup_directories(self):
        for fingers in range(6):  # 0 a 5 dedos
            finger_dir = self.dataset_path / f"{fingers}_fingers"
            finger_dir.mkdir(parents=True, exist_ok=True)
    
    def count_existing_images(self):
        total = 0
        for finger_dir in self.dataset_path.glob("*_fingers"):
            total += len(list(finger_dir.glob("*.png")))
        return total
    
    def save_training_image(self, image, box, fingers):
        finger_dir = self.dataset_path / f"{fingers}_fingers"
        existing = len(list(finger_dir.glob("*.png")))
        
        x1, y1, x2, y2 = box
        filename = f"{existing+1:04d}_{x1},{y1}_{x2},{y2}.png"
        filepath = finger_dir / filename
        
        cv2.imwrite(str(filepath), image)
        return filepath
    
    def load_dataset(self):
        images = []
        labels = []
        boxes = []
        
        for finger_count in range(6):
            finger_dir = self.dataset_path / f"{finger_count}_fingers"
            
            for img_path in finger_dir.glob("*.png"):
                # Extrair coordenadas do nome do arquivo
                parts = img_path.stem.split('_')
                coords1 = parts[1].split(',')
                coords2 = parts[2].split(',')
                
                box = [int(coords1[0]), int(coords1[1]), 
                       int(coords2[0]), int(coords2[1])]
                
                img = cv2.imread(str(img_path))
                if img is not None:
                    images.append(img)
                    labels.append(finger_count)
                    boxes.append(box)
        
        return images, labels, boxes