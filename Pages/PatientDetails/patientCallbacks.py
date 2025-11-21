"""
Patient Details Callbacks
Handles patient input, validation, prediction, and field preservation.
"""

from dash.dependencies import Input, Output, State
from dash import html
import dash_bootstrap_components as dbc
from dash import no_update
from utils.model_utils import predictor

# Field names for validation messages
FIELD_NAMES = [
    'Age', 'Sex', 'Chest Pain Type', 'Resting Blood Pressure',
    'Cholesterol', 'Fasting Blood Sugar', 'Resting ECG',
    'Maximum Heart Rate', 'Exercise Induced Angina',
    'ST Depression', 'Slope', 'Number of Vessels', 'Thalassemia'
]

# Field IDs for restoration
FIELD_IDS = [
    'patient-age', 'patient-sex', 'patient-cp', 'patient-trestbps',
    'patient-chol', 'patient-fbs', 'patient-restecg', 'patient-thalachh',
    'patient-exang', 'patient-oldpeak', 'patient-slope', 'patient-ca', 'patient-thal'
]


def _create_field_values_dict(age, sex, cp, trestbps, chol, fbs, restecg, 
                              thalachh, exang, oldpeak, slope, ca, thal):
    """Helper function to create field values dictionary."""
    return {
        'age': age, 'sex': sex, 'cp': cp, 'trestbps': trestbps,
        'chol': chol, 'fbs': fbs, 'restecg': restecg, 'thalachh': thalachh,
        'exang': exang, 'oldpeak': oldpeak, 'slope': slope, 'ca': ca, 'thal': thal
    }


def _validate_inputs(inputs):
    """Validate that all inputs are provided. Returns list of missing field names."""
    return [name for name, value in zip(FIELD_NAMES, inputs) if value is None]


def _create_patient_data_dict(age, sex, cp, trestbps, chol, fbs, restecg,
                              thalachh, exang, oldpeak, slope, ca, thal):
    """Create patient data dictionary for prediction."""
    return {
        'age': age, 'sex': sex, 'cp': cp, 'trestbps': trestbps,
        'chol': chol, 'fbs': fbs, 'restecg': restecg, 'thalachh': thalachh,
        'exang': exang, 'oldpeak': oldpeak, 'slope': slope, 'ca': ca, 'thal': thal
    }


def patientCallbacks(app):
    """Register all callbacks for the Patient Details page."""
    
    @app.callback(
        Output('patient-output', 'children'),
        Output('prediction-store', 'data'),
        Output('field-values-store', 'data'),
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
        State('prediction-store', 'data'),
        prevent_initial_call=True
    )
    def predict_heart_disease(n_clicks, age, sex, cp, trestbps, chol, fbs,
                             restecg, thalachh, exang, oldpeak, slope, ca, thal, 
                             previous_data):
        """Handle prediction request with validation and duplicate check."""
        
        print("=" * 50)
        print("PREDICTION CALLBACK TRIGGERED")
        print(f"Button clicks: {n_clicks}")
        
        # Collect all inputs
        inputs = [age, sex, cp, trestbps, chol, fbs, restecg, thalachh,
                 exang, oldpeak, slope, ca, thal]
        
        # Validate inputs
        missing_fields = _validate_inputs(inputs)
        if missing_fields:
            message = (f"Please fill in the missing field: {missing_fields[0]}"
                      if len(missing_fields) == 1
                      else f"Please fill in the missing fields: {', '.join(missing_fields)}")
            
            field_values = _create_field_values_dict(age, sex, cp, trestbps, chol, fbs,
                                                    restecg, thalachh, exang, oldpeak,
                                                    slope, ca, thal)
            return (
                dbc.Alert([
                    html.H5("Missing Information", className="alert-heading"),
                    html.P(message)
                ], color="danger"),
                previous_data,
                field_values
            )
        
        # Create patient data dictionary
        current_submission = _create_patient_data_dict(age, sex, cp, trestbps, chol, fbs,
                                                      restecg, thalachh, exang, oldpeak,
                                                      slope, ca, thal)
        
        # Check for duplicate submission
        if previous_data and 'patient_data' in previous_data:
            if previous_data['patient_data'] == current_submission:
                print("Duplicate submission detected")
                field_values = _create_field_values_dict(age, sex, cp, trestbps, chol, fbs,
                                                        restecg, thalachh, exang, oldpeak,
                                                        slope, ca, thal)
                return (
                    dbc.Alert([
                        html.H5("Patient Already Diagnosed", className="alert-heading"),
                        html.P("Patient already diagnosed and results are displayed below.")
                    ], color="warning"),
                    previous_data,
                    field_values
                )
        
        # Disable button immediately to prevent double-click
        # Button will be re-enabled after prediction completes or on error
        
        # Prepare features for prediction
        features = [age, sex, cp, trestbps, chol, fbs, restecg,
                   thalachh, exang, oldpeak, slope, ca, thal]
        
        print(f"Making prediction with features: {features}")
        
        # Make prediction
        result = predictor.predict(features)
        
        if result is None:
            print("ERROR: Prediction returned None!")
            field_values = _create_field_values_dict(age, sex, cp, trestbps, chol, fbs,
                                                    restecg, thalachh, exang, oldpeak,
                                                    slope, ca, thal)
            return (
                dbc.Alert([
                    html.H5("Prediction Error", className="alert-heading"),
                    html.P("There was an error making the prediction. Please check the terminal for details.")
                ], color="danger"),
                previous_data,
                field_values
            )
        
        # Store prediction results
        stored_data = {
            'prediction': result['prediction'],
            'risk_probability': result['risk_probability'],
            'risk_level': result['risk_level'],
            'patient_data': current_submission
        }
        
        print(f"Prediction complete: {stored_data['risk_level']}")
        print("=" * 50)
        
        # Create field values for restoration
        field_values = _create_field_values_dict(age, sex, cp, trestbps, chol, fbs,
                                                restecg, thalachh, exang, oldpeak,
                                                slope, ca, thal)
        
        return (
            dbc.Alert([
                html.H5("Prediction Complete!", className="alert-heading"),
                html.P(f"Risk Level: {result['risk_level']}"),
                html.P("Scroll down to view detailed results...")
            ], color="success"),
            stored_data,
            field_values
        )
    
    @app.callback(
        Output('patient-age', 'value', allow_duplicate=True),
        Output('patient-sex', 'value', allow_duplicate=True),
        Output('patient-cp', 'value', allow_duplicate=True),
        Output('patient-trestbps', 'value', allow_duplicate=True),
        Output('patient-chol', 'value', allow_duplicate=True),
        Output('patient-fbs', 'value', allow_duplicate=True),
        Output('patient-restecg', 'value', allow_duplicate=True),
        Output('patient-thalachh', 'value', allow_duplicate=True),
        Output('patient-exang', 'value', allow_duplicate=True),
        Output('patient-oldpeak', 'value', allow_duplicate=True),
        Output('patient-slope', 'value', allow_duplicate=True),
        Output('patient-ca', 'value', allow_duplicate=True),
        Output('patient-thal', 'value', allow_duplicate=True),
        Input('field-values-store', 'data'),
        prevent_initial_call=True
    )
    def restore_field_values(field_values_store):
        """Restore field values from store after prediction."""
        if not field_values_store:
            return tuple([no_update] * 13)
        
        print("Restoring field values from store")
        return (
            field_values_store.get('age'),
            field_values_store.get('sex'),
            field_values_store.get('cp'),
            field_values_store.get('trestbps'),
            field_values_store.get('chol'),
            field_values_store.get('fbs'),
            field_values_store.get('restecg'),
            field_values_store.get('thalachh'),
            field_values_store.get('exang'),
            field_values_store.get('oldpeak'),
            field_values_store.get('slope'),
            field_values_store.get('ca'),
            field_values_store.get('thal')
        )
    
    # Clientside callback to disable button for 3 seconds on click (prevents double-click)
    app.clientside_callback(
        """
        function(n_clicks) {
            const button = document.getElementById('patient-button');
            if (!button || !n_clicks || n_clicks === 0) {
                return window.dash_clientside.no_update;
            }
            
            // Only disable if button is not already disabled
            if (!button.disabled) {
                // Store original text
                const originalText = button.textContent || button.innerText || 'Predict Heart Disease Risk';
                button.setAttribute('data-original-text', originalText);
                
                // Immediately disable button to prevent double-click
                button.disabled = true;
                button.textContent = 'Processing...';
                
                // Re-enable after 3 seconds
                setTimeout(function() {
                    button.disabled = false;
                    const storedText = button.getAttribute('data-original-text') || originalText;
                    button.textContent = storedText;
                }, 3000);
            }
            
            return window.dash_clientside.no_update;
        }
        """,
        Output('patient-button', 'n_clicks', allow_duplicate=True),
        Input('patient-button', 'n_clicks'),
        prevent_initial_call=True
    )
