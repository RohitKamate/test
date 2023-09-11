import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


df = pd.read_excel('C:/Users/rohit/Downloads/Book2.xlsx')


app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=df['Date'].min(),
        end_date=df['Date'].max(),
        display_format='DD-MM-YYYY'
    ),
    dcc.Graph(id='call-volume-graph'),

])


@app.callback(
    Output('call-volume-graph', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_graph(start_date, end_date):
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    fig = px.bar(
        filtered_df,
        x='Date',
        y='Inbound Call Volume',
        title='Inbound Call Volume',
        labels={'Date': 'Date', 'Inbound Call Volume': 'Inbound Call Volume'}
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
