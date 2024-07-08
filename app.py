
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
continent = df['country']
# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(external_stylesheets=external_stylesheets)
fig = px.scatter(df, x="gdpPercap", y="lifeExp",
                 size="pop", color="continent", hover_name="country",
                 log_x=True, size_max=60)

# App layout
app.layout = html.Div([
    html.Div(className='row', children='Plotly App with Data, Graph, and Controls',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

    html.Div(className='row', children=[
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
                       value='lifeExp',
                       inline=True,
                       id='my-radio-buttons-final')
    ]),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='histo-chart-final')
        ])
    ]),

    
    html.Header(
            "Geographic Distribution",
            style={"font-size": "30px", "textAlign": "center"},
        ),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='scatter-geo-chart-final')
        ]),

        html.Div(className='six columns', children=[
        dcc.Graph(
            id='life-exp-vs-gdp',
            figure=fig
        )
        ])
    ])

])

@callback(
    Output(component_id='histo-chart-final', component_property='figure'),
    Output(component_id='scatter-geo-chart-final', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    scatter_geo_fig = px.scatter_geo(df, locations="continent",
                                     size="pop", color="continent", hover_name="country",
                                     size_max=50, projection="natural earth")

    return fig, scatter_geo_fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8051)
