from dash import html, dcc
import dash_bootstrap_components as dbc

# Home Page Layout
homeLayout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Home Page", className="text-center mb-4"),
            html.Hr(),
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Input Section")),
                dbc.CardBody([
                    dbc.Label("Enter some text:"),
                    dbc.Input(
                        id="home-input",
                        type="text",
                        placeholder="Type something for Home...",
                        className="mb-3"
                    ),
                    dbc.Button(
                        "Submit",
                        id="home-button",
                        color="primary",
                        className="w-100"
                    )
                ])
            ], className="mb-4")
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Output Section")),
                dbc.CardBody([
                    html.Div(
                        id="home-output",
                        children="Your output will appear here...",
                        style={'minHeight': '100px'}
                    )
                ])
            ])
        ], width=12)
    ])
], fluid=True)