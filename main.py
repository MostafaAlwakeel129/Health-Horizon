import dash
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

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='prediction-store', storage_type='session'),  
    html.Div(id='page-content')
])

# Navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Patient Details", href="/patient")),
        dbc.NavItem(dbc.NavLink("Results", href="/results")),
    ],
    brand="Health Horizon",
    brand_href="/",
    color="primary",
    dark=True,
    className="mb-4"
)

# Main app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', style={'padding': '20px'})
])

# Callback to switch pages
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/patient':
        return patientLayout
    elif pathname == '/results':
        return resultsLayout
    else:
        return homeLayout

# Register callbacks from all pages
homeCallbacks(app)
patientCallbacks(app)
resultsCallbacks(app)

if __name__ == '__main__':
    app.run(debug=True, port=8050)