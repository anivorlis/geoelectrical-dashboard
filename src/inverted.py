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
        Output(component_id="inv-series", component_property="figure"),
        Input(component_id="picker-task", component_property="value"),
        Input(component_id="inv-type-radio", component_property="value"),
        Input(component_id="inv-scale-radio", component_property="value")
    )
    def update_raw_series(task_id: str, type_of_plot: str, type_of_scale: str) -> go.Figure:
        local_data_inv = data.inverted[data.inverted.tid==task_id]
        lower_x, upper_x = 0, 32
        lower_z, upper_z = 0, 1
        local_data_inv = local_data_inv[ (lower_x < local_data_inv.x) &
                                         (upper_x > local_data_inv.x) &
                                         (lower_z < local_data_inv.z) &
                                         (upper_z > local_data_inv.z)]
        if type_of_plot == 'res':
            mean_res_by_dt = local_data_inv.groupby('dt')['resistivity'].mean()
            plot_x = mean_res_by_dt.index.tolist()
            plot_y = mean_res_by_dt.values.tolist()
        else:
            mean_res_by_dt = local_data_inv.groupby('dt')['chargeability'].mean()
            plot_x = mean_res_by_dt.index.tolist()
            plot_y = mean_res_by_dt.values.tolist()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=plot_x, y=plot_y, mode='lines+markers'))
        return fig
    

    # Raw Cross-Section
    @app.callback(
        Output(component_id="cross-section", component_property="figure"),
        Input(component_id="picker-time", component_property="value"),
        Input(component_id="picker-date", component_property="date"),
        Input(component_id="picker-task", component_property="value"),
        Input(component_id="inv-type-radio", component_property="value"),
        State(component_id="inv-vmin", component_property="value"),
        State(component_id="inv-vmax", component_property="value"),
        Input(component_id="inv-scale-radio", component_property="value")
    )
    def update_inv_2d(time: str, date: str, task_id: str, type_of_plot: str,
                      vmin: str, vmax: str, type_of_scale: str) -> go.Figure:
        if vmin is None:
            vmin = 30
        if vmax is None:
            vmax = 300
        dt = f"{date} {time}:00"
        local_data = data.inverted[(data.inverted.tid==task_id) & (data.inverted.dt==dt)]
        if type_of_plot == 'res':
            c = local_data.resistivity
        else:
            c = local_data.chargeability
        if type_of_scale == 'log':
            c = np.log10(c)
        fig = go.Figure(data =
            go.Contour(x = local_data.x, y=-local_data.z, z=c,
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
                    html.H1("Cross-section"),
                    dcc.Graph(id='cross-section')
                ], className="inv-2d"
            ), 
            html.Div(
                [
                    html.H1("Time-Series"),
                    dcc.Graph(id='inv-series')
                ], className="inv-1d"
            )
        ], className="inv"
    )