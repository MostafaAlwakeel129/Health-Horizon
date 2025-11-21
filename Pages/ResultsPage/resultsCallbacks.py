"""
Results Page Callbacks
Handles displaying prediction results and resetting assessments.
"""

from dash.dependencies import Input, Output
from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime
import json

# Value mapping functions for readable display
VALUE_MAPPINGS = {
    'sex': lambda v: "Male" if v == 1 else "Female",
    'cp': {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-anginal Pain", 3: "Asymptomatic"},
    'fbs': lambda v: "Yes (> 120 mg/dl)" if v == 1 else "No (≤ 120 mg/dl)",
    'restecg': {0: "Normal", 1: "ST-T Wave Abnormality", 2: "Left Ventricular Hypertrophy"},
    'exang': lambda v: "Yes" if v == 1 else "No",
    'slope': {0: "Upsloping", 1: "Flat", 2: "Downsloping"},
    'thal': {0: "Normal", 1: "Fixed Defect", 2: "Reversible Defect", 3: "Reversible Defect (Type 3)"}
}


def _get_mapped_value(field_name, value):
    """Get human-readable value for a field."""
    mapper = VALUE_MAPPINGS.get(field_name)
    if mapper is None:
        return str(value)
    
    if callable(mapper):
        return mapper(value)
    else:
        return mapper.get(value, "Unknown")


def _create_report_data(patient, risk_percentage, risk_text):
    """Create report data dictionary for export."""
    return {
        'patient_details': {
            'Age': f"{patient['age']} years",
            'Sex': _get_mapped_value('sex', patient['sex']),
            'Chest Pain Type': _get_mapped_value('cp', patient['cp']),
            'Resting Blood Pressure': f"{patient['trestbps']} mm Hg",
            'Serum Cholesterol': f"{patient['chol']} mg/dl",
            'Fasting Blood Sugar': _get_mapped_value('fbs', patient['fbs']),
            'Resting ECG': _get_mapped_value('restecg', patient['restecg']),
            'Maximum Heart Rate': f"{patient['thalachh']} bpm",
            'Exercise Induced Angina': _get_mapped_value('exang', patient['exang']),
            'ST Depression': f"{patient['oldpeak']}",
            'Slope': _get_mapped_value('slope', patient['slope']),
            'Number of Major Vessels': f"{patient['ca']}",
            'Thalassemia': _get_mapped_value('thal', patient['thal'])
        },
        'risk_assessment': {
            'Risk Probability': f"{risk_percentage:.1f}%",
            'Risk Level': risk_text,
            'Assessment Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }


def _create_results_display(patient, risk_percentage, risk_text, risk_color, risk_icon, report_data):
    """Create the results display HTML."""
    return html.Div([
        dbc.Card([
            dbc.CardHeader([
                html.H2("Heart Disease Risk Assessment Report", 
                       className="text-center mb-0 report-header")
            ], className="report-card-header"),
            dbc.CardBody([
                # Risk Display - Enhanced Layout
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H3([risk_icon, f" {risk_text}"], 
                                   className=f"text-{risk_color} text-center mb-3"),
                            html.H1(f"{risk_percentage:.1f}%", 
                                   className=f"text-{risk_color} text-center mb-4",
                                   style={'font-size': '4rem', 'font-weight': 'bold'}),
                            html.P("Risk Probability", className="text-center text-muted mb-0")
                        ], className="risk-display-box")
                    ], width=12, className="mb-4")
                ]),
                
                # Patient Details - Enhanced with Cards
                html.H4("Patient Details", className="mb-4 section-title"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Personal Information", className="mb-3 text-muted"),
                                html.P([html.Strong("Age: "), f"{patient['age']} years"], className="mb-2"),
                                html.P([html.Strong("Sex: "), _get_mapped_value('sex', patient['sex'])], className="mb-2"),
                                html.P([html.Strong("Chest Pain Type: "), _get_mapped_value('cp', patient['cp'])], className="mb-2"),
                                html.P([html.Strong("Fasting Blood Sugar: "), _get_mapped_value('fbs', patient['fbs'])], className="mb-0"),
                            ])
                        ], className="mb-3")
                    ], width=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Vital Signs", className="mb-3 text-muted"),
                                html.P([html.Strong("Resting BP: "), f"{patient['trestbps']} mm Hg"], className="mb-2"),
                                html.P([html.Strong("Cholesterol: "), f"{patient['chol']} mg/dl"], className="mb-2"),
                                html.P([html.Strong("Max Heart Rate: "), f"{patient['thalachh']} bpm"], className="mb-2"),
                                html.P([html.Strong("ST Depression: "), f"{patient['oldpeak']}"], className="mb-0"),
                            ])
                        ], className="mb-3")
                    ], width=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Medical Tests", className="mb-3 text-muted"),
                                html.P([html.Strong("Resting ECG: "), _get_mapped_value('restecg', patient['restecg'])], className="mb-2"),
                                html.P([html.Strong("Exercise Angina: "), _get_mapped_value('exang', patient['exang'])], className="mb-2"),
                                html.P([html.Strong("Slope: "), _get_mapped_value('slope', patient['slope'])], className="mb-2"),
                                html.P([html.Strong("Major Vessels: "), f"{patient['ca']}"], className="mb-2"),
                                html.P([html.Strong("Thalassemia: "), _get_mapped_value('thal', patient['thal'])], className="mb-0"),
                            ])
                        ], className="mb-3")
                    ], width=4)
                ], className="mb-4"),
                
                # Action Buttons
                dbc.Row([
                    dbc.Col([
                        dbc.Button("New Assessment", id="new-assessment-button",
                                 color="primary", size="lg", className="w-100 mb-2")
                    ], width=6),
                    dbc.Col([
                        html.Button("Export Report", id="export-report-button",
                                   className="btn btn-success w-100",
                                   style={'height': '48px', 'font-size': '1.1rem'},
                                   n_clicks=0)
                    ], width=6)
                ], className="mb-3"),
                
                # Hidden report data for export
                html.Div(id="report-data-store", style={'display': 'none'},
                        children=json.dumps(report_data),
                        **{'data-report': json.dumps(report_data)})
            ])
        ], className="mb-4 report-card")
    ])


def resultsCallbacks(app):
    """Register all callbacks for the Results page."""
    
    @app.callback(
        Output('results-output', 'children'),
        Input('prediction-store', 'data')
    )
    def display_results(stored_data):
        """Display prediction results."""
        
        if not stored_data:
            return html.Div([
                dbc.Alert([
                    html.H4("No Assessment Data", className="alert-heading"),
                    html.P("Please complete a patient assessment above to view results here.")
                ], color="warning")
            ])
        
        if 'prediction' not in stored_data:
            return html.Div([
                dbc.Alert([
                    html.H4("Invalid Data", className="alert-heading"),
                    html.P("The prediction data is incomplete. Please try again above.")
                ], color="warning")
            ])
        
        # Extract data
        result = {
            'prediction': stored_data['prediction'],
            'risk_probability': stored_data.get('risk_probability', 0),
            'risk_level': stored_data.get('risk_level', 'Unknown')
        }
        patient = stored_data['patient_data']
        
        # Calculate risk percentage
        risk_percentage = (result['risk_probability'] * 100 
                          if result['risk_probability'] 
                          else (100 if result['prediction'] == 1 else 0))
        
        # Determine risk display properties
        if risk_percentage >= 50:
            risk_text, risk_color, risk_icon = "High Risk", "danger", "⚠️"
        else:
            risk_text, risk_color, risk_icon = "Low Risk", "success", "✓"
        
        # Create report data
        report_data = _create_report_data(patient, risk_percentage, risk_text)
        
        return _create_results_display(patient, risk_percentage, risk_text,
                                      risk_color, risk_icon, report_data)
    
    @app.callback(
        Output('prediction-store', 'data', allow_duplicate=True),
        Output('field-values-store', 'data', allow_duplicate=True),
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
        Output('patient-output', 'children', allow_duplicate=True),
        Input('new-assessment-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def reset_assessment(n_clicks):
        """Reset all fields and data for a new assessment."""
        if n_clicks:
            print("Resetting assessment - clearing all fields and data")
            return tuple([None] * 16)
        return tuple([None] * 16)
