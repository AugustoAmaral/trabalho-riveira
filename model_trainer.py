import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from skimage.feature import hog
import pickle
from pathlib import Path
from data_handler import DataHandler

class ModelTrainer:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = Path("hand_model.pkl")
        self.scaler_path = Path("hand_scaler.pkl")
        
    def extract_features(self, image, box):
        x1, y1, x2, y2 = box
        roi = image[y1:y2, x1:x2]
        
        # Redimensionar para tamanho fixo
        roi_resized = cv2.resize(roi, (64, 128))
        roi_gray = cv2.cvtColor(roi_resized, cv2.COLOR_BGR2GRAY)
        
        # Extrair features HOG
        features = hog(roi_gray, orientations=9, pixels_per_cell=(8, 8),
                      cells_per_block=(2, 2), block_norm='L2-Hys')
        
        return features
    
    def train(self, dataset_path):
        data_handler = DataHandler(dataset_path)
        images, labels, boxes = data_handler.load_dataset()
        
        if len(images) < 10:
            print(f"Apenas {len(images)} imagens encontradas. Mínimo de 10 necessário.")
            return None
        
        # Extrair features
        features = []
        valid_labels = []
        
        for img, label, box in zip(images, labels, boxes):
            try:
                feat = self.extract_features(img, box)
                features.append(feat)
                valid_labels.append(label)
            except Exception as e:
                print(f"Erro ao processar imagem: {e}")
                continue
        
        if len(features) < 10:
            print("Não há features suficientes para treinar.")
            return None
        
        X = np.array(features)
        y = np.array(valid_labels)
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Normalizar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treinar modelo SVM
        self.model = SVC(kernel='rbf', probability=True, C=10, gamma='scale')
        self.model.fit(X_train_scaled, y_train)
        
        # Avaliar
        accuracy = self.model.score(X_test_scaled, y_test)
        print(f"Acurácia no conjunto de teste: {accuracy:.2%}")
        
        # Salvar modelo
        self.save_model()
        
        return self
    
    def predict(self, image, box):
        if self.model is None:
            return None, 0
            
        try:
            features = self.extract_features(image, box)
            features_scaled = self.scaler.transform([features])
            
            prediction = self.model.predict(features_scaled)[0]
            confidence = np.max(self.model.predict_proba(features_scaled))
            
            return prediction, confidence
        except:
            return None, 0
    
    def save_model(self):
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
    
    def load_model(self):
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            return True
        except:
            return False