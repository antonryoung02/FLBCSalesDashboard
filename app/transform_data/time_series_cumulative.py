import pandas as pd

class TimeSeriesCumulativePipeline:    
    def __init__(self, categories_dataframe, mean_features, features_to_ignore):
        self.categories_dataframe = categories_dataframe
        self.mean_features = mean_features
        self.features_to_ignore = features_to_ignore

    # Will/Should it ever get a feature_to_ignore dataframe?
    def transform(self, dataframe_dict):
        cumulative_dataframe_dict = {}
        for name, df in dataframe_dict.items():
            if name not in self.features_to_ignore:
                aggregation_strategy = 'mean' if name in self.mean_features else 'sum'
                cumulative_dataframe_dict[name] = self._create_cumulative_dataframe(df, aggregation_strategy)
        return cumulative_dataframe_dict
            
    def _create_cumulative_dataframe(self, df, aggregation_strategy) -> pd.DataFrame:
        cumulative_df = pd.DataFrame()
        for c in self.categories_dataframe.get_columns():
            categories = self.categories_dataframe.get_values_for_column(c)
            categories = [n for n in categories if n in df.columns]
            cumulative_df[c] = df[categories].aggregate(aggregation_strategy, axis=1)
        return cumulative_df
