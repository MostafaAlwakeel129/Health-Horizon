from dash import html, dcc
import dash_bootstrap_components as dbc

# Home Page Layout
homeLayout = dbc.Container([
    # Hero Section
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Project Ventro", 
                       className="display-3 fw-bold text-center mb-3",
                       style={'color': '#2c3e50'}),
                html.P("Advanced Heart Disease Risk Assessment System", 
                      className="lead text-center text-muted mb-2"),
                html.P("by Team Health Horizon", 
                      className="text-center text-muted fst-italic mb-5",
                      style={'fontSize': '1.1rem'})
            ], style={'padding': '40px 0'})
        ], width=12)
    ]),
    
    # Mission Statement Card
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H3("🫀 Empowering Healthcare Professionals", 
                               className="text-center mb-4",
                               style={'color': '#e74c3c'}),
                        html.P([
                            "Ventro is a cutting-edge clinical decision support tool designed to assist ",
                            "healthcare professionals in assessing cardiovascular disease risk. Using ",
                            "advanced machine learning algorithms trained on comprehensive patient data, ",
                            "our system provides rapid, evidence-based risk assessments to support ",
                            "clinical decision-making."
                        ], className="text-center lead", style={'fontSize': '1.1rem'}),
                    ])
                ])
            ], className="shadow-lg mb-5", style={'border': 'none', 'borderRadius': '15px'})
        ], width=10, className="mx-auto")
    ]),
    
    # Feature Cards
    dbc.Row([
        # Feature 1
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H2("⚡", className="text-center mb-3", style={'fontSize': '3rem'}),
                        html.H4("Rapid Assessment", className="text-center mb-3"),
                        html.P([
                            "Get instant risk predictions based on standard clinical parameters. ",
                            "Our model processes patient data in seconds, providing immediate insights ",
                            "to support timely clinical decisions."
                        ], className="text-center")
                    ])
                ])
            ], className="h-100 shadow", style={'border': 'none', 'borderRadius': '10px'})
        ], width=4, className="mb-4"),
        
        # Feature 2
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H2("🎯", className="text-center mb-3", style={'fontSize': '3rem'}),
                        html.H4("Evidence-Based", className="text-center mb-3"),
                        html.P([
                            "Our machine learning model is trained on validated clinical datasets, ",
                            "incorporating key cardiovascular risk factors including ECG results, ",
                            "blood pressure, cholesterol levels, and exercise stress test outcomes."
                        ], className="text-center")
                    ])
                ])
            ], className="h-100 shadow", style={'border': 'none', 'borderRadius': '10px'})
        ], width=4, className="mb-4"),
        
        # Feature 3
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H2("📊", className="text-center mb-3", style={'fontSize': '3rem'}),
                        html.H4("Probability Scores", className="text-center mb-3"),
                        html.P([
                            "Beyond binary predictions, Ventro provides risk probability scores, ",
                            "giving clinicians a nuanced understanding of patient risk levels to ",
                            "inform personalized treatment strategies."
                        ], className="text-center")
                    ])
                ])
            ], className="h-100 shadow", style={'border': 'none', 'borderRadius': '10px'})
        ], width=4, className="mb-4"),
    ]),
    
    # How It Works Section
    dbc.Row([
        dbc.Col([
            html.H3("How Ventro Works", className="text-center mb-4 mt-5", style={'color': '#2c3e50'}),
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H1("1", className="text-primary fw-bold mb-3"),
                                html.H5("Enter Patient Data", className="mb-2"),
                                html.P("Input standard clinical parameters including vital signs, ECG results, and lab values")
                            ], className="text-center")
                        ], width=3),
                        dbc.Col([
                            html.Div([
                                html.H1("2", className="text-primary fw-bold mb-3"),
                                html.H5("AI Analysis", className="mb-2"),
                                html.P("Our trained model analyzes the data using validated cardiovascular risk factors")
                            ], className="text-center")
                        ], width=3),
                        dbc.Col([
                            html.Div([
                                html.H1("3", className="text-primary fw-bold mb-3"),
                                html.H5("Risk Assessment", className="mb-2"),
                                html.P("Receive instant risk probability score and categorical risk level")
                            ], className="text-center")
                        ], width=3),
                        dbc.Col([
                            html.Div([
                                html.H1("4", className="text-primary fw-bold mb-3"),
                                html.H5("Clinical Decision", className="mb-2"),
                                html.P("Use results to support diagnosis, treatment planning, and patient counseling")
                            ], className="text-center")
                        ], width=3),
                    ])
                ])
            ], className="shadow-lg mb-5", style={'border': 'none', 'borderRadius': '15px'})
        ], width=12)
    ]),
    
    # Call to Action
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Ready to Begin Assessment?", className="text-center text-white mb-4"),
                    html.P("Start by entering patient clinical data for comprehensive risk evaluation", 
                          className="text-center text-white mb-4", style={'fontSize': '1.1rem'}),
                    html.Div([
                        dbc.Button(
                            "Start Patient Assessment →",
                            href="/patient",
                            color="light",
                            size="lg",
                            className="px-5 py-3",
                            style={'fontSize': '1.2rem', 'fontWeight': 'bold'}
                        )
                    ], className="text-center")
                ])
            ], className="shadow-lg", 
            style={'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
                   'border': 'none', 
                   'borderRadius': '15px'})
        ], width=10, className="mx-auto mb-5")
    ]),
    
    # Disclaimer
    dbc.Row([
        dbc.Col([
            dbc.Alert([
                html.H6("⚕️ Clinical Use Disclaimer", className="alert-heading fw-bold"),
                html.P([
                    "Ventro is intended as a clinical decision support tool only. All risk assessments ",
                    "should be interpreted by qualified healthcare professionals in the context of ",
                    "complete clinical evaluation. This tool does not replace clinical judgment, ",
                    "diagnostic testing, or comprehensive patient assessment."
                ], className="mb-0", style={'fontSize': '0.9rem'})
            ], color="info", className="shadow-sm")
        ], width=10, className="mx-auto mb-4")
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("© 2024 Team Health Horizon | Project Ventro", 
                  className="text-center text-muted",
                  style={'fontSize': '0.9rem'})
        ], width=12, className="mt-4")
    ])
    
], fluid=True, style={'backgroundColor': '#f8f9fa', 'minHeight': '100vh', 'paddingTop': '20px', 'paddingBottom': '20px'})