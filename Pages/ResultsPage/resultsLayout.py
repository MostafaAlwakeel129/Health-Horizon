from dash import html, dcc
import dash_bootstrap_components as dbc

# Results Page Layout
resultsLayout = dbc.Container([
    # Store prediction results (this is important - keeps the store in the layout)
    dcc.Store(id='prediction-store', storage_type='session'),
    
    dbc.Row([
        dbc.Col([
            html.H1("Heart Disease Risk Assessment", className="text-center mb-4"),
            html.Hr(),
        ], width=12)
    ]),
    
    # Results Display Area - This will be populated by the callback
    dbc.Row([
        dbc.Col([
            html.Div(id="results-output")
        ], width=12)
    ])
], fluid=True)