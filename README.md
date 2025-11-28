# 🫀 Ventro - Heart Disease Risk Assessment System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Dash](https://img.shields.io/badge/Dash-2.0+-green.svg)
![ML](https://img.shields.io/badge/ML-Random%20Forest-red.svg)

> A machine learning-powered web application for rapid cardiovascular risk assessment in clinical settings.

**Developed by Team Health Horizon**

---

##  Overview

**Ventro** is a clinical decision support system that helps healthcare professionals assess heart disease risk quickly and accurately. Using a trained Random Forest machine learning model, the system analyzes 13 key cardiovascular parameters to provide instant risk predictions with percentage probabilities in under 3 seconds.

### Key Features

-  **Instant Risk Assessment** - Results in < 3 seconds
-  **ML-Powered Predictions** - Random Forest classifier with 13 clinical features
-  **Professional Reports** - Exportable assessments for medical records
-  **Intuitive Interface** - User-friendly web application for healthcare providers
-  **Data Validation** - Real-time input checking and error prevention

---

## Technology Stack

- **Frontend**: Dash, Dash Bootstrap Components, HTML/CSS/JavaScript
- **Backend**: Python 3.8+, Flask, Pandas, NumPy
- **Machine Learning**: Scikit-learn, Random Forest Classifier, StandardScaler
- **Deployment**: Gunicorn WSGI server

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/ventro-heart-disease-assessment.git
cd ventro-heart-disease-assessment

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

The application will start on `http://localhost:8050`

---

## Usage

### For Healthcare Providers

1. **Access Application** - Navigate to `http://localhost:8050`
2. **Begin Assessment** - Click "Begin Assessment" button
3. **Enter Patient Data** - Fill in 13 clinical parameters across organized cards
4. **Submit** - Click "Predict Heart Disease Risk"
5. **Review Results** - View risk percentage, classification, and patient summary
6. **Export Report** - Download formatted text file for medical records (optional)
7. **New Assessment** - Click "New Assessment" to reset for next patient

### Clinical Parameters

The system collects 13 cardiovascular indicators:

**Personal & Vitals**: Age, Sex, Resting BP, Cholesterol, Max Heart Rate  
**Cardiac Symptoms**: Chest Pain Type, Resting ECG  
**Diagnostic Tests**: ST Depression, Fasting Blood Sugar, Exercise Angina  
**Advanced Measurements**: Slope, Number of Major Vessels (0-4), Thalassemia

---

## Project Structure
```
ventro-heart-disease-assessment/
├── main.py                      # Application entry point
├── requirements.txt             # Dependencies
├── assets/                      # CSS, JavaScript
├── Pages/
│   ├── HomePage/               # Landing page
│   ├── PatientDetails/         # Input form & validation
│   └── ResultsPage/            # Results display
├── utils/
│   └── model_utils.py          # ML model wrapper
└── Model and EDA notebook/
    ├── random_forest_model.pkl # Trained model
    └── scaler.pkl              # Feature scaler
```

---

## Machine Learning Model

- **Algorithm**: Random Forest Classifier
- **Features**: 13 normalized cardiovascular parameters
- **Output**: Binary classification (High Risk / Low Risk)
- **Probability**: Continuous risk score (0-100%)

### Risk Classification
- **High Risk**: ≥50% probability (displayed in red)
- **Low Risk**: <50% probability (displayed in green)

---

## Testing

### Sample Test Case - High Risk
```
Age: 65, Sex: Male, CP: 3, BP: 160, Chol: 280
FBS: 1, RestECG: 2, HR: 110, ExAng: 1
Oldpeak: 3.5, Slope: 2, Vessels: 3, Thal: 2
Expected: High Risk (>50%)
```

### Sample Test Case - Low Risk
```
Age: 35, Sex: Female, CP: 0, BP: 110, Chol: 180
FBS: 0, RestECG: 0, HR: 160, ExAng: 0
Oldpeak: 0.5, Slope: 0, Vessels: 0, Thal: 0
Expected: Low Risk (<50%)
```

<div align="center">

**Built by Team Health Horizon**

</div>
