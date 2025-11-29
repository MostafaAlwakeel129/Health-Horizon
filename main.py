import dash
import os
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Import layouts
from Pages.HomePage.homeLayout import homeLayout
from Pages.PatientDetails.patientLayout import patientLayout
from Pages.ResultsPage.resultsLayout import resultsLayout

# Import callbacks - Import from the callback FILES
from Pages.HomePage.homeCallbacks import homeCallbacks
from Pages.PatientDetails.patientCallbacks import patientCallbacks
from Pages.ResultsPage.resultsCallbacks import resultsCallbacks

# Create the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server


# Single page layout combining all three sections
app.layout = html.Div([
    # Bootstrap Icons CDN for heart icon
    html.Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css"
    ),
    
    # Store for prediction data
    dcc.Store(id='prediction-store', storage_type='session'),
    # Store for field values to preserve them
    dcc.Store(id='field-values-store', storage_type='session'),
    
    # Header with Logo and Branding
    html.Div([
        html.Div([
            html.H1("Ventro", className="ventro-logo-text"),
            html.Div([
                html.I(className="bi bi-heart-fill", id="animated-heart-icon")
            ], className="heart-icon-container")
        ], className="header-content")
    ], className="heart-icon-top-container"),
    
    # Home section at the top
    homeLayout,
    
    # Patient details section in the middle
    html.Div([
        html.Div(id='patient-section', children=patientLayout)
    ], id='patient-details-section', className="patient-details-section-wrapper"),
    # Results section at the bottom
    html.Div([
        html.Div(id='results-section', children=resultsLayout)
    ], id='results-section-container', className="results-section-wrapper")
], className="main-app-container", style={'margin': '0', 'padding': '0'})

# Register callbacks from all pages
homeCallbacks(app)
patientCallbacks(app)
resultsCallbacks(app)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
