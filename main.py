import dash
import os
import psycopg2
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Import layouts
from Pages.HomePage.homeLayout import homeLayout
from Pages.PatientDetails.patientLayout import patientLayout
from Pages.ResultsPage.resultsLayout import resultsLayout
from Pages.HistoryDashboard.historyLayout import historyLayout

# Import callbacks
from Pages.HomePage.homeCallbacks import homeCallbacks
from Pages.PatientDetails.patientCallbacks import patientCallbacks
from Pages.ResultsPage.resultsCallbacks import resultsCallbacks
from Pages.HistoryDashboard.historyCallbacks import historyCallbacks

# Create the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# App layout with offcanvas dashboard
app.layout = html.Div([
    # Bootstrap Icons CDN
    html.Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css"
    ),
    
    # Stores
    dcc.Store(id='prediction-store', storage_type='session'),
    dcc.Store(id='field-values-store', storage_type='session'),
    
    # Floating Dashboard Toggle Button
    html.Button([
        html.I(className="bi bi-clock-history", style={'fontSize': '1.5rem'}),
    ], id="open-history-dashboard", 
       className="floating-dashboard-btn",
       style={
           'position': 'fixed',
           'right': '30px',
           'top': '50%',
           'transform': 'translateY(-50%)',
           'zIndex': '1000',
           'backgroundColor': '#4f46e5',
           'color': 'white',
           'border': 'none',
           'borderRadius': '12px',
           'padding': '15px 20px',
           'cursor': 'pointer',
           'boxShadow': '0 4px 12px rgba(79, 70, 229, 0.4)',
           'transition': 'all 0.3s ease'
       }),
    
    # Offcanvas Dashboard (Right Side Panel)
    dbc.Offcanvas(
        historyLayout,
        id="history-offcanvas",
        title="Patient History Dashboard",
        is_open=False,
        placement="end",
        style={'width': '60%', 'maxWidth': '900px'}
    ),
    
    # Header with Logo
    html.Div([
        html.Div([
            html.H1("Ventro", className="ventro-logo-text"),
            html.Div([
                html.I(className="bi bi-heart-fill", id="animated-heart-icon")
            ], className="heart-icon-container")
        ], className="header-content")
    ], className="heart-icon-top-container"),
    
    # Main Content
    homeLayout,
    
    html.Div([
        html.Div(id='patient-section', children=patientLayout)
    ], id='patient-details-section', className="patient-details-section-wrapper"),
    
    html.Div([
        html.Div(id='results-section', children=resultsLayout)
    ], id='results-section-container', className="results-section-wrapper")
], className="main-app-container", style={'margin': '0', 'padding': '0'})

# Callback to toggle dashboard
@app.callback(
    Output("history-offcanvas", "is_open"),
    Input("open-history-dashboard", "n_clicks"),
    State("history-offcanvas", "is_open"),
    prevent_initial_call=True
)
def toggle_offcanvas(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Register all callbacks
homeCallbacks(app)
patientCallbacks(app)
resultsCallbacks(app)
historyCallbacks(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)