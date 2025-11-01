# Health-Horizon
The Healthcare Predictive Analytics project uses machine learning to forecast healthcare outcomes, support patient risk prediction, and identify trends in health data. It helps professionals make informed decisions, improve patient care, and optimize resource management.
# Heart Attack Prediction System

Machine learning system to predict heart attack risk using Random Forest classification on clinical patient data.

## Dataset

603 patient records with 13 clinical features including age, sex, chest pain type, blood pressure, cholesterol, heart rate, and ECG results. Balanced classes (51.9% vs 48.1%).

## Installation
```bash
git clone https://github.com/MostafaAlwakeel129/Health-Horizon.git
pip install pandas numpy matplotlib seaborn scikit-learn scipy joblib jupyter
```

## Usage

### Training
```python
Heart_disease_model.ipynb
simply run the notebook cell by cell in order to train and save the model for usage
```

## Model Performance

Random Forest Classifier with 20 estimators and max depth of 5.

**Results:**
```
              precision    recall  f1-score   support
           0       0.85      0.89      0.87        65
           1       0.87      0.82      0.84        56
    accuracy                           0.86       121
   macro avg       0.86      0.86      0.86       121
weighted avg       0.86      0.86      0.86       121
```

**Overall Accuracy: 86%**

**Key Predictors:**
- Chest pain type (cp): 0.54 correlation
- Max heart rate (thalachh): -0.38 correlation
- Exercise angina (exang): -0.39 correlation


