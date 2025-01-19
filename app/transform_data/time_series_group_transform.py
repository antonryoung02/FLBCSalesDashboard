import pandas as pd

def time_series_group_transform(dataframe_dict:dict, categories:dict, mean_features:list, features_to_ignore:list) -> dict:
    cumulative_dataframe_dict = {}
    for name, df in dataframe_dict.items():
        if name not in features_to_ignore:
            aggregation_strategy = 'mean' if name in mean_features else 'sum'
            cumulative_dataframe_dict[name] = _create_cumulative_dataframe(df, aggregation_strategy, categories)
    return cumulative_dataframe_dict
        
def _create_cumulative_dataframe(df:pd.DataFrame, aggregation_strategy:str, categories:dict) -> pd.DataFrame:
    cumulative_df = pd.DataFrame()
    for c in categories:
        grouped_categories = [n for n in categories[c] if n in df.columns]
        cumulative_df[c] = df[grouped_categories].aggregate(aggregation_strategy, axis=1)
    return cumulative_df
