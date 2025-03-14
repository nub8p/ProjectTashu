import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import KFold, cross_validate


class RegressionModelBase:

    __skf = KFold(n_splits=5, shuffle=True, random_state=42)
    __scoring = ['r2', 'neg_mean_squared_error', 'neg_mean_absolute_error']

    available_model = {
        'LinearRegression': LinearRegression(),
        'Ridge': Ridge(),
        'Lasso': Lasso(),
        'DecisionTreeRegressor': DecisionTreeRegressor(),
        'RandomForestRegressor': RandomForestRegressor(),
        'GradientBoostingRegressor': GradientBoostingRegressor()
    }

    __result = None
    __model_name = 'LinearRegression'

    def __init__(self, X: pd.DataFrame, y: pd.DataFrame):
        self.X, self.y = X, y
        self.model = self.available_model[self.__model_name]

    def fit(self):
        self.__result = cross_validate(self.model, self.X, self.y, cv=self.__skf,
                                       scoring=self.__scoring, return_estimator=True)

    def print_test_result(self):
        if not self.__result:
            self.fit()
        print(f"r2: {self.__result['test_r2']}")
        print(f"mse: {self.__result['test_neg_mean_squared_error']}")
        print(f"mae: {self.__result['test_neg_mean_absolute_error']}")

    def result(self):
        if not self.__result:
            self.fit()
        return self.__result

    def set_model(self, model_name: str):
        if model_name not in self.available_model:
            raise "Unsupported model"
        self.__model_name = self.available_model[model_name]
