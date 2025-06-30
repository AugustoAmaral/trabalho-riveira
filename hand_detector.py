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
    
    def detect_hands_with_finger_count(self, frame):
        """Detecta mãos e conta dedos usando apenas MediaPipe"""
        detections = []
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            h, w, _ = frame.shape
            
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Obter bounding box
                x_coords = [lm.x * w for lm in hand_landmarks.landmark]
                y_coords = [lm.y * h for lm in hand_landmarks.landmark]
                
                margin = 30
                x1 = max(0, int(min(x_coords)) - margin)
                y1 = max(0, int(min(y_coords)) - margin)
                x2 = min(w, int(max(x_coords)) + margin)
                y2 = min(h, int(max(y_coords)) + margin)
                
                # Contar dedos levantados
                finger_count = self._count_fingers(hand_landmarks, results.multi_handedness[hand_idx])
                
                detections.append({
                    'box': (x1, y1, x2, y2),
                    'fingers': finger_count,
                    'landmarks': hand_landmarks
                })
        
        return detections
    
    def _count_fingers(self, hand_landmarks, handedness):
        """Conta dedos levantados usando landmarks do MediaPipe"""
        fingers_up = 0
        
        # Pontos de referência dos dedos (tips e PIPs)
        THUMB_TIP = 4
        THUMB_IP = 3
        INDEX_TIP = 8
        INDEX_PIP = 6
        MIDDLE_TIP = 12
        MIDDLE_PIP = 10
        RING_TIP = 16
        RING_PIP = 14
        PINKY_TIP = 20
        PINKY_PIP = 18
        
        landmarks = hand_landmarks.landmark
        
        # Verificar se é mão direita ou esquerda
        is_right_hand = handedness.classification[0].label == 'Right'
        
        # Polegar - lógica diferente pois move lateralmente
        if is_right_hand:
            if landmarks[THUMB_TIP].x > landmarks[THUMB_IP].x:
                fingers_up += 1
        else:
            if landmarks[THUMB_TIP].x < landmarks[THUMB_IP].x:
                fingers_up += 1
        
        # Outros dedos - verificar se a ponta está acima do PIP
        finger_tips = [INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
        finger_pips = [INDEX_PIP, MIDDLE_PIP, RING_PIP, PINKY_PIP]
        
        for tip, pip in zip(finger_tips, finger_pips):
            if landmarks[tip].y < landmarks[pip].y:  # Y cresce para baixo
                fingers_up += 1
        
        return fingers_up
    
    def get_hand_landmarks(self, frame):
        """Retorna landmarks para análise mais detalhada se necessário"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results.multi_hand_landmarks
    
    def draw_landmarks(self, frame, hand_landmarks):
        """Desenha os pontos da mão para debug"""
        self.mp_drawing.draw_landmarks(
            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)