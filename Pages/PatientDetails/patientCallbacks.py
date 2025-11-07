from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.model_utils import predictor

def patientCallbacks(app):
    """
    Register all callbacks for the Patient Details page.
    """
    
    @app.callback(
        Output('patient-output', 'children'),
        Output('prediction-store', 'data'),
        Output('url', 'pathname', allow_duplicate=True),
        Input('patient-button', 'n_clicks'),
        State('patient-age', 'value'),
        State('patient-sex', 'value'),
        State('patient-cp', 'value'),
        State('patient-trestbps', 'value'),
        State('patient-chol', 'value'),
        State('patient-fbs', 'value'),
        State('patient-restecg', 'value'),
        State('patient-thalachh', 'value'),
        State('patient-exang', 'value'),
        State('patient-oldpeak', 'value'),
        State('patient-slope', 'value'),
        State('patient-ca', 'value'),
        State('patient-thal', 'value'),
        prevent_initial_call=True
    )
    def predict_heart_disease(n_clicks, age, sex, cp, trestbps, chol, fbs, 
                             restecg, thalachh, exang, oldpeak, slope, ca, thal):
        
        print("=" * 50)
        print("CALLBACK TRIGGERED!")
        print(f"Button clicks: {n_clicks}")
        
        # Validate all inputs are provided
        inputs = [age, sex, cp, trestbps, chol, fbs, restecg, thalachh, 
                 exang, oldpeak, slope, ca, thal]
        input_names = ['Age', 'Sex', 'Chest Pain Type', 'Resting Blood Pressure', 
                      'Cholesterol', 'Fasting Blood Sugar', 'Resting ECG', 
                      'Maximum Heart Rate', 'Exercise Induced Angina', 
                      'ST Depression', 'Slope', 'Number of Vessels', 'Thalassemia']
        
        print(f"Received inputs: {inputs}")
        
        missing_fields = [name for name, value in zip(input_names, inputs) if value is None]
        
        if missing_fields:
            print(f"Missing fields: {missing_fields}")
            return (
                dbc.Alert([
                    html.H5("Missing Information", className="alert-heading"),
                    html.P(f"Please fill in the following fields: {', '.join(missing_fields)}")
                ], color="danger"),
                None,
                '/patient'
            )
        
        # ✅ Pass as list in correct order
        features = [age, sex, cp, trestbps, chol, fbs, restecg, 
                    thalachh, exang, oldpeak, slope, ca, thal]
        
        print(f"Features prepared: {features}")
        print(f"Predictor object: {predictor}")
        print(f"Model loaded: {predictor.model is not None}")
        print(f"Scaler loaded: {predictor.scaler is not None}")
        
        # Make prediction
        result = predictor.predict(features)
        
        print(f"Prediction result: {result}")
        
        if result is None:
            print("ERROR: Prediction returned None!")
            return (
                dbc.Alert([
                    html.H5("Prediction Error", className="alert-heading"),
                    html.P("There was an error making the prediction. Please check the terminal for details.")
                ], color="danger"),
                None,
                '/patient'
            )
        
        # Store result with all input data
        stored_data = {
            'prediction': result['prediction'],
            'risk_probability': result['risk_probability'],
            'risk_level': result['risk_level'],
            'patient_data': {
                'age': age,
                'sex': sex,
                'cp': cp,
                'trestbps': trestbps,
                'chol': chol,
                'fbs': fbs,
                'restecg': restecg,
                'thalachh': thalachh,
                'exang': exang,
                'oldpeak': oldpeak,
                'slope': slope,
                'ca': ca,
                'thal': thal
            }
        }
        
        print(f"Storing data: {stored_data}")
        print("Redirecting to /results")
        print("=" * 50)
        
        return (
            dbc.Alert([
                html.H5("Prediction Complete!", className="alert-heading"),
                html.P(f"Risk Level: {result['risk_level']}"),
                html.P("Redirecting to results page...")
            ], color="success"),
            stored_data,
            '/results'
        )