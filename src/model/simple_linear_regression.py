import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from src.base.regression_model_base import RegressionModelBase
from src.repository.rent_data_loader import RentDataLoader
from src.base.column_name import RentDataCN
from src.transform.transformer.data_concater import DataConcater
from src.transform.transformer.simple_datetime_aggregator import SimpleDatetimeAggregator
from src.transform.sampling.random_sampling import RandomSampling
from src.transform.transformer.location_column_extender import LocationColumnExtender
from src.transform.transformer.column_renamer import ColumnRenamer
from src.transform.transformer.string_to_datetime_converter import StringToDatetimeConverter


class SimpleLinearRegression(RegressionModelBase):
    def __init__(self):
        data_loader = RentDataLoader()

        pipline = Pipeline([
            ('data_concatenate', DataConcater()),
            ('renamer', ColumnRenamer()),
            ('str2datatime', StringToDatetimeConverter()),
            ('location_extender', LocationColumnExtender(year="2021", only_rent_location=True)),
            ('aggregate', SimpleDatetimeAggregator())
        ])

        self.__processed_data = pipline.fit_transform(data_loader.all_data)

        self.y = self.__processed_data[RentDataCN.RENT_COUNT]
        self.X = self.__processed_data.drop(columns=[RentDataCN.RENT_COUNT])
        self.X[RentDataCN.RENT_DATE] = self.X[RentDataCN.RENT_DATE].apply(lambda x: pd.to_datetime(x).timestamp())

        random_sampling = RandomSampling(self.X, self.y)
        self.X_train, self.X_test, self.y_train, self.y_test = random_sampling.train_test_split()

        super().__init__(self.X, self.y)
