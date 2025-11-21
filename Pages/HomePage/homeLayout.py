from dash import html, dcc
import dash_bootstrap_components as dbc

# New Home Layout with Heart Icon and Blue Theme
homeLayout = html.Div([
    # Hero Section with CTA
    dbc.Container([
        # Main Content Row
        dbc.Row([
            # Left Side - CTA Text
            dbc.Col([
                html.Div([
                    html.H1(
                        "Early detection saves lives — assess your risk now",
                        className="hero-cta-text"
                    )
                ], className="cta-text-container")
            ], lg=5, md=12, className="cta-left"),
            
            # Middle - Button
            dbc.Col([
                html.Div([
                    html.A(
                        dbc.Button(
                            "Begin Assessment",
                            size="lg",
                            className="begin-assessment-btn",
                            id="begin-assessment-button"
                        ),
                        href="#patient-details-section",
                        style={'text-decoration': 'none', 'display': 'inline-block'}
                    )
                ], className="button-container")
            ], lg=12, md=12, className="d-flex align-items-center justify-content-center"),
            
            # Right Side - Team Info (Absolute positioned)
            html.Div([
                html.Div([
                    html.Div([
                        html.P("Presented by Team", className="team-presented-text"),
                        html.H1("Health Horizon", className="team-name-text")
                    ], className="team-info-container")
                ], className="team-text-container")
            ], className="cta-right")
        ], className="align-items-center hero-content-row")
    ], fluid=True, className="hero-section-new")
    
], className="ventro-home-new", style={'margin': '0', 'padding': '0'})
