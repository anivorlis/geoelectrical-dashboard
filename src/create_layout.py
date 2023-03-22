from dash import Dash, dcc, html, Input, Output

from src.data_handler import AppData

from src import (
    settings, 
    raw, 
    inverted
)

def create_layout(app: Dash, data: AppData) -> html.Div:
    return html.Div(
        [
            # Header
            html.Div(
                [
                    html.H1("Dashboard for Geoelectrical Monitoring Data", className="app-name")
                ], className="head"
            ),
            # Main
            html.Div(
                [
                    settings.render(app, data),
                    # raw data
                    raw.render(app, data),
                    # inverted data
                    inverted.render(app, data)
                ], className="main"
            )
        ], className="app"
        )