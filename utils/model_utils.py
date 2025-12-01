import joblib
import pandas as pd
import numpy as np
import os

class HeartDiseasePredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model and scaler"""
        try:
            model_path = 'Model and EDA notebook/random_forest_model.pkl'
            scaler_path = 'Model and EDA notebook/scaler.pkl'
            
            if not os.path.exists(model_path):
                print(f"Model file not found at: {model_path}")
                return
            if not os.path.exists(scaler_path):
                print(f"Scaler file not found at: {scaler_path}")
                return
            
            # Load using joblib
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            
            print("Model and scaler loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            print(f"Current working directory: {os.getcwd()}")
    
    def predict(self, features):
        """Make prediction based on patient features"""
        if self.model is None or self.scaler is None:
            print("Model or scaler not loaded properly!")
            return None
            
        try:
            feature_order = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
                           'restecg', 'thalachh', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
            
            df = pd.DataFrame([features], columns=feature_order)
            scaled_features = self.scaler.transform(df)
            prediction = self.model.predict(scaled_features)[0]
            
            try:
                probability = self.model.predict_proba(scaled_features)[0]
                # Convert NumPy float64 to Python float
                risk_probability = float(probability[1])
            except:
                risk_probability = None
            
            return {
                'prediction': int(prediction),
                'risk_probability': risk_probability,
                'risk_level': 'High Risk' if prediction == 1 else 'Low Risk'
            }
        except Exception as e:
            print(f"Error making prediction: {e}")
            return None

predictor = HeartDiseasePredictor()