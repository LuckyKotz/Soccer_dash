from pandas import DataFrame
from data_functions import *

championat = 'england_PL.xlsx'
count_mathes = 20  # крайних матчей
# Загружаем файл Excel с данными
score = pd.read_excel(championat, sheet_name='match', index_col=0)
# Оставляем только сыгранные матчи
score: DataFrame = score[score['Unnamed: 4'].notna()]
# Переменовываем колонки в Домашнюю и выездную команду
score[['Team1', 'Team2']] = score[['Unnamed: 1', 'Unnamed: 2']]
# Форматируем данные о голах
score[['Team1_goals', 'Team2_goals', 'Team1_fh', 'Team2_fh']] = score['Unnamed: 3'].str.split(r'\:|\(', expand=True)
score['Team2_fh'] = score['Team2_fh'].str.replace(r'\)', '', regex=True)
# Форматируем данные об угловых и ЖК
score[['Team1_corners', 'Team2_corners']] = score['Unnamed: 5'].str.split(r'\:|\(', expand=True)
score[['Team1_YC', 'Team2_YC']] = score['Unnamed: 4'].str.split(r':|\(', expand=True)
# Оставляем только нужные колонки
score = score.loc[:, 'Team1':]
# Создаем список колонок с колличесвенными значениями
columns_kol_vo = ['Team1_goals', 'Team2_goals', 'Team1_fh', 'Team2_fh',
                  'Team1_corners', 'Team2_corners', 'Team1_YC', 'Team2_YC']
# Изменяем тип данных
score[columns_kol_vo] = score[columns_kol_vo].astype(int)
# Добавляем колонку Date
score["Date"] = score.index
# Создаем DataFrame с замененными значениями аномалий
score_without_outlier = score.copy()
# Результаты без аномалий
score_without_outlier[columns_kol_vo] = df_without_outlier(score_without_outlier[columns_kol_vo])
# Результаты, срез по колличеству  матчей. count_mathes колличество последних матчей
score_last_mathes = last_matches(score, count_mathes)
# Результаты без аномалий
score_last_mathes_wa = last_matches(score_without_outlier, count_mathes)
# Таблица средних значений
# Группируем и вычисляем средние показатели для "Team1" и "Team2"
home_avg = score_last_mathes_wa.groupby("Team1")[columns_kol_vo].mean()
home_avg = home_avg.rename(columns={'Team1_goals': 'goals_home', 'Team2_goals': 'goals_opponent_home',
                                    'Team1_fh': 'fh_home', 'Team2_fh': 'fh_opponent_home',
                                    'Team1_corners': 'corners_home', 'Team2_corners': 'corners_opponent_home',
                                    'Team1_YC': 'YC_home', 'Team2_YC': 'YC_opponent_home'})
home_avg.index.name = 'Team'
# Вычисляем средние значения для "Team2"
away_avg = score_last_mathes_wa.groupby("Team2")[columns_kol_vo].mean()
away_avg = away_avg.rename(columns={'Team1_goals': 'goals_opponent_away', 'Team2_goals': 'goals_away',
                                    'Team1_fh': 'fh_opponent_away', 'Team2_fh': 'fh_away',
                                    'Team1_corners': 'corners_opponent_away', 'Team2_corners': 'corners_away',
                                    'Team1_YC': 'YC_opponent_away', 'Team2_YC': 'YC_away'})
away_avg.index.name = 'Team'
# Объединяем таблицы по горизонтали
table_mean_Home_Away = pd.merge(home_avg, away_avg, how="inner", on="Team").round(2)
# Таблица Коэфициентов
# Вычисляем средние значения по колонкам
column_means = table_mean_Home_Away.columns
table_mean_liga = table_mean_Home_Away[column_means].mean()
# Вычисляем таблицу коэффициентов относительно лиги
table_coefficients = table_mean_Home_Away[column_means].div(table_mean_liga).round(2)
# Устанавливаем имена колонок
table_coefficients.columns = [col + '_coeff' for col in column_means]
# Таблица средних значений и коэфициетов
table_mean_coeff = pd.merge(table_mean_Home_Away, table_coefficients, how='left', left_index=True, right_index=True)
# Таблица средних значений и коэфициетов
table_mean_coeff = calculate_means_and_coefficients(table_mean_coeff)
# Общий DataFrame
data = merge_and_rename_columns(score_last_mathes, table_mean_coeff)
data.iloc[:, 2:] = data.iloc[:, 2:].round(2)
pd.options.display.max_columns = None

if __name__ == '__main__':
    print(data.head(3))
    print(data.columns)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
