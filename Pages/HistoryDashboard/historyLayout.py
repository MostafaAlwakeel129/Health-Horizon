from dash import html, dcc
import dash_bootstrap_components as dbc

historyLayout = html.Div([
    # Header
    dbc.Row([
        dbc.Col([
            html.H2("Patient Assessment History", 
                   className="text-center mb-3",
                   style={'color': '#1a1d29', 'fontWeight': '700'}),
        ], width=12)
    ]),
    
    # Search Bar
    dbc.Row([
        dbc.Col([
            dbc.InputGroup([
                dbc.Input(
                    id="search-input",
                    placeholder="Search by patient name or ID...",
                    type="text",
                    style={'borderRadius': '8px 0 0 8px'}
                ),
                dbc.Button(
                    "Search",
                    id="search-button",
                    color="primary",
                    style={'borderRadius': '0 8px 8px 0'}
                ),
                dbc.Button(
                    "Show All",
                    id="show-all-button",
                    color="secondary",
                    className="ms-2",
                    style={'borderRadius': '8px'}
                )
            ], className="mb-3")
        ], width=12)
    ]),
    
    # Stats Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="total-assessments", children="0", 
                           className="text-center mb-0",
                           style={'color': '#4f46e5', 'fontSize': '2rem', 'fontWeight': 'bold'}),
                    html.P("Total Assessments", className="text-center text-muted mb-0",
                          style={'fontSize': '0.85rem'})
                ])
            ], style={'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="high-risk-count", children="0", 
                           className="text-center mb-0",
                           style={'color': '#ef4444', 'fontSize': '2rem', 'fontWeight': 'bold'}),
                    html.P("High Risk Patients", className="text-center text-muted mb-0",
                          style={'fontSize': '0.85rem'})
                ])
            ], style={'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="low-risk-count", children="0", 
                           className="text-center mb-0",
                           style={'color': '#10b981', 'fontSize': '2rem', 'fontWeight': 'bold'}),
                    html.P("Low Risk Patients", className="text-center text-muted mb-0",
                          style={'fontSize': '0.85rem'})
                ])
            ], style={'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
        ], width=4)
    ], className="mb-4"),
    
    
    # Patient History Table
    dbc.Row([
        dbc.Col([
            html.Div(id="history-table-container")
        ], width=12)
    ]),
    
    # Modal for viewing detailed patient info
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Patient Details")),
        dbc.ModalBody(id="patient-detail-modal-body"),
        dbc.ModalFooter([
            dbc.Button("Close", id="close-detail-modal", className="ms-auto")
        ])
    ], id="patient-detail-modal", size="lg", is_open=False),
    
    # Interval component to refresh data
    dcc.Interval(
        id='history-refresh-interval',
        interval=30*1000,  # Refresh every 30 seconds
        n_intervals=0
    )
], style={'padding': '20px'})