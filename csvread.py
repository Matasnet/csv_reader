import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.graph_objects as go
import base64 as b64
import io
import pandas as pd
from datetime import datetime


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # inicjacja aplikacji
server = app.server


app.layout = app.layout = html.Div([
    dcc.Upload(
        id='upload-1',
        children=html.Div([
            'Drag and drop or ',
            html.A('Select a File')
    ]),
    style={
        'width': '100%',
        'height': '60px',
        'textAlign': 'center',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'lineHeight': '60px'
    },
    multiple=True
    ),

    html.Div(id='div-1')
])


def parse_contents(content, name, date):
    content_type, content_string = content.split(',')

    decode = b64.b64decode(content_string)
    try:
        if 'csv' in name:
            df = pd.read_csv(io.StringIO(decode.decode('utf-8')))
        elif 'xls' in name:
            df = pd.read_excel(io.BytesIO(decode))
    except Exception as e:
        print(e)
        return html.Div([
            'Wystąpił błąd podczas przetwarzania pliku !'
        ])

    return html.Div([
        html.H5(name),
        html.H6(datetime.fromtimestamp(date)),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
        html.Hr(),
        html.Div('Row Content'),
        html.Pre(content[:300] + '...')
    ])

@app.callback(
    Output('div-1', 'children'),
    [Input('upload-1', 'contents')],
    [State('upload-1', 'filename'),
     State('upload-1', 'last_modified')]
)
def update_output(list_of_contents , list_of_names , list_of_dates):
    print(list_of_contents)
    print(list_of_names)
    print(list_of_dates)
    if list_of_contents is not None:
        children = [
            parse_contents(content, name, date) for content, name, date in zip(list_of_contents,
                                                                               list_of_names,
                                                                               list_of_dates)

        ]
        return children

if __name__ == '__main__':
    app.run_server(debug=False)
