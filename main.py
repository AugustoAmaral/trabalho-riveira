#!/usr/bin/env python3
import cv2
import numpy as np
from pathlib import Path
from data_handler import DataHandler
from model_trainer import ModelTrainer
from hand_detector import HandDetector
from capture_manager import CaptureManager

class HandRecognitionSystem:
    def __init__(self):
        self.data_handler = DataHandler()
        self.model_trainer = ModelTrainer()
        self.detector = HandDetector()
        self.capture_manager = CaptureManager()
        
        self.cap = cv2.VideoCapture(0)
        self.model = None
        
    def initialize(self):
        existing_count = self.data_handler.count_existing_images()
        
        if existing_count > 0:
            print(f"\nEncontradas {existing_count} imagens no dataset.")
            response = input("Deseja treinar novo modelo com estas imagens? (s/n): ")
            
            if response.lower() == 's':
                print("Treinando modelo...")
                self.model = self.model_trainer.train(self.data_handler.dataset_path)
                if self.model:
                    print("Modelo treinado com sucesso!")
                else:
                    print("Aviso: Modelo não pôde ser treinado. Continuando sem detecção.")
        
    def run(self):
        print("\nControles:")
        print("ESPAÇO - Capturar frame para treinamento")
        print("ESC - Sair")
        print("-" * 40)
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            display_frame = frame.copy()
            
            # Detectar e desenhar mãos se modelo disponível
            if self.model:
                detections = self.detector.detect_hands(frame, self.model)
                for box, fingers, confidence in detections:
                    x1, y1, x2, y2 = box
                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    label = f"{fingers} dedos ({confidence:.1%})"
                    cv2.putText(display_frame, label, (x1, y1-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Hand Recognition System', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:  # ESC
                break
            elif key == 32:  # ESPAÇO
                captured_data = self.capture_manager.capture_frame(frame)
                if captured_data:
                    self.data_handler.save_training_image(
                        captured_data['image'],
                        captured_data['box'],
                        captured_data['fingers']
                    )
                    print(f"Imagem salva: {captured_data['fingers']} dedos")
                    
                    # Retreinar com nova imagem
                    response = input("Deseja retreinar o modelo agora? (s/n): ")
                    if response.lower() == 's':
                        print("Retreinando modelo...")
                        self.model = self.model_trainer.train(self.data_handler.dataset_path)
                        if self.model:
                            print("Modelo atualizado!")
        
        self.cleanup()
    
    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    system = HandRecognitionSystem()
    system.initialize()
    system.run()