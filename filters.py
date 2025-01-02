
class BaseFilter:
    def __init__(self, display_pipeline):
        self.display_pipeline = display_pipeline

    def filter(self, dataframe_dict:dict, columns:list, index:list, names:list):
        filtered_dict = dataframe_dict.copy()   
        if names:
            filtered_dict = {name:df for name, df in dataframe_dict.items() if name in names}
        if columns:
            filtered_dict = {name:df[columns] for name, df in filtered_dict.items()}
        if index:
            filtered_dict = {name:df[df.index.isin(index)] for name, df in filtered_dict.items()}
        self.display_pipeline(filtered_dict)

