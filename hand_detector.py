import cv2
import numpy as np
import mediapipe as mp

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=10,  # Detecta até 10 mãos
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def detect_hands(self, frame, model_trainer):
        detections = []
        
        # Converter BGR para RGB (MediaPipe usa RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            h, w, _ = frame.shape
            
            for hand_landmarks in results.multi_hand_landmarks:
                # Obter bounding box da mão
                x_coords = [lm.x * w for lm in hand_landmarks.landmark]
                y_coords = [lm.y * h for lm in hand_landmarks.landmark]
                
                margin = 30
                x1 = max(0, int(min(x_coords)) - margin)
                y1 = max(0, int(min(y_coords)) - margin)
                x2 = min(w, int(max(x_coords)) + margin)
                y2 = min(h, int(max(y_coords)) + margin)
                
                # Classificar número de dedos se modelo disponível
                if model_trainer and model_trainer.model:
                    fingers, confidence = model_trainer.predict(frame, (x1, y1, x2, y2))
                    if fingers is not None:
                        detections.append(((x1, y1, x2, y2), fingers, confidence))
                else:
                    # Se não há modelo, apenas detectar sem classificar
                    detections.append(((x1, y1, x2, y2), -1, 0))
        
        return detections
    
    def get_hand_landmarks(self, frame):
        """Retorna landmarks para análise mais detalhada se necessário"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results.multi_hand_landmarks
    
    def draw_landmarks(self, frame, hand_landmarks):
        """Desenha os pontos da mão para debug"""
        self.mp_drawing.draw_landmarks(
            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)