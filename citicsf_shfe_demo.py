# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout
from t1 import test_plotly, get_df_sqlite, get_instrumentids, get_df_by_instrument
import dash_table_experiments as dt
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
app = dash.Dash()


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


def test(test_df):
    # import plotly.plotly as py
    # import plotly
    # import plotly.graph_objs as go
    # from plotly.graph_objs import Scatter, Layout
    data = [go.Bar(
        x=test_df['期货公司会员简称'],
        y=test_df['成交量']
    )]

    # py.iplot(data, filename='basic-bar')
    # plotly.offline.plot
    plotly.offline.plot({
        "data": data,
        "layout": Layout(title="hello world")
    })
    return
# test_df = test_plotly()
instrumentids = get_instrumentids()

test_df, report_date = get_df_sqlite()
data = [go.Bar(
        x=test_df['期货公司会员简称'],
        y=test_df['成交量']
    )]

df = test_df
trace = go.Table(
    header=dict(values=df.columns,
                fill = dict(color='#C2D4FF'),
                align = ['left'] * 5),
    cells=dict(values=df,
               fill = dict(color='#F5F8FF'),
               align = ['left'] * 5))

# data = [trace]
# py.iplot(data, filename = 'pandas_table')
# layout = go.Layout(yaxis=dict(tickformat=".2%"))
'''xaxis: {
tickvals: x,
ticktext: dates.map(d => { return (new Date(d)).toDateString(); })
}'''
app.layout = html.Div(children=[
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='instrument-dropdown',
                options=[{'label': i, 'value': i } for i in instrumentids],
                value='all'
            ),

        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in ["上海期货交易所", "郑州商品交易所", "大连商品交易所", "中国金融期货交易所"]],
                value='Life expectancy at birth, total (years)'
            ),

        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    # html.H1(children='测试Demo'),
    #
    # html.Div(children='''
    #     上期所期货公司汇总排名前20.
    # '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': data,
            'layout': {
                'yaxis':{
                    'tickvals':[x for x in range(0, 2000000, 100000)],
                    # 'ticktext': [str(x/10000) + "万" for x in range(0, 2000000, 100000)],
                    'ticktext': ['%.0f'%(x/10000) + "万" for x in range(0, 2000000, 100000)],
                    'tickformat': '.0f',
                    'ticksuffix': '万',
                },
                'title': '<b>中信期货展示</b><br> 测试 (上期所 日期:{date})'.format(date=report_date)
            }
        }
    ),

    # generate_table(df),
    # html.H4('DataTable'),
    dt.DataTable(
        # Initialise the rows
        columns=['期货公司会员简称', '成交量', '比上交易日增减'],
        rows=df.to_dict('records'),
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='table'
    ),

])

@app.callback(Output('table', 'rows'), [Input('instrument-dropdown', 'value')])
def update_table(user_selection):
    """
    For user selections, return the relevant table
    """
    # df = get_df_sqlite(user_selection)
    if user_selection == None:
        return
    print(user_selection)
    if user_selection != 'all':
        df = get_df_by_instrument(user_selection)
    else:
        df = get_df_by_instrument()

    return df.to_dict('records')

@app.callback(Output('example-graph', 'figure'), [Input('instrument-dropdown', 'value')])
def update_bar(user_selection):
    """
    For user selections, return the relevant table
    """
    # df = get_df_sqlite(user_selection)
    if user_selection == None:
        return
    print(user_selection)
    if user_selection != 'all':
        df = get_df_by_instrument(user_selection)
    else:
        df = get_df_by_instrument()
    temp_data = [go.Bar(
        x=df['期货公司会员简称'],
        y=df['成交量']
    )]
    return {
            'data': temp_data,
            'layout': {
                'yaxis':{
                    'tickvals':[x for x in range(0, 2000000, 100000)],
                    # 'ticktext': [str(x/10000) + "万" for x in range(0, 2000000, 100000)],
                    'ticktext': ['%.0f'%(x/10000) + "万" for x in range(0, 2000000, 100000)],
                    # 'tickformat': '.0f',
                    # 'ticksuffix': '万',
                },
                'title': '<b>中信期货展示</b><br> 测试 (上期所 日期:{date})'.format(date=report_date)
            }
        }

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=False, port=8081, host='10.21.68.43')