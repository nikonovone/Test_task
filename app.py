# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# загрузка необходимых библиотек
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from utils import * 

from plotly.subplots import make_subplots
from functools import partialmethod
from scipy.stats import mstats

# настройки к Pandas
pd.DataFrame.head = partialmethod(pd.DataFrame.head, n=2)
pd.options.display.max_rows = 13
pd.options.display.max_columns = 20

app = Dash(__name__)

# чтение данных
df = pd.read_csv("https://drive.google.com/file/d/1yiQRY0KAikINENbnA9xmRlANlg0ZTVHz/view?usp=sharing", index_col=0)

# уберем минимальную зарплату в 0 рублей и посмотрим на данные в 95% диапазоне
data = pd.Series(mstats.winsorize(
    df[df['vacancy_salary_from'] != 0]['vacancy_salary_from'], limits=[0, 0.05]))
fig1 = px.histogram(df, x=data, marginal="box")
fig1.update_layout(
    title='Распределение минимальной зарплаты в 95% вакансий',
    xaxis_title="Зарплата, руб",
    yaxis_title="Вакансии, шт",
    font=dict(
        family="Gotham Pro Medium",
        size=12,
    ),
)
# уберем все NaN и посмотрим на данные в 95% диапазоне
data = pd.Series(mstats.winsorize(
    df['vacancy_salary_to'].dropna(), limits=[0, 0.05]))

fig2 = px.histogram(x=data, marginal="box")
fig2.update_layout(
    title='Распределение максимальной зарплаты в 95% вакансий',
    xaxis_title="Зарплата, руб",
    yaxis_title="Количество, шт",
    font=dict(
        family="Gotham Pro Medium",
        size=12,
    ),
)

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

app.layout = html.Div(
    style={'font-family': 'Gotham Pro'},

    children=[
    html.H1(children='Hello Dash', style={'textAlign': 'center'}),

    html.Div(children=markdown_text, style={'textAlign': 'center'}),

    dcc.Graph(
        id='example-graph1',
        figure=fig1
    ),
    dcc.Graph(
        id='example-graph2',
        figure=fig2
    ),
    
])

if __name__ == '__main__':
    app.run_server(debug=True)
