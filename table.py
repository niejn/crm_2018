import dash
import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

import pandas as pd
import plotly

app = dash.Dash()
app.config.supress_callback_exceptions = True

DF_WALMART = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/1962_2006_walmart_store_openings.csv')

DF_GAPMINDER = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
)
DF_GAPMINDER = DF_GAPMINDER[DF_GAPMINDER['year'] == 2007]

DF_SIMPLE = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E', 'F'],
    'y': [4, 3, 1, 2, 3, 6],
    'z': ['a', 'b', 'c', 'a', 'b', 'c']
})

_pages = {
    'page1': {
        'url': '/page1',
    },
    'page2': {
        'url': '/page2',
    }
}

app.layout = html.Div([
    html.Div(id="content"),
    dcc.Location(id='location', refresh=False)
])


def _get_page_content(name):
    if name == 'page1':
        return _render_page1()
    elif name == 'page2':
        return _render_page2()


def _render_page1():
    return html.H1('Page 1')


def _render_page2():
    return html.Div([
        html.H1('Page 2'),
        html.H4('Gapminder DataTable'),
        dt.DataTable(
            rows=DF_GAPMINDER.to_dict('records'),

            # optional - sets the order of columns
            columns=sorted(DF_GAPMINDER.columns),

            row_selectable=True,
            filterable=False,
            sortable=True,
            selected_rows=[],
            id='datatable-gapminder'
        ),
        html.Div(id='selected-indexes'),
        dcc.Graph(
            id='graph-gapminder'
        ),

        html.H4('Simple DataTable'),
        dt.DataTable(
            rows=DF_SIMPLE.to_dict('records'),
            filterable=False,
            sortable=True,
            id='datatable'
        ),
        dcc.Graph(
            id='graph'
        ),
    ], className="container")


@app.callback(
    Output('datatable-gapminder', 'selected_rows'),
    [Input('graph-gapminder', 'clickData')],
    [State('datatable-gapminder', 'selected_rows')])
def update_selected_rows(clickData, selected_rows):
    if clickData:
        new_points = [point['pointNumber'] for point in clickData['points']]
    else:
        new_points = []
    return new_points + selected_rows


@app.callback(
    Output('graph-gapminder', 'figure'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_rows')])
def update_figure(rows, selected_rows):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=3, cols=1,
        subplot_titles=('Life Expectancy', 'GDP Per Capita', 'Population',),
        shared_xaxes=True)
    marker = {'color': ['#0074D9'] * len(dff)}
    for i in (selected_rows or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace({
        'x': dff['country'],
        'y': dff['lifeExp'],
        'type': 'bar',
        'marker': marker
    }, 1, 1)
    fig.append_trace({
        'x': dff['country'],
        'y': dff['gdpPercap'],
        'type': 'bar',
        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'x': dff['country'],
        'y': dff['pop'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 800
    fig['layout']['margin'] = {
        'l': 20,
        'r': 20,
        't': 60,
        'b': 200
    }
    return fig


@app.callback(
    Output('graph', 'figure'),
    [Input('datatable', 'rows')])
def update_figure(rows):
    dff = pd.DataFrame(rows)
    return {
        'data': [{
            'x': dff['x'],
            'y': dff['y'],
            'text': dff['z'],
            'type': 'bar'
        }]
    }


@app.callback(
    Output('content', 'children'),
    [Input('location', 'pathname')])
def display_content(pathname):
    if pathname is None:
        return html.Div()
    matched = [c for c in _pages.keys()
               if _pages[c]['url'] == pathname]

    if matched and matched[0] != 'index':
        content = html.Div([
            html.Div(_get_page_content(matched[0])),
        ])
    else:
        content = html.H1('Invalid Page')

    return content


app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == '__main__':
    app.run_server(debug=True)