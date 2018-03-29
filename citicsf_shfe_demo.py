# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout
from t1 import test_plotly, get_df_sqlite
import dash_table_experiments as dt
app = dash.Dash()

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

app.layout = html.Div(children=[
    html.H1(children='测试Demo'),

    html.Div(children='''
        上期所期货公司汇总排名前20.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': data,
            'layout': {
                'title': '<b>中信期货展示</b><br> 测试 (上期所 日期:{date})'.format(date=report_date)
            }
        }
    ),



])

if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=False, port=8081, host='10.21.68.43')