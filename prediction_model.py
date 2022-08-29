from catboost import CatBoostRegressor
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
import numpy as np
import warnings


warnings.filterwarnings("ignore", category=UserWarning)

X_train = pd.read_csv(r'train_data.csv')
y_train = pd.read_csv(r'train_data_targets.csv')

knn = KNeighborsRegressor(n_neighbors=25, p=1, weights='distance')
knn.fit(X_train, y_train)

cb_reg = CatBoostRegressor()
cb_reg.load_model("cb_reg.txt")

with open(r'weights.txt', 'r') as f:
    w_knn = float(f.readline()[:-1])
    w_cb_reg = float(f.readline())


def predict_object(price, week_day, category):
    cat_list = ['bread', 'hotcake', 'milk_or_sour_milk', 'cheese_cottage_cheese', 'others']

    df = pd.DataFrame({'price': pd.Series([price]),
                       'bread': pd.Series([0]),
                       'hotcake': pd.Series([0]),
                       'milk_or_sour_milk': pd.Series([0]),
                       'cheese_cottage_cheese': pd.Series([0]),
                       'others': pd.Series([0]),
                       'week_day_0': pd.Series([0]),
                       'week_day_1': pd.Series([0]),
                       'week_day_2': pd.Series([0]),
                       'week_day_3': pd.Series([0]),
                       'week_day_4': pd.Series([0])})

    df[cat_list[category]] = 1
    df['week_day_' + str(week_day)] = 1

    return int(predict(df).round()[0])


def predict(df):
    return np.reshape(knn.predict(df) * w_knn + np.reshape(cb_reg.predict(df), (df.shape[0], 1)) * w_cb_reg, (df.shape[0]))


def predict_file(file, exp):
    if exp == '.csv':
        df = pd.read_csv(file)
        res_name = file[:-4] + '_predicted.xlsx'
    else:
        df = pd.read_excel(file)
        res_name = file[:-5] + '_predicted.xlsx'

    df['res'] = pd.Series(predict(df).round())
    df.to_excel(res_name)

    return res_name
