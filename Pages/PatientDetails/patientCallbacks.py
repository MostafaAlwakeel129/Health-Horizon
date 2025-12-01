"""
Patient Details Callbacks
Handles patient input, validation, prediction, field preservation, and database storage.
"""

from dash.dependencies import Input, Output, State
from dash import html
import dash_bootstrap_components as dbc
from dash import no_update
from utils.model_utils import predictor
from utils.db_utils import db_manager

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

# Field ranges for validation
FIELD_RANGES = {
    'age': (1, 120),
    'sex': (0, 1),
    'cp': (0, 3),
    'trestbps': (50, 250),
    'chol': (30, 1000),
    'fbs': (0, 1),
    'restecg': (0, 2),
    'thalachh': (40, 220),
    'exang': (0, 1),
    'oldpeak': (0, 6.2),
    'slope': (0, 2),
    'ca': (0, 4),
    'thal': (0, 3)
}

# Field keys corresponding to FIELD_NAMES
FIELD_KEYS = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
    'thalachh', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
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


def _validate_ranges(inputs):
    """Validate that all inputs are within acceptable ranges. Returns list of out-of-range field errors."""
    errors = []
    for field_name, field_key, value in zip(FIELD_NAMES, FIELD_KEYS, inputs):
        if value is not None:
            min_val, max_val = FIELD_RANGES[field_key]
            if value < min_val or value > max_val:
                errors.append({
                    'field': field_name,
                    'value': value,
                    'min': min_val,
                    'max': max_val
                })
    return errors


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
        Output('patient-name', 'value'),  # Clear patient name
        Output('patient-id-input', 'value'),  # Clear patient ID
        Input('patient-button', 'n_clicks'),
        State('patient-name', 'value'),
        State('patient-id-input', 'value'),
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
    def predict_heart_disease(n_clicks, patient_name, patient_id, age, sex, cp, 
                             trestbps, chol, fbs, restecg, thalachh, exang, 
                             oldpeak, slope, ca, thal, previous_data):
        """Handle prediction request with validation, duplicate check, and database storage."""
        
        print("=" * 50)
        print("PREDICTION CALLBACK TRIGGERED")
        print(f"Button clicks: {n_clicks}")
        
        # Validate patient name first
        if not patient_name or not patient_name.strip():
            return (
                dbc.Alert([
                    html.H5("Missing Patient Name", className="alert-heading"),
                    html.P("Please enter the patient's name before submitting.")
                ], color="danger"),
                previous_data,
                None,
                no_update,  # Don't clear name
                no_update   # Don't clear ID
            )
        
        # Validate patient ID
        if not patient_id or not patient_id.strip():
            return (
                dbc.Alert([
                    html.H5("Missing Patient ID", className="alert-heading"),
                    html.P("Please enter a unique patient ID before submitting.")
                ], color="danger"),
                previous_data,
                None,
                no_update,  # Don't clear name
                no_update   # Don't clear ID
            )
        
        # Collect all inputs
        inputs = [age, sex, cp, trestbps, chol, fbs, restecg, thalachh,
                 exang, oldpeak, slope, ca, thal]
        
        # Validate both missing fields and ranges
        missing_fields = _validate_inputs(inputs)
        range_errors = _validate_ranges(inputs)
        
        # Create field values for restoration
        field_values = _create_field_values_dict(age, sex, cp, trestbps, chol, fbs,
                                                restecg, thalachh, exang, oldpeak,
                                                slope, ca, thal)
        
        # If we have BOTH missing fields AND range errors, show combined message
        if missing_fields and range_errors:
            # Create missing fields message
            missing_message = (f"Please fill in the missing field: {missing_fields[0]}"
                             if len(missing_fields) == 1
                             else f"Please fill in the missing fields: {', '.join(missing_fields)}")
            
            # Create range error messages
            range_error_messages = [
                html.P(f'The input for "{error["field"]}" is out of range, please input data in range of {error["min"]} and {error["max"]}')
                for error in range_errors
            ]
            
            return (
                dbc.Alert([
                    html.H5("Validation Errors", className="alert-heading"),
                    html.P(missing_message, className="mb-1"),
                    html.Hr(className="my-2"),
                    html.H5("Range Errors:", className="alert-heading mb-1"),
                    *range_error_messages
                ], color="danger"),
                previous_data,
                field_values,
                no_update,  # Don't clear name
                no_update   # Don't clear ID
            )
        
        # If only missing fields (no range errors)
        if missing_fields:
            message = (f"Please fill in the missing field: {missing_fields[0]}"
                      if len(missing_fields) == 1
                      else f"Please fill in the missing fields: {', '.join(missing_fields)}")
            
            return (
                dbc.Alert([
                    html.H5("Missing Information", className="alert-heading"),
                    html.P(message)
                ], color="danger"),
                previous_data,
                field_values,
                no_update,  # Don't clear name
                no_update   # Don't clear ID
            )
        
        # If only range errors (no missing fields)
        if range_errors:
            error_messages = [
                html.P(f'The input for "{error["field"]}" is out of range, please input data in range of {error["min"]} and {error["max"]}')
                for error in range_errors
            ]
            
            return (
                dbc.Alert([
                    html.H5("Invalid Input Range", className="alert-heading"),
                    *error_messages
                ], color="danger"),
                previous_data,
                field_values,
                no_update,  # Don't clear name
                no_update   # Don't clear ID
            )
        
        # Create patient data dictionary
        current_submission = _create_patient_data_dict(age, sex, cp, trestbps, chol, fbs,
                                                      restecg, thalachh, exang, oldpeak,
                                                      slope, ca, thal)
        
        # Check for duplicate submission
        if previous_data and 'patient_data' in previous_data:
            if (previous_data['patient_data'] == current_submission and 
                previous_data.get('patient_id') == patient_id.strip()):
                print("Duplicate submission detected")
                return (
                    dbc.Alert([
                        html.H5("Patient Already Diagnosed", className="alert-heading"),
                        html.P("Patient already diagnosed and results are displayed below.")
                    ], color="warning"),
                    previous_data,
                    field_values,
                    no_update,  # Don't clear name
                    no_update   # Don't clear ID
                )
        
        # Prepare features for prediction
        features = [age, sex, cp, trestbps, chol, fbs, restecg,
                   thalachh, exang, oldpeak, slope, ca, thal]
        
        print(f"Making prediction with features: {features}")
        
        # Make prediction
        result = predictor.predict(features)
        
        if result is None:
            print("ERROR: Prediction returned None!")
            return (
                dbc.Alert([
                    html.H5("Prediction Error", className="alert-heading"),
                    html.P("There was an error making the prediction. Please check the terminal for details.")
                ], color="danger"),
                previous_data,
                field_values,
                no_update,  # Don't clear name
                no_update   # Don't clear ID
            )
        
        # Prepare patient data for database storage
        patient_data_for_db = {
            'patient_name': patient_name.strip(),
            'patient_id': patient_id.strip(),
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
        
        # Save to database
        print("Attempting to save assessment to database...")
        save_success = db_manager.save_patient_assessment(patient_data_for_db, result)
        
        if not save_success:
            print("WARNING: Failed to save assessment to database")
            # Show warning but still display results
            return (
                dbc.Alert([
                    html.H5("Prediction Complete (Database Warning)", className="alert-heading"),
                    html.P(f"Risk Level: {result['risk_level']}"),
                    html.P("Note: Assessment could not be saved to history database."),
                    html.P("Scroll down to view detailed results...")
                ], color="warning"),
                {
                    'prediction': result['prediction'],
                    'risk_probability': result['risk_probability'],
                    'risk_level': result['risk_level'],
                    'patient_data': current_submission,
                    'patient_name': patient_name.strip(),
                    'patient_id': patient_id.strip()
                },
                field_values,
                "",  # Clear patient name
                ""   # Clear patient ID
            )
        
        # Store prediction results with patient info
        stored_data = {
            'prediction': result['prediction'],
            'risk_probability': result['risk_probability'],
            'risk_level': result['risk_level'],
            'patient_data': current_submission,
            'patient_name': patient_name.strip(),
            'patient_id': patient_id.strip()
        }
        
        print(f"Prediction complete: {stored_data['risk_level']}")
        print("Assessment saved to database successfully!")
        print("=" * 50)
        
        return (
            dbc.Alert([
                html.H5("Prediction Complete!", className="alert-heading"),
                html.P(f"Patient: {patient_name.strip()} (ID: {patient_id.strip()})"),
                html.P(f"Risk Level: {result['risk_level']}"),
                html.P("Assessment saved to history. Scroll down to view detailed results...")
            ], color="success"),
            stored_data,
            field_values,
            "",  # Clear patient name
            ""   # Clear patient ID
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