import dash
from app_proect import *
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from figure_app import *

def range_similar(df_columns):
    list_select = []
    if df_columns == "Очень слабые":
        list_select.extend(['Очень слабые', 'Слабые'])
    if df_columns == "Слабые":
        list_select.extend(['Очень слабые', 'Слабые', 'Средние'])
    if df_columns == "Средние":
        list_select.extend(['Слабые', 'Средние', 'Сильные'])
    if df_columns == "Сильные":
        list_select.extend(['Средние', 'Сильные', 'Очень сильные'])
    if df_columns == "Очень сильные":
        list_select.extend(['Сильные', 'Очень сильные'])
    return list_select

# Фильтр слайдер. Итоговая разница голов. -2, 2 по дэфолту. ALL figure
range_diff_goals = dcc.RangeSlider(
    id='range-diff-goals',
    min=-4,
    max=4,
    marks={-3: "-3", -2: "-2", -1: "-1", 0: "0", 1: "1", 2: "2", 3: "3", },
    step=1,
    value=[-3, 3],
)
default_value = ['Очень слабые', 'Слабые', 'Средние', 'Сильные', 'Очень сильные']
'''Тело Приложения'''
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.SOLAR])

app.layout = html.Div([#ТИТУЛЬНЫЙ ЛИСТ
    html.H1(f'{team[0]}  - {team[1]}',
            style={'color': 'white',
                   'fontSize': 'auto'}),
    html.H2(f'{(team1_goals["it1"].mean() * team2_goals["goals_it2_coeff"].mean()).round(2)} - '
            f'{(team2_goals["it1"].mean() * team1_goals["goals_it2_coeff"].mean()).round(2)}',
            style={'color': 'white',
                   'fontsize': 'auto'}),
    dbc.Row([
        dbc.Col([
            html.Div(f'Select result range diff_goals'),
            html.Div(range_diff_goals),
        ], width={'size': 6, 'offset': 'auto'}),
        dbc.Col([
            dbc.Button('Apply', id='button-diff-goals', n_clicks=0, className='mr-1', color='blue'),
        ], width={'size': 'auto', 'offset': 'auto'})
    ]),
    dbc.Tabs([
        dbc.Tab([#ВКЛАДКА ГОЛЫ
            dbc.Row([#1КОЛОНКА
                html.Div(f'{(team1_goals["goals_it1"][0] * team2_goals["goals_it2_coeff"][0]).round(2)}'
                         f' - {(team2_goals["goals_it1"][0] * team1_goals["goals_it2_coeff"][0]).round(2)}'),
                dbc.Col([#1ГРАФИК
                    html.Div(f'{team[1]} в ОБОРОНЕ {team2_goals["it2_category_goals"][0]}'),
                    dcc.Dropdown(
                        id='Team1-VS-similar-def-Team2',
                        options=[{"label": category, "value": category} for category in
                                 team1_goals["it2_opponent_category_goals"].unique()],
                        value=range_similar(team2_goals["it2_category_goals"][0]),
                        multi=True
                    ),
                    dcc.Graph(id='graph-goals-id1'),
                ], width={'size': 6, 'offset': 'auto'}),
                dbc.Col([#2ГРАФИК
                    html.Div(f'{team[0]} в АТАКЕ {team1_goals["it1_category_goals"][0]}'),
                    dcc.Dropdown(
                        id="Team2-VS-similar-att-Team1",
                        options=[{"label": category, "value": category} for category in
                                 team2_goals["it1_opponent_category_goals"].unique()],
                        value=range_similar(team1_goals["it1_category_goals"][0]),
                        multi=True
                    ),
                    dcc.Graph(id='graph-goals-id2'),
                ], width={'size': 6, 'offset': 'auto'}),
            ]),
            dbc.Row([#2КОЛОНКА
                dbc.Col([#3ГРАФИК
                    html.Div(f'{team[0]} в ОБОРОНЕ {team1_goals["it2_category_goals"][0]}'),
                    dcc.Dropdown(
                        id='Team2-VS-similar-def-Team1',
                        options=[{"label": category, "value": category} for category in
                                 team2_goals["it2_opponent_category_goals"].unique()],
                        value=range_similar(team1_goals["it2_category_goals"][0]),
                        multi=True
                    ),
                    dcc.Graph(id='graph-goals-id3'),
                ], width={'size': 6, 'offset': 'auto'}),
                dbc.Col([#4ГРАФИКУ
                    html.Div(f'{team[1]} в АТАКЕ {team2_goals["it1_category_goals"][0]}'),
                    dcc.Dropdown(
                        id='Team1-VS-similar-att-Team2',
                        options=[{"label": category, "value": category} for category in
                                 team1_goals["it1_opponent_category_goals"].unique()],
                        value=range_similar(team2_goals["it1_category_goals"][0]),
                        multi=True
                    ),
                    dcc.Graph(id='graph-goals-id4'),
                ], width={'size': 6, 'offset': 'auto'}),
            ])
        ], label='goals'),
        dbc.Tab([#ВКЛАДКА 1 ТАЙМ
            html.Div(f'{(team1_fh["fh_it1"][0] * team2_fh["fh_it2_coeff"][0]).round(2)}'
                     f' - {(team2_fh["fh_it1"][0] * team1_fh["fh_it2_coeff"][0]).round(2)}'),
            dbc.Row([#1СТРОКА
                dbc.Col([#1ГРАФИК
                    html.Div(f'{team[1]} в ОБОРОНЕ {team2_fh["it2_category_fh"][0]}'),
                    dcc.Dropdown(
                        id='fh-Team1-VS-similar-def-Team2',
                        options=[{"label": category, "value": category} for category in
                                 team1_fh["it2_opponent_category_fh"].unique()],
                        value=range_similar(team2_fh["it2_category_fh"][0]),
                        multi=True
                    ),
                    dcc.Graph(id='graph-fh-id1'),
                ], width={'size': 6, 'offset': 'auto'}),
                dbc.Col([#2ГРАФИК
                    html.Div(f'{team[0]} в АТАКЕ {team1_fh["it1_category_fh"][0]}'),
                    dcc.Dropdown(
                        id="fh-Team2-VS-similar-att-Team1",
                        options=[{"label": category, "value": category} for category in
                                 team2_fh["it1_opponent_category_fh"].unique()],
                        value=range_similar(team1_fh["it1_category_fh"][0]),
                        multi=True
                    ),
                    dcc.Graph(id='graph-fh-id2'),
                ], width={'size': 6, 'offset': 'auto'}),
            ]),
            dbc.Row([#2СТРОКА
                dbc.Col([#3ГРАФИК
                    html.Div(f'{team[0]} в ОБОРОНЕ {team1_fh["it2_category_fh"][0]}'),
                    dcc.Dropdown(
                        id='fh-Team2-VS-similar-def-Team1',
                        options=[{"label": category, "value": category} for category in
                                 team2_fh["it2_opponent_category_fh"].unique()],
                        value=range_similar(team1_fh["it2_category_fh"][0]),
                        multi=True
                    ),
                    dcc.Graph(id='graph-fh-id3'),
                ], width={'size': 6, 'offset': 'auto'}),
                dbc.Col([#4ГРАФИК
                    html.Div(f'{team[1]} в АТАКЕ {team2_fh["it1_category_fh"][0]}'),
                    dcc.Dropdown(
                        id='fh-Team1-VS-similar-att-Team2',
                        options=[{"label": category, "value": category} for category in
                                 team1_fh["it1_opponent_category_fh"].unique()],
                        value=range_similar(team2_fh["it1_category_fh"][0]),
                        multi=True
                    ),
                    dcc.Graph(id='graph-fh-id4'),
                ], width={'size': 6, 'offset': 'auto'}),
            ])
        ], label='first_half'),
        dbc.Tab([#ВКЛАДКА УГЛОВЫЕ
            dbc.Row([#1СТРОКА
                html.Div(f'{(team1_corners["corners_it1"][0] * team2_corners["corners_it2_coeff"][0]).round(2)}'
                         f' - {(team2_corners["corners_it1"][0] * team1_corners["corners_it2_coeff"][0]).round(2)}'),
                dbc.Col([#1 ГРАФИК
                    html.Div(f'{team[1]} в ОБОРОНЕ {team2_corners["it2_category_corners"][0]}'),
                    dcc.Dropdown(
                        id='corners-Team1-VS-similar-def-Team2',
                        options=[{"label": category, "value": category} for category in
                                 team1_corners["it2_opponent_category_corners"].unique()],
                        value=range_similar(team2_corners["it2_category_corners"][0]),
                        multi=True
                    ),
                    dcc.Graph(id='graph-corners-id1'),
                ], width={'size': 6, 'offset': 'auto'}),
                dbc.Col([#2 ГРАФИК
                    html.Div(f'{team[0]} в АТАКЕ {team1_corners["it1_category_corners"][0]}'),
                    dcc.Dropdown(
                        id="corners-Team2-VS-similar-att-Team1",
                        options=[{"label": category, "value": category} for category in
                                 team2_corners["it1_opponent_category_corners"].unique()],
                        value=range_similar(team1_corners["it1_category_corners"][0]),
                        multi=True
                    ),
                    dcc.Graph(id='graph-corners-id2'),
                ], width={'size': 6, 'offset': 'auto'}),
            ]),
            dbc.Row([
                dbc.Col([#3ГРАФИК
                    html.Div(f'{team[0]} в ОБОРОНЕ {team1_corners["it2_category_corners"][0]}'),
                    dcc.Dropdown(
                        id='corners-Team2-VS-similar-def-Team1',
                        options=[{"label": category, "value": category} for category in
                                 team2_corners["it2_opponent_category_corners"].unique()],
                        value=range_similar(team1_corners["it2_category_corners"][0]),
                        multi=True
                    ),
                    dcc.Graph(id='graph-corners-id3'),
                ], width={'size': 6, 'offset': 'auto'}),
                dbc.Col([#4 ГРАФИК
                    html.Div(f'{team[1]} в АТАКЕ {team2_corners["it1_category_corners"][0]}'),
                    dcc.Dropdown(
                        id='corners-Team1-VS-similar-att-Team2',
                        options=[{"label": category, "value": category} for category in
                                 team1_corners["it1_opponent_category_corners"].unique()],
                        value=range_similar(team2_corners["it1_category_corners"][0]),
                        multi=True
                    ),
                    dcc.Graph(id='graph-corners-id4'),
                ], width={'size': 6, 'offset': 'auto'}),
            ]),
        ], label='corners'),
        dbc.Tab([# ВКЛАДКА ДАННЫЕ
            dash_table.DataTable(score.to_dict('records'), [{"name": i, "id": i} for i in score.columns],
                                 page_size=13, id='table-page-data'),
        ], label='data')
    ])
])
@app.callback(
    Output(component_id="table-page-data", component_property="data"),
    Input(component_id="button-diff-goals", component_property="n_clicks"),
    State(component_id="range-diff-goals", component_property="value")
)
def update_data_page(n_clicks, diff_goals_table_page):
    score_df = score[(score["Team1_goals"] - score["Team2_goals"] >= diff_goals_table_page[0]) &
                     (score["Team1_goals"] - score["Team2_goals"] <= diff_goals_table_page[1])]
    return score_df.to_dict('records')

'''СТРАНИЦА ГОЛЫ 1 ГРАФИК'''
@app.callback(
    Output(component_id="graph-goals-id1", component_property="figure"),
    [Input(component_id="range-diff-goals", component_property="value"),
     Input(component_id="Team1-VS-similar-def-Team2", component_property="value")]
)
def update_graph1(diff_goals, range_category):
    team1_filtr = team1_goals[(team1_goals["diff_goals"] >= diff_goals[0]) &
                              (team1_goals["diff_goals"] <= diff_goals[1]) &
                              (team1_goals["it2_opponent_category_goals"]).isin(range_category)]

    fig = plot_figure(team1_filtr, 'goals', team[0], team[1])[0]
    return fig

'''СТРАНИЦА ГОЛЫ. 2 ГРАФИК'''
@app.callback(
    Output(component_id="graph-goals-id2", component_property="figure"),
    [Input(component_id="range-diff-goals", component_property="value"),
     Input(component_id="Team2-VS-similar-att-Team1", component_property="value")]
)
def update_graph2(range_diff_goals2, range_category2):
    team2_filtr = team2_goals[(team2_goals["diff_goals"] >= range_diff_goals2[0]) &
                              (team2_goals["diff_goals"] <= range_diff_goals2[1]) &
                              (team2_goals["it1_opponent_category_goals"]).isin(range_category2)
                              ]
    fig = plot_figure(team2_filtr, 'goals', team[0], team[1])[1]
    return fig

'''СТРАНИЦА ГОЛЫ. 3 ГРАФИК'''
@app.callback(
    Output(component_id="graph-goals-id3", component_property="figure"),
    [Input(component_id="range-diff-goals", component_property="value"),
     Input(component_id="Team2-VS-similar-def-Team1", component_property="value")]
)
def update_graph3(range_diff_goals3, range_category3):
    team2_filtr = team2_goals[(team2_goals["diff_goals"] >= range_diff_goals3[0]) &
                              (team2_goals["diff_goals"] <= range_diff_goals3[1]) &
                              (team2_goals["it2_opponent_category_goals"]).isin(range_category3)
                              ]
    fig = plot_figure(team2_filtr, 'goals', team[1], team[0])[0]
    return fig

'''СТРАНИЦА ГОЛЫ. 4 ГРАФИК'''
@app.callback(
    Output(component_id="graph-goals-id4", component_property="figure"),
    [Input(component_id="range-diff-goals", component_property="value"),
     Input(component_id="Team1-VS-similar-att-Team2", component_property="value")]
)
def update_graph4(range_diff_goals4, range_category4):
    team1_filtr = team1_goals[(team1_goals["diff_goals"] >= range_diff_goals4[0]) &
                              (team1_goals["diff_goals"] <= range_diff_goals4[1]) &
                              (team1_goals["it1_opponent_category_goals"]).isin(range_category4)
                              ]
    fig = plot_figure(team1_filtr, 'goals', team[1], team[0])[1]
    return fig


@app.callback(
    Output(component_id="graph-corners-id1", component_property="figure"),
    [Input(component_id="range-diff-goals", component_property="value"),
     Input(component_id="corners-Team1-VS-similar-def-Team2", component_property="value")]
)
def update_graph_corners1(range_diff_goals1, range_category):
    team1_filtr = team1_corners[(team1_corners["diff_goals"] >= range_diff_goals1[0]) &
                                (team1_corners["diff_goals"] <= range_diff_goals1[1]) &
                                (team1_corners["it2_opponent_category_corners"]).isin(range_category)
                                ]
    fig = plot_figure(team1_filtr, 'corners', team[0], team[1])[0]
    return fig


@app.callback(
    Output(component_id="graph-corners-id2", component_property="figure"),
    [Input(component_id="range-diff-goals", component_property="value"),
     Input(component_id="corners-Team2-VS-similar-att-Team1", component_property="value")]
)
def update_graph_corners2(range_diff_goals2, range_category2):
    team2_filtr = team2_corners[(team2_corners["diff_goals"] >= range_diff_goals2[0]) &
                                (team2_corners["diff_goals"] <= range_diff_goals2[1]) &
                                (team2_corners["it1_opponent_category_corners"]).isin(range_category2)
                                ]
    fig = plot_figure(team2_filtr, 'corners', team[0], team[1])[1]
    return fig


@app.callback(
    Output(component_id="graph-corners-id3", component_property="figure"),
    [Input(component_id="range-diff-goals", component_property="value"),
     Input(component_id="corners-Team2-VS-similar-def-Team1", component_property="value")]
)
def update_graph_corners3(range_diff_goals3, range_category3):
    team2_filtr = team2_corners[(team2_corners["diff_goals"] >= range_diff_goals3[0]) &
                                (team2_corners["diff_goals"] <= range_diff_goals3[1]) &
                                (team2_corners["it2_opponent_category_corners"]).isin(range_category3)
                                ]
    fig = plot_figure(team2_filtr, 'corners', team[1], team[0])[0]
    return fig


@app.callback(
    Output(component_id="graph-corners-id4", component_property="figure"),
    [Input(component_id="range-diff-goals", component_property="value"),
     Input(component_id="corners-Team1-VS-similar-att-Team2", component_property="value")]
)
def update_graph_corners4(range_diff_goals4, range_category4):
    team1_filtr = team1_corners[(team1_corners["diff_goals"] >= range_diff_goals4[0]) &
                                (team1_corners["diff_goals"] <= range_diff_goals4[1]) &
                                (team1_corners["it1_opponent_category_corners"]).isin(range_category4)
                                ]
    fig = plot_figure(team1_filtr, 'corners', team[1], team[0])[1]
    return fig


@app.callback(
    Output(component_id="graph-fh-id1", component_property="figure"),
    [Input(component_id="range-diff-goals", component_property="value"),
     Input(component_id="fh-Team1-VS-similar-def-Team2", component_property="value")]
)
def update_graph_fh1(range_diff_goals2, range_category):
    team1_filtr = team1_fh[(team1_fh["diff_goals"] >= range_diff_goals2[0]) &
                           (team1_fh["diff_goals"] <= range_diff_goals2[1]) &
                           (team1_fh["it2_opponent_category_fh"]).isin(range_category)
                           ]
    fig = plot_figure(team1_filtr, 'fh', team[0], team[1])[0]
    return fig


@app.callback(
    Output(component_id="graph-fh-id2", component_property="figure"),
    [Input(component_id="range-diff-goals", component_property="value"),
     Input(component_id="fh-Team2-VS-similar-att-Team1", component_property="value")]
)
def update_graph_fh2(range_diff_goals2, range_category2):
    team2_filtr = team2_fh[(team2_fh["diff_goals"] >= range_diff_goals2[0]) &
                           (team2_fh["diff_goals"] <= range_diff_goals2[1]) &
                           (team2_fh["it1_opponent_category_fh"]).isin(range_category2)
                           ]
    fig = plot_figure(team2_filtr, 'fh', team[0], team[1])[1]
    return fig


@app.callback(
    Output(component_id="graph-fh-id3", component_property="figure"),
    [Input(component_id="range-diff-goals", component_property="value"),
     Input(component_id="fh-Team2-VS-similar-def-Team1", component_property="value")]
)
def update_graph_fh3(range_diff_goals3, range_category3):
    team2_filtr = team2_fh[(team2_fh["diff_goals"] >= range_diff_goals3[0]) &
                           (team2_fh["diff_goals"] <= range_diff_goals3[1]) &
                           (team2_fh["it2_opponent_category_fh"]).isin(range_category3)
                           ]
    fig = plot_figure(team2_filtr, 'fh', team[1], team[0])[0]
    return fig


@app.callback(
    Output(component_id="graph-fh-id4", component_property="figure"),
    [Input(component_id="range-diff-goals", component_property="value"),
     Input(component_id="fh-Team1-VS-similar-att-Team2", component_property="value")]
)
def update_graph_fh4(range_diff_goals4, range_category4):
    team1_filtr = team1_fh[(team1_fh["diff_goals"] >= range_diff_goals4[0]) &
                           (team1_fh["diff_goals"] <= range_diff_goals4[1]) &
                           (team1_fh["it1_opponent_category_fh"]).isin(range_category4)
                           ]
    fig = plot_figure(team1_filtr, 'fh', team[1], team[0])[1]
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
