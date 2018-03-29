# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import flask

# server = flask.Flask(__name__)
# app = dash.Dash(__name__, server=server)

app_flask = flask.Flask(__name__)
app = dash.Dash(__name__, server=app_flask, url_base_pathname='/pathname')

@app_flask.route('/plotly_dashboard')
def render_dashboard():
    return flask.redirect('/pathname')

@app_flask.route('/')
def render_home():
    return 'Hello, World!'
# app = dash.Dash()

# @server.route('/hello')
# def hello():
#     return 'Hello, World!'

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == '__main__':
    # app.run_server(debug=True)
    app_flask.run()
