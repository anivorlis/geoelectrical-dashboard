import datetime
from collections import defaultdict
from typing import Generator

import numpy as np
from dash import Dash, Input, Output, dcc, html

from src.data_handler import AppData


def get_dropbox_options(values: np.ndarray|list[str]) -> list[dict[str, str]]:
    return [ {"label": value, "value": value} for value in values]

def string_to_date(string: str) -> datetime.date:
    #Format should be YYYY-MM-DD
    return datetime.date(*[int(value) for value in string.split('-')])

def date_to_string(date: datetime.date) -> str:
    # YYYY-MM-DD format
    return f"{date.year}-{date.month:02}-{date.day:02}"

def find_missing_days(dates: list[str], start_date: datetime.date, end_date: datetime.date) -> list[datetime.date]:
    def daterange(start_date: datetime.date, end_date: datetime.date) -> Generator[datetime.date, None, None]:
        for n in range(int((end_date - start_date).days)):
            yield start_date + datetime.timedelta(n)
    dates_set = set([string_to_date(date) for date in dates])
    all_dates_possible = set([date for date in daterange(start_date, end_date+datetime.timedelta(1))])
    dates_missing = all_dates_possible - dates_set
    return list(dates_missing)

def render(app: Dash, data: AppData) -> html.Div:

    # Update Time from date
    @app.callback(
        Output(component_id="picker-time", component_property="options"),
        Output(component_id="picker-time", component_property="value"),
        Input(component_id="picker-date", component_property="date")
    )
    def update_times(date: str) -> tuple[list[str], str]:
        options = get_dropbox_options(times_for_date[date])
        values = [option["value"] for option in options]
        return values, values[-1]

    # Update DPID from Task
    @app.callback(
        Output(component_id="picker-dpid", component_property="options"),
        Output(component_id="picker-dpid", component_property="value"),
        Input(component_id="picker-task", component_property="value")
    )
    def update_dpid(task_id: str) -> tuple[list[str], str]:
        local_dpid = data.raw.dpid[data.raw.tid == task_id]
        options = get_dropbox_options(np.sort(local_dpid.unique()))
        values = [option["value"] for option in options]
        return values, values[0]
    

    dpids = np.sort(data.raw.dpid.unique())
    task_ids = np.sort(data.inverted.tid.unique())

    # Datetime manipulation for settings
    datetimes = data.raw.dt.unique()
    dates = set()
    times_for_date = defaultdict(list)
    for dt in datetimes:
        date, time = dt.split(' ')
        dates.add(date)
        times_for_date[date].append(time[:-3])
    dates = sorted(list(dates))

    # Calendar
    min_date = string_to_date(dates[0])
    max_date = string_to_date(dates[-1])
    missing_dates = find_missing_days(dates, min_date, max_date)
    default_date = max_date

    # dropbox time
    dropbox_time_options = get_dropbox_options(times_for_date[date_to_string(default_date)])
    dropbox_time_value = dropbox_time_options[0]["value"]
    # dropbox task
    dropbox_task_options = get_dropbox_options(task_ids)
    dropbox_task_value = dropbox_task_options[0]["value"]
    # dropbox dpid
    dropbox_dpid_options = get_dropbox_options(dpids)
    dropbox_dpid_value = dropbox_dpid_options[0]["value"]

    return html.Div(
        [
            html.H1("Settings"),
            html.Div(
                [
                    html.H3("Date"),
                    dcc.DatePickerSingle(
                        id='picker-date',
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        date=max_date,
                        disabled_days=missing_dates,
                        display_format="YYYY-MM-DD",
                        className="picker-date"
                    ),
                    html.H3("Time"),
                    dcc.Dropdown(id='picker-time',
                        options=dropbox_time_options,
                        value=dropbox_time_value,
                        clearable=False,
                        className="picker-time"),
                ], className="datetime"
            ),
            html.Hr(className='hr-background'),
            html.Div(
                [
                    html.H3("Task"),
                    dcc.Dropdown(id='picker-task',
                        options=dropbox_task_options,
                        value=dropbox_task_value,
                        clearable=False,
                        className="picker-task"),
                    html.H3("DPID"),
                    dcc.Dropdown(id='picker-dpid',
                        options=dropbox_dpid_options,
                        value=dropbox_dpid_value,
                        clearable=False,
                        className="picker-dpid")
                ], className="task"
            ),
            html.Hr(className='hr-background'),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Type of Plot (Raw)"),
                            dcc.RadioItems(
                                id='raw-type-radio',
                                options=[
                                    {'label': 'resistivity', 'value': 'res'},
                                    {'label': 'chargeability', 'value': 'ip'}
                                ],
                                value='res',
                                className="raw-type-radio"
                            )
                        ], className="raw-plottype-container"
                    ),
                    html.Div(
                        [
                            html.H3('vminx'),
                            html.H3('vmax'),
                            dcc.Input(
                                id="raw-vmin",
                                type="text",
                                placeholder=30,
                                className="raw-colorscale-textbox"
                            ),
                            dcc.Input(
                                id="raw-vmax",
                                type="text",
                                placeholder=300,
                                className="raw-colorscale-textbox"
                            ),
                        ], className="raw-range-container"
                    ),
                    html.Div(
                        [
                            html.H3("Scale"),
                            dcc.RadioItems(
                                id='raw-scale-radio',
                                options=[
                                    {'label': 'log', 'value': 'log'},
                                    {'label': 'linear', 'value': 'linear'}
                                ],
                                value='log',
                                className="raw-scale-radio"
                            )
                        ], className="raw-scale-container"
                    )
                ], className="raw-2d-options"
            ),
            html.Hr(className='hr-background'),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Type of Plot (Inv)"),
                            dcc.RadioItems(
                                id='inv-type-radio',
                                options=[
                                    {'label': 'resistivity', 'value': 'res'},
                                    {'label': 'chargeability', 'value': 'ip'}
                                ],
                                value='res',
                                className="inv-type-radio"
                            )
                        ], className="inv-plottype-container"
                    ),
                    html.Div(
                        [
                            html.H3('vminx'),
                            html.H3('vmax'),
                            dcc.Input(
                                id="inv-vmin",
                                type="text",
                                placeholder=30,
                                className="inv-colorscale-textbox"
                            ),
                            dcc.Input(
                                id="inv-vmax",
                                type="text",
                                placeholder=300,
                                className="inv-colorscale-textbox"
                            ),
                        ], className="inv-range-container"
                    ),
                    html.Div(
                        [
                            html.H3("Scale"),
                            dcc.RadioItems(
                                id='inv-scale-radio',
                                options=[
                                    {'label': 'log', 'value': 'log'},
                                    {'label': 'linear', 'value': 'linear'}
                                ],
                                value='log',
                                className="inv-scale-radio"
                            )
                        ], className="inv-scale-container"
                    )
                ], className="inv-2d-options"
            )
        ], className="settings"
    )