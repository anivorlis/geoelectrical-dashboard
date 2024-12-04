import json

import dash_auth
from dash import Dash

from assets.config import APP_TITLE, EXTERNAL_STYLESHEET
from src.create_layout import create_layout
from src.data_handler import read_data

# Read usernames/passwords
with open("assets/auth.json", 'r') as fin:
    VALID_USERNAME_PASSWORD_PAIRS = json.load(fin)

data = read_data()

#print('-----------------------------')
#print(data.raw.head())
#print([dtype for dtype in data.raw.dtypes])
#print('-----------------------------')
#print(data.filtered.head())
#print([dtype for dtype in data.filtered.dtypes])
#print('-----------------------------')
#print(data.inverted.head())
#print([dtype for dtype in data.inverted.dtypes])

# Dashboard App
app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEET)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.title = APP_TITLE

# Dashboard Layout
app.layout = create_layout(app, data)

if __name__ == '__main__':
    app.run_server(debug=True)