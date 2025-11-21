from dash import html, dcc
import dash_bootstrap_components as dbc

# Results Page Layout - Clean Report Display
resultsLayout = dbc.Container([
    # Results Display Area - This will be populated by the callback
    dbc.Row([
        dbc.Col([
            html.Div(id="results-output")
        ], width=12)
    ])
], fluid=True)
