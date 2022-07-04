# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# Загрузка необходимых библиотек
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output, dash_table
from utils import *
from plotly.subplots import make_subplots
from functools import partialmethod
from scipy.stats import mstats

# Настройки к Pandas
pd.DataFrame.head = partialmethod(pd.DataFrame.head, n=2)
pd.options.display.max_rows = 13
pd.options.display.max_columns = 20

app = Dash(__name__)

# Чтение датасета
#df = pd.read_csv("https://media.githubusercontent.com/media/nikonovone/Test_task/master/data.csv", index_col=0)
df = pd.read_csv("data.csv", index_col=0)

font = dict(
    family="Gotham Pro Medium",
    size=12,
)

# Мин. зарплата
data = pd.Series(mstats.winsorize(
    df[df['vacancy_salary_from'] != 0]['vacancy_salary_from'], limits=[0, 0.05]))
min_salary = px.histogram(df, x=data, marginal="box", color_discrete_sequence=['#6189c9'])
min_salary.update_layout(
    title='Распределение минимальной зарплаты в 95% вакансий',
    xaxis_title="Зарплата, руб",
    yaxis_title="Вакансии, шт",
    font=font,
)

# Макс. зарплата
data = pd.Series(mstats.winsorize(
    df['vacancy_salary_to'].dropna(), limits=[0, 0.05]))
max_salary = px.histogram(x=data, marginal="box",  color_discrete_sequence=['#6189c9'])
max_salary.update_layout(
    title='Распределение максимальной зарплаты в 95% вакансий',
    xaxis_title="Зарплата, руб",
    yaxis_title="Количество, шт",
    font=font
)
# Образование
data = df['vacancy_offer_education_id']
education_cat = px.histogram(x=data, marginal="box", color_discrete_sequence=['#6189c9'])
education_cat.update_layout(
    title='Распределение категорий образования в вакансиях',
    xaxis_title="Категории",
    yaxis_title="Вакансии, шт",
    font=font
)
data = df.groupby('vacancy_offer_education_id')['vacancy_salary_from'].median().sort_values()
education_bar = px.bar(x=data.index, y=data,  color_discrete_sequence=['#6189c9'])
education_bar.update_layout(
    title='Зависимость медианны минимальной зарплаты от типа образования',
    xaxis_title="Образование",
    yaxis_title="Медианная зарплата",
    font=font,
    yaxis={'categoryorder':'total ascending'}
)
education_bar.update_yaxes(range=[32000, 42000])

# Опыт работы
df['vacancy_offer_experience_year_count'].replace(
    [-1, -100], np.nan, inplace=True)
data = df['vacancy_offer_experience_year_count']
offer_experience = px.histogram(x=data, marginal="box",  color_discrete_sequence=['#6189c9'])
offer_experience.update_layout(
    title='Распределение требуемого опыта работы в вакансиях',
    yaxis_title="Вакансии, шт",
    xaxis=dict(
        tickmode='linear',
        title="Опыт работы, лет",
    ),
    font=font
)

# Города
data = pd.Series(mstats.winsorize(df['vacancy_city_id'], limits=[0, 0.05]))
cities = px.histogram(x=data, marginal="box",  color_discrete_sequence=['#6189c9'])
cities.update_layout(
    title='Распределение id городов в 95% вакансий',
    xaxis_title="ID города",
    yaxis_title="Вакансии, шт",
    font=font
)

# Корреляция числовых признаков
corrs = df.drop(columns=['vacany_company_id', 'vacancy_is_agency',
                         'vacancy_offer_experience_year_id', 'vacancy_city_id']).corr()
correlations =  px.imshow(np.array(np.round(corrs,2)),
                text_auto=True,
                aspect="auto",
                color_continuous_scale=px.colors.sequential.Cividis,
                x=['Зарплата от', 'Зарплата до', 'Опыт работы', 'Диапазон зарплаты', ' '],
                y=['Зарплата от', 'Зарплата до', 'Опыт работы', 'Диапазон зарплаты',' ']
                )
correlations.update_layout(
    title='Карта корреляций числовых признаков',
    font=font
)

# Срез по зарплатам городов
#slice_cities = df[df['vacancy_salary_from'] > 10000].groupby(
#'vacancy_city_id')[['vacancy_salary_from', 'vacancy_salary_to']].median()[:10].sort_values(
  #  'vacancy_salary_from', ascending=False)[:10]

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🐬", className="header-emoji"),
                html.H1(
                    children="Bimbo аналитика",
                    className="header-title"
                ),
                html.P(
                    children="Анализируем тестовые датасеты с 1995 года",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.H1(children='Основные распределения данных'),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='min_salary',
                            figure=min_salary,
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='max_salary',
                            figure=max_salary,
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='education_cat',
                            figure=education_cat,
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='education_bar',
                            figure=education_bar,
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='offer_experience',
                            figure=offer_experience,
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='cities',
                            figure=cities,
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='correlations',
                            figure=correlations,
                        ),
                    ],
                    className="card",
                )
            ],
            className="graphs",
        ),
        html.Div(
            children=[


                html.H6(
                    "Change the value in the text box to see callbacks in action!"),
                html.Div([
                    "Input: ",
                    
                    dcc.Input(id='my-input',
                              value='initial value', type='text')
                ]),
                html.Br(),
                html.Div(id='my-output'),


            ]
        )
    ]
)




if __name__ == '__main__':
    app.run_server(debug=True)
