from dash.dependencies import Input, Output
from dash import html
import dash_bootstrap_components as dbc

def resultsCallbacks(app):
    """
    Register all callbacks for the Results page.
    """
    
    @app.callback(
        Output('results-output', 'children'),
        Input('prediction-store', 'data')
    )
    def display_results(stored_data):
        
        print("=" * 50)
        print("RESULTS PAGE CALLBACK TRIGGERED!")
        print(f"Stored data received: {stored_data}")
        print(f"Data type: {type(stored_data)}")
        
        # Check if we have prediction data
        if not stored_data:
            print("ERROR: No stored data!")
            return dbc.Alert([
                html.H4("No Assessment Data", className="alert-heading"),
                html.P("Please complete a patient assessment first."),
                dbc.Button("Go to Patient Details", href="/patient", color="primary", className="mt-2")
            ], color="warning")
        
        if 'prediction' not in stored_data:
            print("ERROR: No prediction in stored data!")
            return dbc.Alert([
                html.H4("Invalid Data", className="alert-heading"),
                html.P("The prediction data is incomplete. Please try again."),
                dbc.Button("Go to Patient Details", href="/patient", color="primary", className="mt-2")
            ], color="warning")
        
        # Extract prediction results and patient data
        result = {
            'prediction': stored_data['prediction'],
            'risk_probability': stored_data.get('risk_probability'),
            'risk_level': stored_data['risk_level']
        }
        
        patient = stored_data['patient_data']
        age = patient['age']
        sex = patient['sex']
        trestbps = patient['trestbps']
        chol = patient['chol']
        thalachh = patient['thalachh']
        oldpeak = patient['oldpeak']
        exang = patient['exang']
        ca = patient['ca']
        
        print(f"Prediction: {result['prediction']}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Risk Probability: {result['risk_probability']}")
        print("=" * 50)
        
        # Determine risk level and color
        if result['prediction'] == 1:
            risk_color = "danger"
            risk_icon = "⚠️"
            risk_text = "High Risk"
            recommendations = [
                "Consult with a cardiologist as soon as possible",
                "Schedule comprehensive cardiac evaluation",
                "Monitor blood pressure and cholesterol regularly",
                "Adopt heart-healthy lifestyle changes",
                "Consider stress testing and further diagnostic procedures"
            ]
        else:
            risk_color = "success"
            risk_icon = "✓"
            risk_text = "Low Risk"
            recommendations = [
                "Continue maintaining a healthy lifestyle",
                "Regular check-ups with your primary care physician",
                "Keep monitoring your cardiovascular health",
                "Maintain healthy diet and exercise routine",
                "Stay informed about heart disease prevention"
            ]
        
        # Create results display
        return html.Div([
            # Risk Level Card
            dbc.Card([
                dbc.CardBody([
                    html.H2([risk_icon, f" {risk_text}"], 
                           className=f"text-{risk_color} text-center mb-4"),
                    html.Hr(),
                    
                    # Patient Summary
                    dbc.Row([
                        dbc.Col([
                            html.H5("Patient Information", className="mb-3"),
                            html.P([html.Strong("Age: "), f"{age} years"]),
                            html.P([html.Strong("Sex: "), "Male" if sex == 1 else "Female"]),
                            html.P([html.Strong("Resting BP: "), f"{trestbps} mm Hg"]),
                            html.P([html.Strong("Cholesterol: "), f"{chol} mg/dl"]),
                        ], width=6),
                        dbc.Col([
                            html.H5("Assessment Details", className="mb-3"),
                            html.P([html.Strong("Max Heart Rate: "), f"{thalachh} bpm"]),
                            html.P([html.Strong("ST Depression: "), f"{oldpeak}"]),
                            html.P([html.Strong("Exercise Angina: "), "Yes" if exang == 1 else "No"]),
                            html.P([html.Strong("Major Vessels: "), f"{ca}"]),
                        ], width=6)
                    ], className="mb-4"),
                    
                    # Probability if available
                    html.Div([
                        html.Hr(),
                        html.H5("Risk Assessment", className="mb-3"),
                        dbc.Progress(
                            value=result['risk_probability'] * 100 if result['risk_probability'] else (100 if result['prediction'] == 1 else 0),
                            label=f"{result['risk_probability']*100:.1f}%" if result['risk_probability'] else f"{100 if result['prediction'] == 1 else 0}%",
                            color=risk_color,
                            className="mb-3",
                            style={"height": "30px"}
                        )
                    ]) if result['risk_probability'] is not None else html.Div(),
                ])
            ], className="mb-4", color=risk_color, outline=True),
            
            # Recommendations Card
            dbc.Card([
                dbc.CardHeader(html.H4("Recommendations", className="mb-0")),
                dbc.CardBody([
                    html.Ul([html.Li(rec) for rec in recommendations])
                ])
            ], className="mb-4"),
            
            # Action Buttons
            dbc.Row([
                dbc.Col([
                    dbc.Button("New Assessment", href="/patient", color="primary", className="w-100")
                ], width=6),
                dbc.Col([
                    dbc.Button("Back to Home", href="/", color="secondary", className="w-100")
                ], width=6)
            ], className="mb-4"),
            
            # Disclaimer
            dbc.Alert([
                html.H6("Important Disclaimer", className="alert-heading"),
                html.P([
                    "This assessment is for informational purposes only and should not be considered as medical advice. ",
                    "Please consult with a qualified healthcare professional for proper diagnosis and treatment."
                ], className="mb-0")
            ], color="info")
        ])