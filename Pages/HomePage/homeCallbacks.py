from dash.dependencies import Input, Output, State
from dash import html

def homeCallbacks(app):
    """
    Register all callbacks for the Home page.
    Replace 'home' with 'patient' or 'results' for other pages.
    Replace function name with patientCallbacks or resultsCallbacks.
    """
    
    @app.callback(
        Output('home-output', 'children'),
        Input('home-button', 'n_clicks'),
        State('home-input', 'value'),
        prevent_initial_call=True
    )
    def update_home_output(n_clicks, input_value):
        if input_value:
            return html.Div([
                html.H5("Success!", className="text-success"),
                html.P(f"You entered: {input_value}"),
                html.P(f"Button clicked {n_clicks} time(s)")
            ])
        else:
            return html.Div([
                html.H5("Error", className="text-danger"),
                html.P("Please enter some text before submitting.")
            ])