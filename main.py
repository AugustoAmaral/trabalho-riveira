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
        # Perguntar modo de execução
        print("\nSelecione o modo de execução:")
        print("1 - Modo Normal (detecção e classificação)")
        print("2 - Modo Treino Automático (gerar dataset com MediaPipe)")
        
        mode = input("\nEscolha (1 ou 2): ")
        
        if mode == '2':
            print("\n=== MODO TREINO AUTOMÁTICO ===")
            print("O MediaPipe detectará mãos e contará dedos automaticamente.")
            print("Pressione ESPAÇO para salvar as detecções atuais.")
            print("ESC para sair.")
            return 'training'
        
        # Modo normal
        existing_count = self.data_handler.count_existing_images()
        
        # Tentar carregar modelo existente primeiro
        if self.model_trainer.load_model():
            print("Modelo existente carregado!")
            self.model = self.model_trainer
        
        if existing_count > 0:
            print(f"\nEncontradas {existing_count} imagens no dataset.")
            response = input("Deseja treinar novo modelo com estas imagens? (s/n): ")
            
            if response.lower() == 's':
                print("Treinando modelo...")
                self.model = self.model_trainer.train(self.data_handler.dataset_path)
                if self.model:
                    print("Modelo treinado com sucesso!")
                else:
                    print("Aviso: Modelo não pôde ser treinado. Continuando sem classificação de dedos.")
        
        return 'normal'
    
    def run_training_mode(self):
        """Modo de treino automático usando MediaPipe"""
        print("\n[MODO TREINO] Posicione suas mãos e pressione ESPAÇO para capturar")
        saved_count = 0
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            display_frame = frame.copy()
            
            # Detectar mãos e contar dedos com MediaPipe
            detections = self.detector.detect_hands_with_finger_count(frame)
            
            # Desenhar detecções
            for detection in detections:
                x1, y1, x2, y2 = detection['box']
                fingers = detection['fingers']
                
                # Desenhar retângulo e contagem
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 255), 3)
                label = f"{fingers} dedos (MediaPipe)"
                cv2.putText(display_frame, label, (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                # Desenhar landmarks para visualização
                self.detector.draw_landmarks(display_frame, detection['landmarks'])
            
            # Mostrar estatísticas
            info_text = f"Modo Treino | Mãos: {len(detections)} | Salvos: {saved_count}"
            cv2.putText(display_frame, info_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Hand Recognition System - Training Mode', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:  # ESC
                break
            elif key == 32:  # ESPAÇO
                if detections:
                    # Salvar todas as detecções
                    for detection in detections:
                        self.data_handler.save_training_image(
                            frame,
                            detection['box'],
                            detection['fingers']
                        )
                        saved_count += 1
                    
                    print(f"Salvo! Total de imagens: {saved_count}")
                else:
                    print("Nenhuma mão detectada para salvar.")
        
        print(f"\nModo treino finalizado. {saved_count} imagens salvas.")
        print("Execute novamente no modo normal para treinar o modelo com estas imagens.")
    
    def run_normal_mode(self):
        """Modo normal de execução"""
        print("\nControles:")
        print("ESPAÇO - Capturar frame para treinamento manual")
        print("ESC - Sair")
        print("-" * 40)
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            display_frame = frame.copy()
            
            # Detectar e desenhar mãos
            detections = self.detector.detect_hands(frame, self.model)
            for box, fingers, confidence in detections:
                x1, y1, x2, y2 = box
                
                # Cor baseada em se há classificação ou não
                if fingers >= 0:
                    color = (0, 255, 0)  # Verde se classificado
                    label = f"{fingers} dedos ({confidence:.1%})"
                else:
                    color = (255, 165, 0)  # Laranja se apenas detectado
                    label = "Mão detectada"
                
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 3)
                cv2.putText(display_frame, label, (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
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
    
    def run(self):
        mode = self.initialize()
        
        if mode == 'training':
            self.run_training_mode()
        else:
            self.run_normal_mode()
        
        self.cleanup()
    
    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    system = HandRecognitionSystem()
    system.run()