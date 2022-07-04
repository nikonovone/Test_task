# вспомогательные функции
import pandas as pd

def isna_print(df: pd.Series(dtype='float64')):
    '''
    Печатает количество NaN объектов
    '''
    print('Количество NaN объектов: ', df.isna().sum())


def value_counts_modify(df: pd.Series(dtype='float64'), threshold=0.9) -> pd.Series(dtype='float64'):
    '''
    Возвращает наиболее часто встречающиеся значения из датасета,
    сумма которых равна пороговому значению threshold от общего количества данных
    '''
    booleans = df.value_counts(normalize=True).cumsum() <= threshold
    ans = df.value_counts()[booleans]
    return ans


def percentile(n: float):
    '''
    Возвращает заданный перцентиль
    '''
    def percentile_(x):
        return np.percentile(x, n)
    percentile_.__name__ = 'percentile_%s' % n
    return percentile_


def range_salary(x):
    '''
    Возвращает вилку зарплат
    '''
    if np.isnan(x[0]):
        return 0
    else:
        return x[0]-x[1]
