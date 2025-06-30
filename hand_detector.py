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
        """Conta dedos levantados usando landmarks do MediaPipe com lógica melhorada"""
        fingers_up = 0
        
        # Pontos de referência dos dedos
        WRIST = 0
        THUMB_CMC = 1
        THUMB_MCP = 2
        THUMB_IP = 3
        THUMB_TIP = 4
        
        INDEX_MCP = 5
        INDEX_PIP = 6
        INDEX_DIP = 7
        INDEX_TIP = 8
        
        MIDDLE_MCP = 9
        MIDDLE_PIP = 10
        MIDDLE_DIP = 11
        MIDDLE_TIP = 12
        
        RING_MCP = 13
        RING_PIP = 14
        RING_DIP = 15
        RING_TIP = 16
        
        PINKY_MCP = 17
        PINKY_PIP = 18
        PINKY_DIP = 19
        PINKY_TIP = 20
        
        landmarks = hand_landmarks.landmark
        
        # Verificar se é mão direita ou esquerda
        is_right_hand = handedness.classification[0].label == 'Right'
        
        # Calcular orientação da mão (palma virada para câmera ou não)
        # Usando vetor do pulso para o meio da mão
        wrist_to_middle = (
            landmarks[MIDDLE_MCP].x - landmarks[WRIST].x,
            landmarks[MIDDLE_MCP].y - landmarks[WRIST].y,
            landmarks[MIDDLE_MCP].z - landmarks[WRIST].z
        )
        
        # Se z é negativo, a palma está virada para a câmera
        palm_facing_camera = wrist_to_middle[2] < 0
        
        # POLEGAR - lógica especial considerando movimento lateral
        # Calcular distância entre ponta do polegar e base do indicador
        thumb_to_index_base_x = abs(landmarks[THUMB_TIP].x - landmarks[INDEX_MCP].x)
        thumb_to_index_base_y = abs(landmarks[THUMB_TIP].y - landmarks[INDEX_MCP].y)
        
        # Threshold adaptativo baseado no tamanho da mão
        hand_scale = abs(landmarks[WRIST].y - landmarks[MIDDLE_TIP].y)
        thumb_threshold = hand_scale * 0.3
        
        # Polegar levantado se estiver afastado lateralmente
        if is_right_hand:
            if palm_facing_camera:
                if landmarks[THUMB_TIP].x < landmarks[THUMB_IP].x - 0.02:
                    fingers_up += 1
            else:
                if landmarks[THUMB_TIP].x > landmarks[THUMB_IP].x + 0.02:
                    fingers_up += 1
        else:
            if palm_facing_camera:
                if landmarks[THUMB_TIP].x > landmarks[THUMB_IP].x + 0.02:
                    fingers_up += 1
            else:
                if landmarks[THUMB_TIP].x < landmarks[THUMB_IP].x - 0.02:
                    fingers_up += 1
        
        # OUTROS DEDOS - verificar se estão estendidos
        fingers = [
            (INDEX_TIP, INDEX_DIP, INDEX_PIP, INDEX_MCP),
            (MIDDLE_TIP, MIDDLE_DIP, MIDDLE_PIP, MIDDLE_MCP),
            (RING_TIP, RING_DIP, RING_PIP, RING_MCP),
            (PINKY_TIP, PINKY_DIP, PINKY_PIP, PINKY_MCP)
        ]
        
        for tip, dip, pip, mcp in fingers:
            # Calcular se o dedo está estendido usando múltiplos pontos
            tip_y = landmarks[tip].y
            dip_y = landmarks[dip].y
            pip_y = landmarks[pip].y
            mcp_y = landmarks[mcp].y
            
            # Verificar se o dedo está dobrado calculando ângulos
            # Dedo levantado: ponta acima de todas as articulações
            if palm_facing_camera:
                # Palma para câmera - lógica normal
                if tip_y < dip_y - 0.01 and dip_y < pip_y:
                    fingers_up += 1
            else:
                # Dorso da mão para câmera - inverter lógica em alguns casos
                # Mas ainda verificar se está estendido
                finger_extended = (
                    abs(tip_y - mcp_y) > hand_scale * 0.3 and
                    tip_y < pip_y
                )
                if finger_extended:
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