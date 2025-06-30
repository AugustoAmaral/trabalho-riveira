import cv2
import numpy as np

class CaptureManager:
    def __init__(self):
        self.selecting = False
        self.start_point = None
        self.end_point = None
        self.current_frame = None
        
    def capture_frame(self, frame):
        self.current_frame = frame.copy()
        self.selecting = False
        self.start_point = None
        self.end_point = None
        
        cv2.namedWindow('Capture')
        cv2.setMouseCallback('Capture', self._mouse_callback)
        
        print("\nClique e arraste para selecionar a mão")
        
        while True:
            display = self.current_frame.copy()
            
            # Desenhar retângulo de seleção
            if self.start_point and self.end_point:
                cv2.rectangle(display, self.start_point, self.end_point, (0, 0, 255), 2)
            
            cv2.imshow('Capture', display)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:  # ESC - cancelar
                cv2.destroyWindow('Capture')
                return None
                
            # Se seleção completa
            if self.start_point and self.end_point and not self.selecting:
                cv2.destroyWindow('Capture')
                
                # Solicitar número de dedos
                while True:
                    try:
                        fingers = int(input("Quantos dedos estão levantados (0-5)? "))
                        if 0 <= fingers <= 5:
                            break
                        print("Por favor, digite um número entre 0 e 5")
                    except ValueError:
                        print("Por favor, digite um número válido")
                
                # Normalizar coordenadas
                x1 = min(self.start_point[0], self.end_point[0])
                y1 = min(self.start_point[1], self.end_point[1])
                x2 = max(self.start_point[0], self.end_point[0])
                y2 = max(self.start_point[1], self.end_point[1])
                
                return {
                    'image': self.current_frame,
                    'box': (x1, y1, x2, y2),
                    'fingers': fingers
                }
    
    def _mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.selecting = True
            self.start_point = (x, y)
            self.end_point = None
            
        elif event == cv2.EVENT_MOUSEMOVE and self.selecting:
            self.end_point = (x, y)
            
        elif event == cv2.EVENT_LBUTTONUP:
            self.selecting = False
            self.end_point = (x, y)