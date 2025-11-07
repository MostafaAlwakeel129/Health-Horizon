from dash import html, dcc
import dash_bootstrap_components as dbc

# Patient Details Page Layout
patientLayout = dbc.Container([
    # ✅ ADD THIS AT THE TOP
    dcc.Store(id='prediction-store', storage_type='session'),
    
    dbc.Row([
        dbc.Col([
            html.H1("Patient Details", className="text-center mb-4"),
            html.P("Enter patient information to predict heart disease risk", 
                   className="text-center text-muted mb-4"),
            html.Hr(),
        ], width=12)
    ]),
    
    dbc.Row([
        # Left Column - Personal Information
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Personal Information", className="text-white"), 
                             style={'backgroundColor': '#2c3e50'}),
                dbc.CardBody([
                    # Age
                    dbc.Label("Age", className="fw-bold"),
                    dbc.Input(
                        id="patient-age",
                        type="number",
                        placeholder="Enter age (years)",
                        min=1, max=120, step=1,
                        className="mb-3"
                    ),
                    
                    # Sex
                    dbc.Label("Sex", className="fw-bold"),
                    dcc.Dropdown(
                        id="patient-sex",
                        options=[
                            {'label': 'Female', 'value': 0},
                            {'label': 'Male', 'value': 1}
                        ],
                        placeholder="Select sex",
                        className="mb-3"
                    ),
                    
                    # Chest Pain Type
                    dbc.Label("Chest Pain Type", className="fw-bold"),
                    dcc.Dropdown(
                        id="patient-cp",
                        options=[
                            {'label': 'Type 0: Typical Angina', 'value': 0},
                            {'label': 'Type 1: Atypical Angina', 'value': 1},
                            {'label': 'Type 2: Non-anginal Pain', 'value': 2},
                            {'label': 'Type 3: Asymptomatic', 'value': 3}
                        ],
                        placeholder="Select chest pain type",
                        className="mb-3"
                    ),
                    
                    # Fasting Blood Sugar
                    dbc.Label("Fasting Blood Sugar > 120 mg/dl", className="fw-bold"),
                    dcc.Dropdown(
                        id="patient-fbs",
                        options=[
                            {'label': 'No (≤ 120 mg/dl)', 'value': 0},
                            {'label': 'Yes (> 120 mg/dl)', 'value': 1}
                        ],
                        placeholder="Select fasting blood sugar level",
                        className="mb-3"
                    ),
                    
                    # Exercise Induced Angina
                    dbc.Label("Exercise Induced Angina", className="fw-bold"),
                    dcc.Dropdown(
                        id="patient-exang",
                        options=[
                            {'label': 'No', 'value': 0},
                            {'label': 'Yes', 'value': 1}
                        ],
                        placeholder="Select if exercise induces angina",
                        className="mb-3"
                    ),
                ])
            ], className="mb-4")
        ], width=6),
        
        # Right Column - Medical Measurements
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Medical Measurements", className="text-white"), 
                             style={'backgroundColor': '#2c3e50'}),
                dbc.CardBody([
                    # Resting Blood Pressure
                    dbc.Label("Resting Blood Pressure (mm Hg)", className="fw-bold"),
                    dbc.Input(
                        id="patient-trestbps",
                        type="number",
                        placeholder="Enter resting blood pressure",
                        min=80, max=220, step=1,
                        className="mb-3"
                    ),
                    
                    # Cholesterol
                    dbc.Label("Serum Cholesterol (mg/dl)", className="fw-bold"),
                    dbc.Input(
                        id="patient-chol",
                        type="number",
                        placeholder="Enter cholesterol level",
                        min=100, max=600, step=1,
                        className="mb-3"
                    ),
                    
                    # Maximum Heart Rate
                    dbc.Label("Maximum Heart Rate Achieved", className="fw-bold"),
                    dbc.Input(
                        id="patient-thalachh",
                        type="number",
                        placeholder="Enter maximum heart rate",
                        min=60, max=220, step=1,
                        className="mb-3"
                    ),
                    
                    # ST Depression
                    dbc.Label("ST Depression (Oldpeak)", className="fw-bold"),
                    dbc.Input(
                        id="patient-oldpeak",
                        type="number",
                        placeholder="Enter ST depression value",
                        min=0, max=10, step=0.1,
                        className="mb-3"
                    ),
                    
                    # Resting ECG
                    dbc.Label("Resting Electrocardiographic Results", className="fw-bold"),
                    dcc.Dropdown(
                        id="patient-restecg",
                        options=[
                            {'label': '0: Normal', 'value': 0},
                            {'label': '1: ST-T Wave Abnormality', 'value': 1},
                            {'label': '2: Left Ventricular Hypertrophy', 'value': 2}
                        ],
                        placeholder="Select resting ECG result",
                        className="mb-3"
                    ),
                ])
            ], className="mb-4")
        ], width=6)
    ]),
    
    dbc.Row([
        # Additional Medical Information
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Additional Medical Information", className="text-white"), 
                             style={'backgroundColor': '#2c3e50'}),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            # Slope
                            dbc.Label("Slope of Peak Exercise ST Segment", className="fw-bold"),
                            dcc.Dropdown(
                                id="patient-slope",
                                options=[
                                    {'label': '0: Upsloping', 'value': 0},
                                    {'label': '1: Flat', 'value': 1},
                                    {'label': '2: Downsloping', 'value': 2}
                                ],
                                placeholder="Select slope type",
                                className="mb-3"
                            ),
                        ], width=4),
                        
                        dbc.Col([
                            # Number of Major Vessels
                            dbc.Label("Number of Major Vessels (0-4)", className="fw-bold"),
                            dcc.Dropdown(
                                id="patient-ca",
                                options=[
                                    {'label': '0', 'value': 0},
                                    {'label': '1', 'value': 1},
                                    {'label': '2', 'value': 2},
                                    {'label': '3', 'value': 3},
                                    {'label': '4', 'value': 4}
                                ],
                                placeholder="Select number of vessels",
                                className="mb-3"
                            ),
                        ], width=4),
                        
                        dbc.Col([
                            # Thalassemia
                            dbc.Label("Thalassemia", className="fw-bold"),
                            dcc.Dropdown(
                                id="patient-thal",
                                options=[
                                    {'label': '0: Normal', 'value': 0},
                                    {'label': '1: Fixed Defect', 'value': 1},
                                    {'label': '2: Reversible Defect', 'value': 2},
                                    {'label': '3: Reversible Defect', 'value': 3}
                                ],
                                placeholder="Select thalassemia type",
                                className="mb-3"
                            ),
                        ], width=4),
                    ])
                ])
            ], className="mb-4")
        ], width=12)
    ]),
    
    # Submit Button and Messages
    dbc.Row([
        dbc.Col([
            dbc.Button(
                "Predict Heart Disease Risk",
                id="patient-button",
                color="primary",
                size="lg",
                className="w-100 mb-3"
            ),
            html.Div(id="patient-output", className="mt-3")
        ], width=12)
    ])
], fluid=True)