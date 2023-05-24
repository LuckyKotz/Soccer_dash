from excel_procesing import *
import re
from dash_app_functions import *
team = "Arsenal - Chelsea"
team = re.split(r' stats | VS | - ', team)
team1_goals = get_team_(team[0], data, 'goals')
team2_goals = get_team_(team[1], data, 'goals')
team1_corners = get_team_(team[0], data, 'corners')
team2_corners = get_team_(team[1], data, 'corners')
team1_YC = get_team_(team[0], data, 'YC')
team2_YC = get_team_(team[0], data, 'YC')

if __name__ == '__main__':
    print(team1_corners)
