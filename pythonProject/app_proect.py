from excel_procesing import *
import re
from figure_app import *
team = "Токио Верди - Кусатсу"
team = re.split(r' stats | VS | - ', team)
team1_goals = get_team_(team[0], data, 'goals')
team2_goals = get_team_(team[1], data, 'goals')
team1_fh = merge_goals(get_team_(team[0], data, 'fh'), team1_goals)
team2_fh = merge_goals(get_team_(team[0], data, 'fh'), team2_goals)
team1_corners = merge_goals(get_team_(team[0], data, 'corners'), team1_goals)
team2_corners = merge_goals(get_team_(team[1], data, 'corners'), team2_goals)
team1_YC = merge_goals(get_team_(team[0], data, 'YC'), team1_goals)
team2_YC = merge_goals(get_team_(team[0], data, 'YC'), team2_goals)

pd.options.display.max_columns = None

if __name__ == '__main__':
    #app.run_server(debug=True)
    print(team2_corners.head(3))
    #print(team2_goals["it1_opponent_category_goals"])