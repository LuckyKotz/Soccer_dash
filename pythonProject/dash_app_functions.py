import dash

import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output  # ,State

def dash_plotly_callbacks(df_team1, col, team1, team2, df_team2):
    # Настройка Фильтров
    # Голы для 1 команды
    match_selector = dcc.RangeSlider(
        id='range-slader-category',
        min=min(df_team1['diff_goals']),
        max=max(df_team1['diff_goals']),
        marks={-3.01: "-3", -2.01: "-2", -1.01: "-1", 0: "0", 0.99: "1", 1.99: "2", 2.99: "3"},
        step=1,
        value=[-2, 2],
    )
    # Голы для 2 команды
    match_selector_opponent = dcc.RangeSlider(
        id='range-slader-opponent',
        min=min(df_team2['diff_goals']),
        max=max(df_team2['diff_goals']),
        marks={-3.01: "-3", -2.01: "-2", -1.01: "-1", 0: "0", 0.99: "1", 1.99: "2", 2.99: "3"},
        step=1,
        value=[-2, 2],
    )
    # Забивная сила соперников 1 команды
    category_selector_team1 = dcc.Dropdown(
        id='category-selector-team1-it1',
        options=df_team1['it1_coeff_oppo_cattegory_' + col],
        value=['Слабые', 'Слабо-средние', 'Средние', 'Средне-сильные', 'Сильные'],
        multi=True
    )
    # Пропускная сила соперников 1 команды
    category_selector_opponent_team_1 = dcc.Dropdown(
        id='category-selector-team1-it2',
        options=df_team1['it2_coeff_oppo_cattegory_' + col],
        value=['Сильные', 'Средне-сильные', 'Средние', 'Слабо-Средние', 'Слабые'],
        multi=True
    )
    # Забивная сила соперников 2 команды
    category_selector_team2 = dcc.Dropdown(
        id='category-selector-team2-it1',
        options=df_team2['it1_coeff_oppo_cattegory_' + col],
        value=['Слабые', 'Слабо-средние', 'Средние', 'Средне-сильные', 'Сильные'],
        multi=True
    )
    # Пропускная сила соперников 2 команды
    category_selector_opponent_team_2 = dcc.Dropdown(
        id='category-selector-team2-it2',
        options=df_team2['it2_coeff_oppo_cattegory_' + col],
        value=['Сильные', 'Средне-сильные', 'Средние', 'Слабо-Средние', 'Слабые'],
        multi=True
    )

    app = dash.Dash(__name__,
                    external_stylesheets=[dbc.themes.MATERIA])

    app.layout = html.Div([
        dbc.Row(html.H1(f'{col} {team1} {(df_team1.it1.mean() * df_team2.it2_coeff.mean()):.2f} - \
        {(df_team2.it1.mean() * df_team1.it2_coeff.mean()):.2f} {team2} ')),

        dbc.Row([
            dbc.Col([
                html.Div(f'Select result match'),
                html.Div(match_selector),
            ],
                width={'size': 3, 'offset': 0}),
            dbc.Col([
                html.Div(f'Select result match'),
                html.Div(match_selector_opponent),
            ],
                width={'size': 3, 'offset': 4}),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(f'Select category opponent {team1} : {df_team2["it2_coeff_cattegory_" + col][0]}'),
                html.Div(category_selector_team2),
            ],
                width={'size': 'auto', 'offset': 0}),
            dbc.Col([
                html.Div(f'Select category opponent {team2} : {df_team1["it2_coeff_cattegory_" + col][0]}'),
                html.Div(category_selector_team2),
            ],
                width={'size': 'auto', 'offset': 3}),

        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='dist-match-chart'),
            ]),
            dbc.Col([
                dcc.Graph(id='dist-match-chart-opponent'),
            ]),
        ]),

    ],
        style={'margin-left': '20px',
               'margin-right': '20px'})

    @app.callback(
        Output(component_id='dist-match-chart', component_property='figure'),
        [Input(component_id='range-slader-category', component_property='value'),
         Input(component_id='category-selector-team1-it2', component_property='value'), ],

    )
    def update_dist_chart(simmilar_range, category_range):
        print("update_dist_chart вызван")
        print("simmilar_range:", simmilar_range)
        print("category_range:", category_range)

        chart_data = df_team1[(df_team1['diff_goals'] > simmilar_range[0]) &
                              (df_team1['diff_goals'] < simmilar_range[1]) &
                              (df_team1['it2_coeff_oppo_cattegory_' + col].isin(category_range))]

        fig = px.scatter(
            chart_data, x="opponent", y="it1",
            size='it2_coeff_oppo', size_max=24,
            text='it2_coeff_oppo',
            hover_name='diff_goals',
            color='play_', color_discrete_map={'Home': 'green', 'Away': 'red'},
            opacity=0.7,
            labels=dict(
                it1=team1,
                opponent=' ',
                play_='',
                it2_coeff_oppo='',
                cluster_label='',
                it2_coeff_oppo_cluster_label='',
            )
        )

        fig.update_xaxes(categoryorder='category ascending')

        return fig

    @app.callback(
        Output(component_id='dist-match-chart-opponent', component_property='figure'),
        [Input(component_id='range-slader-opponent', component_property='value'),
         Input(component_id='category-selector-team2-it2', component_property='value'), ],

    )
    def update_dist_chart_team2(category_range, simmilar_range):
        chart_data_team2 = df_team2[(df_team2['diff_goals'] > simmilar_range[0]) &
                                    (df_team2['diff_goals'] < simmilar_range[1]) &
                                    (df_team2['it2_coeff_oppo_cattegory_' + col].isin(category_range))]

        fig = px.scatter(
            chart_data_team2, x="opponent", y="it1",
            size='it2_coeff_oppo', size_max=24,
            text='it2_coeff_oppo',
            hover_name='diff_goals',
            color='play_', color_discrete_map={'Home': 'green', 'Away': 'red'},
            opacity=0.7,
            labels=dict(
                it1=team1,
                opponent=' ',
                play_='',
                it2_coeff_oppo='',
                cluster_label='',
                it2_coeff_oppo_cluster_label='',
            )
        )

        fig.update_xaxes(categoryorder='category ascending')

        return fig

    if __name__ == '__main__':
        app.run_server(debug=False)
