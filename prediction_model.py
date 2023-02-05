from catboost import CatBoostRegressor
import pandas as pd
import numpy as np
import warnings
import pickle


warnings.filterwarnings("ignore", category=UserWarning)


class PredictionModel:
    def __init__(self):
        self.knn = pickle.load(open('knn.txt', 'rb'))
        self.cb_reg = CatBoostRegressor()
        self.cb_reg.load_model('cb_reg.txt')
        with open(r'weights.txt', 'r') as f:
            self.w_knn = float(f.readline()[:-1])
            self.w_cb_reg = float(f.readline())

    def predict_object(self, price, week_day, category):
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
        return int(self.predict(df).round()[0])

    def predict(self, df):
        return np.reshape(self.knn.predict(df) * self.w_knn +
                          np.reshape(self.cb_reg.predict(df), (df.shape[0], 1)) * self.w_cb_reg,
                          df.shape[0])

    def predict_file(self, file, exp):
        if exp == '.csv':
            df = pd.read_csv(file)
            res_name = file[:-4] + '_predicted.xlsx'
        else:
            df = pd.read_excel(file)
            res_name = file[:-5] + '_predicted.xlsx'
        df['res'] = pd.Series(self.predict(df).round())
        df.to_excel(res_name)
        return res_name
