import plotly.express as px
import plotly.graph_objects as go
#Положение легенды
charts_template = go.layout.Template(
    layout=dict(
        legend=dict(font=dict(family='Century Gothic'),#Задаем шрифт
                    orientation='h',#Расположение
                    title_text='',
                    x=0,#0 по Х
                    y=1.1)#Вверху
    )
)
def plot_figure(team1_df, col, team1, team2):
    fig1 = px.scatter(
        team1_df, x="opponent", y="it1",
        size=col+'_it2_opponent_coeff', size_max=24,
        text=col+'_it2_opponent',
        hover_name=col+'_it2_coeff_play',
        color='play_', color_discrete_map={'Home': 'green', 'Away': 'red'},
        opacity=0.7,
        labels=dict(
            it1=team1,
            opponent=' ',
            play_='',
            it2_coeff_oppo='',
            cluster_label='',
            it2_coeff_oppo_cluster_label='',
        ),
    )
    fig2 = px.scatter(
        team1_df, x="opponent", y='it2',
        size=col+'_it1_opponent_coeff',
        text=col+'_it1_opponent',
        hover_name=col+'_it1_coeff_play',
        color='play_', color_discrete_map={'Home': 'green', 'Away': 'red'},
        opacity=0.7,
        labels=dict(
            it2=team2,
            opponent=' ',
            play_='',
            it2_coeff_oppo='',
            cluster_label='',
            it2_coeff_oppo_cluster_label='',
        ),
    )
    fig1.update_xaxes(categoryorder='category ascending')
    fig2.update_xaxes(categoryorder='category ascending')
    fig1.add_hline(y=team1_df['it1'].mean().round(2), line_color='green', line_dash='dash',
                   annotation_text=f'MEAN: {team1_df["it1"].mean().round(2)}'),
    fig2.add_hline(y=team1_df['it2'].mean().round(2), line_color='green', line_dash='dash',
                   annotation_text=f'MEAN: {team1_df["it2"].mean().round(2)}')

    fig1.update_layout(template=charts_template)
    fig2.update_layout(template=charts_template)

    return fig1, fig2