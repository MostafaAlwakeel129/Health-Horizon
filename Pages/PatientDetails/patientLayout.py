from dash import html, dcc
import dash_bootstrap_components as dbc

# Radio button options
RADIO_OPTIONS = {
    'sex': [
        {'label': 'Male', 'value': 1},
        {'label': 'Female', 'value': 0}
    ],
    'cp': [
        {'label': 'Typical Angina', 'value': 0},
        {'label': 'Atypical Angina', 'value': 1},
        {'label': 'Non-anginal Pain', 'value': 2},
        {'label': 'Asymptomatic', 'value': 3}
    ],
    'fbs': [
        {'label': 'No (≤ 120 mg/dl)', 'value': 0},
        {'label': 'Yes (> 120 mg/dl)', 'value': 1}
    ],
    'restecg': [
        {'label': 'Normal', 'value': 0},
        {'label': 'ST-T Wave Abnormality', 'value': 1},
        {'label': 'Left Ventricular Hypertrophy', 'value': 2}
    ],
    'exang': [
        {'label': 'No', 'value': 0},
        {'label': 'Yes', 'value': 1}
    ],
    'slope': [
        {'label': 'Upsloping', 'value': 0},
        {'label': 'Flat', 'value': 1},
        {'label': 'Downsloping', 'value': 2}
    ],
    'thal': [
        {'label': 'Normal', 'value': 0},
        {'label': 'Fixed Defect', 'value': 1},
        {'label': 'Reversible Defect', 'value': 2},
        {'label': 'Reversible Defect', 'value': 3}
    ]
}

# Dropdown options
DROPDOWN_OPTIONS = {
    'ca': [
        {'label': str(i), 'value': i} for i in range(5)
    ]
}


def _create_input_field(field_id, label, input_type="number", placeholder="", 
                        min_val=None, max_val=None, step=None):
    """Create a standardized input field with compact spacing."""
    return [
        dbc.Label(label, className="fw-bold mb-0", style={'fontSize': '0.85rem'}),
        dbc.Input(
            id=field_id,
            type=input_type,
            placeholder=placeholder,
            step=step,
            className="mb-1",
            style={'padding': '0.4rem 0.5rem', 'fontSize': '0.9rem'}
        )
    ]


def _create_radio_field(field_id, label, options, inline=False):
    """Create a standardized radio button field with compact spacing."""
    return [
        dbc.Label(label, className="fw-bold mb-0", style={'fontSize': '0.85rem', 'display': 'block', 'marginBottom': '0.3rem'}),
        dbc.RadioItems(
            id=field_id,
            options=options,
            value=None,
            inline=inline,
            className="mb-1 radio-buttons",
            style={'fontSize': '0.9rem'}
        )
    ]


def _create_dropdown_field(field_id, label, options, placeholder=""):
    """Create a standardized dropdown field with compact spacing."""
    return [
        dbc.Label(label, className="fw-bold mb-0", style={'fontSize': '0.85rem'}),
        html.Div([
            dcc.Dropdown(
                id=field_id,
                options=options,
                placeholder=placeholder,
                className="mb-1",
                style={'fontSize': '0.9rem'}
            )
        ], className="dropdown-wrapper")
    ]


patientLayout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("FILL PATIENT DETAILS", className="text-center mb-2 patient-details-header", 
                   style={'fontSize': '1.8rem', 'marginBottom': '0.5rem !important'}),
        ], width=12)
    ]),
    
    # Main Form - Five Columns
    dbc.Row([
        # Column 1 - Personal Info + Measurements
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Personal & Vitals", className="mb-0", style={'fontSize': '1rem', 'color': '#1a1d29'}),
                    style={'backgroundColor': '#f1f3f5', 'padding': '8px 10px'}
                ),
                dbc.CardBody([
                    *_create_input_field('patient-age', 'Age', placeholder="Age", step=1),
                    *_create_radio_field('patient-sex', 'Sex', RADIO_OPTIONS['sex'], inline=True),
                    *_create_input_field('patient-trestbps', 'Resting BP (mm Hg)',
                                       placeholder="BP", step=1),
                    *_create_input_field('patient-chol', 'Cholesterol (mg/dl)',
                                       placeholder="Cholesterol", step=1),
                    *_create_input_field('patient-thalachh', 'Max Heart Rate',
                                       placeholder="Heart Rate", step=1),
                ], style={'padding': '10px', 'minHeight': '500px'})
            ], className="mb-2", style={'marginBottom': '0.5rem !important'})
        ], width=True),
        
        # Column 2
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Chest & ECG", className="mb-0", style={'fontSize': '1rem', 'color': '#1a1d29'}),
                    style={'backgroundColor': '#f1f3f5', 'padding': '8px 10px'}
                ),
                dbc.CardBody([
                    *_create_radio_field('patient-cp', 'Chest Pain Type', RADIO_OPTIONS['cp']),
                    *_create_radio_field('patient-restecg', 'Resting ECG',
                                       RADIO_OPTIONS['restecg']),
                ], style={'padding': '10px', 'minHeight': '500px'})
            ], className="mb-2", style={'marginBottom': '0.5rem !important'})
        ], width=True),
        
        # Column 3
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Test Results", className="mb-0", style={'fontSize': '1rem', 'color': '#1a1d29'}),
                    style={'backgroundColor': '#f1f3f5', 'padding': '8px 10px'}
                ),
                dbc.CardBody([
                    *_create_input_field('patient-oldpeak', 'ST Depression',
                                       placeholder="ST Depression", step=0.1),
                    *_create_radio_field('patient-fbs', 'Fasting Blood Sugar > 120',
                                       RADIO_OPTIONS['fbs'], inline=True),
                    *_create_radio_field('patient-exang', 'Exercise Angina',
                                       RADIO_OPTIONS['exang'], inline=True),
                ], style={'padding': '10px', 'minHeight': '500px'})
            ], className="mb-2", style={'marginBottom': '0.5rem !important'})
        ], width=True),
        
        # Column 4
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Exercise Data", className="mb-0", style={'fontSize': '1rem', 'color': '#1a1d29'}),
                    style={'backgroundColor': '#f1f3f5', 'padding': '8px 10px'}
                ),
                dbc.CardBody([
                    *_create_radio_field('patient-slope', 'Slope',
                                       RADIO_OPTIONS['slope']),
                    *_create_dropdown_field('patient-ca', 'Major Vessels (0-4)',
                                          DROPDOWN_OPTIONS['ca'],
                                          placeholder="Vessels"),
                ], style={'padding': '10px', 'minHeight': '500px'})
            ], className="mb-2", style={'marginBottom': '0.5rem !important'})
        ], width=True),
        
        # Column 5
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Blood Work", className="mb-0", style={'fontSize': '1rem', 'color': '#1a1d29'}),
                    style={'backgroundColor': '#f1f3f5', 'padding': '8px 10px'}
                ),
                dbc.CardBody([
                    *_create_radio_field('patient-thal', 'Thalassemia', RADIO_OPTIONS['thal']),
                ], style={'padding': '10px', 'minHeight': '500px'})
            ], className="mb-2", style={'marginBottom': '0.5rem !important'})
        ], width=True)
    ]),
    
    # Submit Button and Output
    dbc.Row([
        dbc.Col([
            dbc.Button(
                "Predict Heart Disease Risk",
                id="patient-button",
                color="primary",
                size="lg",
                className="w-100 mb-2",
                disabled=False
            ),
            html.Div(id="patient-output", className="mt-2")
        ], width=12)
    ])
], fluid=True)