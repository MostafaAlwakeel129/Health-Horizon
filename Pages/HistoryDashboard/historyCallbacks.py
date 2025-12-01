from dash.dependencies import Input, Output, State
from dash import html, dash_table
import dash
import dash_bootstrap_components as dbc
from utils.db_utils import db_manager
from datetime import datetime

def historyCallbacks(app):
    """Register callbacks for the history dashboard"""
    
    @app.callback(
        Output('history-table-container', 'children'),
        Output('total-assessments', 'children'),
        Output('high-risk-count', 'children'),
        Output('low-risk-count', 'children'),
        Input('search-button', 'n_clicks'),
        Input('show-all-button', 'n_clicks'),
        Input('history-refresh-interval', 'n_intervals'),
        Input('prediction-store', 'data'),  # Add this to trigger on new predictions
        State('search-input', 'value'),
        prevent_initial_call=False
    )
    def update_history_table(search_clicks, show_all_clicks, n_intervals, prediction_data, search_term):
        """Update the history table based on search or show all"""
        
        # Determine which button was clicked
        ctx = dash.callback_context
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'search-button' and search_term:
                assessments = db_manager.search_patients(search_term)
            else:
                assessments = db_manager.get_all_assessments()
        else:
            assessments = db_manager.get_all_assessments()
        
        # Calculate stats
        total_count = len(assessments)
        high_risk_count = sum(1 for a in assessments if a['risk_level'] == 'High Risk')
        low_risk_count = sum(1 for a in assessments if a['risk_level'] == 'Low Risk')
        
        # Create table if we have data
        if not assessments:
            table = dbc.Alert([
                html.H5("No Assessments Found", className="alert-heading"),
                html.P("No patient assessments have been recorded yet or no results match your search.")
            ], color="info")
        else:
            # Format data for display
            table_data = []
            for assessment in assessments:
                table_data.append({
                    'ID': assessment['patient_id'],
                    'Name': assessment['patient_name'],
                    'Age': assessment['age'],
                    'Sex': assessment['sex'],
                    'Risk %': f"{assessment['risk_probability']:.1f}%",
                    'Risk Level': assessment['risk_level'],
                    'Date': assessment['assessment_date'].strftime('%Y-%m-%d %H:%M') if isinstance(assessment['assessment_date'], datetime) else str(assessment['assessment_date'])
                })
            
            table = dash_table.DataTable(
                id='history-table',
                columns=[
                    {'name': 'Patient ID', 'id': 'ID'},
                    {'name': 'Name', 'id': 'Name'},
                    {'name': 'Age', 'id': 'Age'},
                    {'name': 'Sex', 'id': 'Sex'},
                    {'name': 'Risk Probability', 'id': 'Risk %'},
                    {'name': 'Risk Level', 'id': 'Risk Level'},
                    {'name': 'Assessment Date', 'id': 'Date'}
                ],
                data=table_data,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '12px',
                    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
                    'fontSize': '0.9rem'
                },
                style_header={
                    'backgroundColor': '#f1f3f5',
                    'fontWeight': 'bold',
                    'borderBottom': '2px solid #4f46e5',
                    'color': '#1a1d29'
                },
                style_data_conditional=[
                    {
                        'if': {'filter_query': '{Risk Level} = "High Risk"'},
                        'backgroundColor': 'rgba(239, 68, 68, 0.1)',
                        'color': '#dc2626'
                    },
                    {
                        'if': {'filter_query': '{Risk Level} = "Low Risk"'},
                        'backgroundColor': 'rgba(16, 185, 129, 0.1)',
                        'color': '#059669'
                    },
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgba(249, 250, 251, 0.5)'
                    }
                ],
                style_as_list_view=True,
                page_size=10,
                sort_action='native',
                filter_action='native',
                row_selectable='single',
                selected_rows=[],
                page_action='native'
            )
        
        return table, str(total_count), str(high_risk_count), str(low_risk_count)
    
    @app.callback(
        Output('patient-detail-modal', 'is_open'),
        Output('patient-detail-modal-body', 'children'),
        Input('history-table', 'selected_rows'),
        Input('close-detail-modal', 'n_clicks'),
        State('history-table', 'data'),
        State('patient-detail-modal', 'is_open'),
        prevent_initial_call=True
    )
    def toggle_patient_detail_modal(selected_rows, close_clicks, table_data, is_open):
        """Show detailed patient information in a modal"""
        
        ctx = dash.callback_context
        if not ctx.triggered:
            return False, ""
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'close-detail-modal':
            return False, ""
        
        if button_id == 'history-table' and selected_rows:
            # Get the selected patient's ID
            selected_patient_id = table_data[selected_rows[0]]['ID']
            
            # Fetch full patient details from database
            patient = db_manager.get_patient_by_id(selected_patient_id)
            
            if patient:
                # Create detailed view
                detail_content = html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.H4(patient['patient_name'], className="mb-3"),
                            html.P([html.Strong("Patient ID: "), patient['patient_id']]),
                            html.Hr()
                        ], width=12)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.H5("Personal Information", className="mb-3"),
                            html.P([html.Strong("Age: "), f"{patient['age']} years"]),
                            html.P([html.Strong("Sex: "), "Male" if patient['sex'] == 1 else "Female"]),
                        ], width=6),
                        dbc.Col([
                            html.H5("Risk Assessment", className="mb-3"),
                            html.H3(f"{patient['risk_probability']:.1f}%",
                                   style={'color': '#ef4444' if patient['risk_level'] == 'High Risk' else '#10b981'}),
                            html.P([html.Strong("Risk Level: "), patient['risk_level']]),
                        ], width=6)
                    ], className="mb-3"),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col([
                            html.H5("Clinical Data", className="mb-3"),
                            html.P([html.Strong("Chest Pain Type: "), str(patient['cp'])]),
                            html.P([html.Strong("Resting BP: "), f"{patient['trestbps']} mm Hg"]),
                            html.P([html.Strong("Cholesterol: "), f"{patient['chol']} mg/dl"]),
                            html.P([html.Strong("Fasting Blood Sugar: "), str(patient['fbs'])]),
                            html.P([html.Strong("Resting ECG: "), str(patient['restecg'])]),
                        ], width=6),
                        dbc.Col([
                            html.H5("Test Results", className="mb-3"),
                            html.P([html.Strong("Max Heart Rate: "), f"{patient['thalachh']} bpm"]),
                            html.P([html.Strong("Exercise Angina: "), str(patient['exang'])]),
                            html.P([html.Strong("ST Depression: "), str(patient['oldpeak'])]),
                            html.P([html.Strong("Slope: "), str(patient['slope'])]),
                            html.P([html.Strong("Major Vessels: "), str(patient['ca'])]),
                            html.P([html.Strong("Thalassemia: "), str(patient['thal'])]),
                        ], width=6)
                    ])
                ])
                
                return True, detail_content
        
        return is_open, ""