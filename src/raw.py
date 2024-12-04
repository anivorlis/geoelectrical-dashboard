import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, dcc, html

from src.data_handler import AppData

# Jet-like colorscale
jet_colorscale = [
    [0, 'rgb(0, 0, 131)'],
    [0.125, 'rgb(0, 60, 170)'],
    [0.375, 'rgb(5, 255, 255)'],
    [0.625, 'rgb(255, 255, 0)'],
    [0.875, 'rgb(250, 0, 0)'],
    [1, 'rgb(128, 0, 0)']
]

def render(app: Dash, data: AppData) -> html.Div:

    # Raw Time-Series
    @app.callback(
        Output(component_id="raw-series", component_property="figure"),
        [Input(component_id="picker-dpid", component_property="value")]
    )
    def update_raw_series(dpid: str) -> go.Figure:
        local_data_raw = data.raw[data.raw.dpid==dpid]
        local_data_filtered = data.filtered[data.filtered.dpid==dpid]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=local_data_raw.dt, y=local_data_raw.apres, mode='markers', name='raw'))
        fig.add_trace(go.Scatter(x=local_data_filtered.dt, y=local_data_filtered.apres, mode='lines', name='filtered'))
        fig.update_layout(
            legend=dict(
                orientation='h',       # Set the orientation to horizontal
                xanchor='center',      # Anchor the x position to the center of the legend
                yanchor='bottom',      # Anchor the y position to the bottom of the legend
                x=0.5,                 # Position the legend horizontally in the center
                y=-0.3,                 # Position the legend slightly below the plot area
                bgcolor='rgba(255, 255, 255, 0.5)',  # Add a semi-transparent background
                bordercolor='rgba(0, 0, 0, 0.2)',    # Add a border with a slight transparency
                borderwidth=1          # Set the border width
            )
        )
        return fig

    # Raw Pseudo-Section
    @app.callback(
        Output(component_id="pseudo-section", component_property="figure"),
        Input(component_id="picker-time", component_property="value"),
        Input(component_id="picker-date", component_property="date"),
        Input(component_id="picker-task", component_property="value"),
        Input(component_id="raw-type-radio", component_property="value"),
        State(component_id="raw-vmin", component_property="value"),
        State(component_id="raw-vmax", component_property="value"),
        Input(component_id="raw-scale-radio", component_property="value")
    )
    def update_raw_2d(time: str, date: str, task_id: str, type_of_plot: str,
                      vmin: str, vmax: str, type_of_scale: str) -> go.Figure:
        if vmin is None:
            vmin = 30
        if vmax is None:
            vmax = 300
        dt = f"{date} {time}:00"
        local_data = data.raw[(data.raw.tid==task_id) & (data.raw.dt==dt)]
        if type_of_plot == 'res':
            c = local_data.apres
        else:
            c = local_data.charg
        if type_of_scale == 'log':
            c = np.log10(c)
        fig = go.Figure(data =
            go.Contour(x = local_data.fx, y=-local_data.fz, z=c, 
                       colorscale=jet_colorscale,
                       colorbar=dict(
                            orientation='h',
                            x=0.5,
                            y=-0.1,
                            xanchor="center",
                            yanchor="top",
                            lenmode="fraction",
                            len=0.5
            )))
        return fig

    return html.Div(
        [
            html.Div(
                [
                    html.H1("Pseudo-section"),
                    dcc.Graph(id='pseudo-section')
                ], className="raw-2d"
            ),
            html.Div(
                [
                    html.H1("Time-Series"),
                    dcc.Graph(id='raw-series')
                ], className="raw-2d"
            )
        ], className="raw"
    )
