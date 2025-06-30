import cv2
import numpy as np

class HandDetector:
    def __init__(self):
        self.min_area = 5000  # Área mínima para considerar uma mão
        
    def detect_hands(self, frame, model_trainer):
        detections = []
        
        # Converter para HSV para melhor detecção de pele
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Range de cor de pele em HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Criar máscara
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Aplicar operações morfológicas
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            if area > self.min_area:
                # Obter bounding box
                x, y, w, h = cv2.boundingRect(contour)
                
                # Adicionar margem
                margin = 20
                x1 = max(0, x - margin)
                y1 = max(0, y - margin)
                x2 = min(frame.shape[1], x + w + margin)
                y2 = min(frame.shape[0], y + h + margin)
                
                # Classificar número de dedos
                fingers, confidence = model_trainer.predict(frame, (x1, y1, x2, y2))
                
                if fingers is not None:
                    detections.append(((x1, y1, x2, y2), fingers, confidence))
        
        return detections
    
    def detect_hands_simple(self, frame):
        """Versão simplificada para quando não há modelo treinado"""
        detections = []
        
        # Mesma detecção de pele
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_area:
                x, y, w, h = cv2.boundingRect(contour)
                detections.append(((x, y, x+w, y+h), -1, 0))  # -1 indica sem classificação
        
        return detections