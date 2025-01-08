import pandas as pd
from app.categories_dataframe import categories_dataframe

class TimeSeriesCumulativePipeline:

    mean_features = ['*menu Price $', 'FC%', '*cm category', '*CM $', '*FC $']
    features_to_ignore = ['*categories']

    def transform(self, dataframe_dict):
        cumulative_dataframe_dict = {}
        for name, df in dataframe_dict.items():
            if name not in TimeSeriesCumulativePipeline.features_to_ignore:
                aggregation_strategy = 'mean' if name in TimeSeriesCumulativePipeline.mean_features else 'sum'
                cumulative_dataframe_dict[name] = self._create_cumulative_dataframe(df, aggregation_strategy)
        return cumulative_dataframe_dict
            
    def _create_cumulative_dataframe(self, df, aggregation_strategy) -> pd.DataFrame:
        cumulative_df = pd.DataFrame()
        for c in categories_dataframe.get_columns():
            categories = categories_dataframe.get_values_for_column(c)
            categories = [c for c in categories if c in df.columns]
            cumulative_df[c] = df[categories].aggregate(aggregation_strategy, axis=1)
        return cumulative_df
