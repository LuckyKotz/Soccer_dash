import pandas as pd

# Для Обработки Шахматки
def clean_data(file_path, sheet_name, column_range, team_replacements):
    data = pd.read_excel(file_path, sheet_name=sheet_name, index_col=0)
    df = data.iloc[:, column_range]
    # create a new DataFrame and fill it with values from the original DataFrame
    new_df = pd.DataFrame(columns=["Team1", "Team2", "score"])
    for i in range(len(df)):
        for j in range(len(df.columns)):
            if j != i + 1 and not pd.isna(df.iloc[i, j]):
                new_df = new_df.append({"Team1": i, "Team2": df.columns[j], "score": df.iloc[i, j]}, ignore_index=True)
            if j == i + 1 and not pd.isna(df.iloc[i, j]):
                new_df = new_df.append({"Team1": i, "Team2": df.columns[j], "score": df.iloc[i, j]}, ignore_index=True)
    # clean the new DataFrame
    new_df[['Team1', 'Team2']] = new_df[['Team1', 'Team2']].astype(int)
    new_df['Team1'] = new_df['Team1'] + 1
    new_df['Team1'] = new_df['Team1'].map(data.Team.to_dict())
    new_df['Team2'] = new_df['Team2'].map(data.Team.to_dict())
    new_df[['Team1_score', 'Team2_score']] = new_df['score'].str.split(r':|\(', expand=True)
    new_df = new_df[['Team1', 'Team2', 'Team1_score', 'Team2_score']]
    new_df = new_df.replace(team_replacements)
    new_df = new_df[new_df['Team2_score'].notna()]
    return new_df


# Заменяем вбросы(Аномалии) на верхний и нижний квантиль
def df_without_outlier(data_frame):
    columns_names = list(data_frame.columns)
    for column in columns_names:
        Q1 = data_frame[column].quantile(0.3)
        Q3 = data_frame[column].quantile(0.65)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        data_frame.loc[data_frame[column] < lower_bound, column] = lower_bound
        data_frame.loc[data_frame[column] > upper_bound, column] = upper_bound
    return data_frame


# Фильтр по последним матчам, count_mathes колличесво матчей
def last_matches(data_frame, count_matches):
    last_matches_df = pd.DataFrame()
    for team in data_frame['Team1'].unique():
        last = data_frame[(data_frame['Team1'] == team) | (data_frame['Team2'] == team)].head(count_matches)
        last_matches_df = pd.concat([last_matches_df, last])
    return last_matches_df


def calculate_means_and_coefficients(table_mean_coeff):
    prefixes = ["goals", "YC", "corners", "fh"]

    for prefix in prefixes:
        columns = [f"{prefix}_home", f"{prefix}_away"]
        table_mean_coeff[f"{prefix}_mean"] = table_mean_coeff[columns].mean(axis=1)
        opponent_columns = [f"{prefix}_opponent_home", f"{prefix}_opponent_away"]
        table_mean_coeff[f"{prefix}_mean_opponent"] = table_mean_coeff[opponent_columns].mean(axis=1)
        coeff_columns = [f"{prefix}_home_coeff", f"{prefix}_away_coeff"]
        table_mean_coeff[f"{prefix}_coeff_mean"] = table_mean_coeff[coeff_columns].mean(axis=1)
        opponent_coeff_columns = [f"{prefix}_opponent_home_coeff", f"{prefix}_opponent_away_coeff"]
        table_mean_coeff[f"{prefix}_coeff_mean_opponent"] = table_mean_coeff[opponent_coeff_columns].mean(axis=1)

    return table_mean_coeff

# Обьеденить Средние показатели с календарем сыгранных матчей
def merge_and_rename_columns(score_last_matches, table_coefficients):
    columns_table = table_coefficients.columns

    table_coefficients_team1 = table_coefficients.copy()
    table_coefficients_team1.columns = [col + '_Team1' for col in columns_table]

    table_coefficients_team2 = table_coefficients.copy()
    table_coefficients_team2.columns = [col + '_Team2' for col in columns_table]

    merge_df_team1 = pd.merge(score_last_matches, table_coefficients_team1, left_on="Team1", right_index=True,
                              how='left')
    merge_df_team2 = pd.merge(score_last_matches, table_coefficients_team2, left_on="Team2", right_index=True,
                              how='left')

    merge_df = pd.merge(merge_df_team1, merge_df_team2, how='left')
    return merge_df.drop_duplicates()


# Функция для строковой колонки результат
def result(row):
    if row > 0:
        return 'win'
    elif row == 0:
        return 'draw'
    else:
        return 'lose'


# Последние матчи по срезу клубов
def get_team_(team, df, df_name):
    home_df = pd.DataFrame()
    home_df[['opponent',
             'it1', 'it2', 'Date',
             df_name + '_it1',
             df_name + '_it2',
             df_name + '_it1_coeff',
             df_name + '_it2_coeff',
             df_name + '_it1_coeff_play',
             df_name + '_it2_coeff_play',
             df_name + '_it1_opponent',
             df_name + '_it2_opponent',
             df_name + '_it1_opponent_coeff',
             df_name + '_it2_opponent_coeff'
             ]] = df[df['Team1'] == team][['Team2',
                                           'Team1_' + df_name, 'Team2_' + df_name, 'Date',
                                           df_name + '_mean_Team1',
                                           df_name + '_mean_opponent_Team1',
                                           df_name + '_coeff_mean_Team1',
                                           df_name + '_coeff_mean_opponent_Team1',
                                           df_name + '_home_coeff_Team1',
                                           df_name + '_opponent_home_coeff_Team1',
                                           df_name + '_mean_Team2',
                                           df_name + '_mean_opponent_Team2',
                                           df_name + '_coeff_mean_Team2',
                                           df_name + '_coeff_mean_opponent_Team2'
                                           ]]
    home_df['play_'] = 'Home'

    away_df = pd.DataFrame()
    away_df[['opponent',
             'it1', 'it2', 'Date',
             df_name + '_it1',
             df_name + '_it2',
             df_name + '_it1_coeff',
             df_name + '_it2_coeff',
             df_name + '_it1_coeff_play',
             df_name + '_it2_coeff_play',
             df_name + '_it1_opponent',
             df_name + '_it2_opponent',
             df_name + '_it1_opponent_coeff',
             df_name + '_it2_opponent_coeff'
             ]] = df[df['Team2'] == team][['Team1',
                                           'Team2_' + df_name, 'Team1_' + df_name, 'Date',
                                           df_name + '_mean_Team2',
                                           df_name + '_mean_opponent_Team2',
                                           df_name + '_coeff_mean_Team2',
                                           df_name + '_coeff_mean_opponent_Team2',
                                           df_name + '_away_coeff_Team2',
                                           df_name + '_opponent_away_coeff_Team2',
                                           df_name + '_mean_Team1',
                                           df_name + '_mean_opponent_Team1',
                                           df_name + '_coeff_mean_Team1',
                                           df_name + '_coeff_mean_opponent_Team1'
                                           ]]
    away_df['play_'] = 'Away'

    teams = pd.concat([home_df, away_df], ignore_index=True)
    teams['Date'] = pd.to_datetime(teams['Date'], format='%d.%m.%Y')
    teams['diff_' + df_name] = teams['it1'] - teams['it2']
    teams['result_' + df_name] = teams['diff_' + df_name].apply(result)

    # создаем колонку по категории соперника
    bins = [0, 0.85, 0.95, 1.05, 1.15, 10]
    bins_it2 = [0, 0.85, 0.95, 1.05, 1.15, 10]

    names = ['Очень слабые', 'Слабые', 'Средние', 'Сильные', 'Очень сильные']
    names_it2 = ['Очень сильные', 'Сильные', 'Средние', 'Слабые', 'Очень слабые']

    teams['it1_opponent_category_' + df_name] = pd.cut(teams[df_name + '_it1_opponent_coeff'],
                                                        bins, labels=names)
    teams['it2_opponent_category_' + df_name] = pd.cut(teams[df_name + '_it2_opponent_coeff'],
                                                        bins_it2, labels=names_it2)

    teams['it1_category_' + df_name] = pd.cut(teams[df_name + '_it1_coeff'],
                                               bins, labels=names)
    teams['it2_category_' + df_name] = pd.cut(teams[df_name + '_it2_coeff'],
                                               bins_it2, labels=names_it2)

    options = []
    for k in names:
        options.append({'label': k, 'value': k})

    options_opponents = []
    for k in names:
        options_opponents.append({'label': k, 'value': k})

    return teams.sort_values('Date')


# приджойнить голы к dataframe с переменование +goals,
def merge_goals(indicator_market, Df_goals):
    Df_goals = Df_goals.rename(columns={'it1': 'it1_goals',
                                        'it2': 'it2_goals',
                                        },
                               )# Переменовали колонки для мерджа
    Df_goals.drop(columns='Date', inplace=True)
    indicator_market = pd.merge(indicator_market, Df_goals, on=['opponent', 'play_'], how='left')
    return indicator_market
