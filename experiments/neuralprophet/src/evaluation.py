from itertools import product

import numpy as np
import pandas as pd
from neuralforecast.losses.numpy import mape, smape

from src.data import get_data


def evaluate(lib: str, dataset: str, group: str):
    try:
        forecast = pd.read_csv(f'data/{lib}-forecasts-{dataset}-{group}.csv')
    except:
        return None
    if lib == 'statsforecast':
        col = 'ets_statsforecast'
    elif lib == 'neuralprophet':
        col = 'neuralprophet'
    
    y_test, horizon, freq, seasonality = get_data('data/', dataset, group, False)
    y_hat = forecast[col].values.reshape(-1, horizon)
    y_test = y_test['y'].values.reshape(-1, horizon)

    evals = {}
    for metric in (mape, smape):
        metric_name = metric.__name__
        loss = metric(y_test, y_hat, axis=1).mean()
        evals[metric_name] = loss 

    evals = pd.DataFrame(evals, index=[f'{dataset}_{group}']).rename_axis('dataset').reset_index()
    times = pd.read_csv(f'data/{lib}-time-{dataset}-{group}.csv')
    evals = pd.concat([evals, times], axis=1)

    return evals


if __name__ == '__main__':
    groups = ['ETTm2', 'Other', 'Yearly', 'Quarterly', 'Monthly', 'Other', 'Daily', 'Hourly', 'Weekly']
    lib = ['statsforecast', 'neuralprophet']
    datasets = ['LongHorizon', 'ERCOT', 'M3', 'Tourism', 'M4']
    evaluation = [evaluate(lib, dataset, group) for lib, group in product(lib, groups) for dataset in datasets]
    evaluation = [eval_ for eval_ in evaluation if eval_ is not None]
    evaluation = pd.concat(evaluation)
    evaluation = evaluation[['dataset', 'model', 'mape', 'smape', 'time']]
    evaluation['time'] /= 60 #minutes
    evaluation = evaluation.set_index(['dataset', 'model']).stack().reset_index()
    evaluation.columns = ['dataset', 'model', 'metric', 'val']
    evaluation = evaluation.set_index(['dataset', 'metric', 'model']).unstack().round(3)
    evaluation = evaluation.droplevel(0, 1).reset_index()
    evaluation.to_csv('data/evaluation.csv')
    print(evaluation)
