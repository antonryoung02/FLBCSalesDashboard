from app.transformation_pipelines.standardize import StandardizePipeline 
from app.transformation_pipelines.time_series import TimeSeriesPipeline
from app.transformation_pipelines.time_series_cumulative import TimeSeriesCumulativePipeline
import streamlit as st
from display_pipelines.display_menu_engineering import display_menu_engineering
from display_pipelines.display_cumulative import CumulativeStatisticsDisplayPipeline
from display_pipelines.display_time_series import SalesHistoryDisplayPipeline
from display_pipelines.display_trends import DisplayTrendsPipeline
from app.dataframe_operations import remove_invalid_columns, remove_invalid_rows
from app.utils import extract_dataframe_dict_from_excel, initialize_streamlit_styling, display_data_with_pipeline, read_categories_dataframe
from app.categories_dataframe import CategoriesDataframe
from app.filters import BaseFilter
from app.config import BASE_DIR_PATH, DATA_FILENAME
def main():
    initialize_streamlit_styling()
    try:
        dataframe_dict = extract_dataframe_dict_from_excel()
    except FileNotFoundError:
        st.error(f"The excel file was not found. The file is either open, has been renamed from {DATA_FILENAME}, or has been moved from its initial location ({BASE_DIR_PATH}). Fix the issue and rerun the program.")
        return
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return

    categories_dataframe = CategoriesDataframe(read_categories_dataframe())

    for df in dataframe_dict.values():
        remove_invalid_rows(df)
        remove_invalid_columns(df)

    sp = StandardizePipeline()
    sp.transform(dataframe_dict, inplace=True)

    features_to_ignore = ['*categories']
    tsp = TimeSeriesPipeline(features_to_ignore)
    per_product_time_dataframe_dict = tsp.transform(dataframe_dict)

    mean_features = ['*menu Price $', 'FC%', '*cm category', '*CM $', '*FC $']
    features_to_ignore = ['*categories']
    tscp = TimeSeriesCumulativePipeline(categories_dataframe, mean_features, features_to_ignore)
    per_group_time_dataframe_dict = tscp.transform(per_product_time_dataframe_dict)

    visualization_options = {"Per-Product Data": per_product_time_dataframe_dict, "Per-Group Data":per_group_time_dataframe_dict}
    selected_visualization = st.radio(
        "Select Data Type",
        list(visualization_options.keys()),
        index=list(visualization_options.keys()).index(st.session_state.get("selected_visualization", "Per-Product Data")),
        horizontal=True
    )

    selected_dataframe_dict = visualization_options[selected_visualization]

    filter = BaseFilter(categories_dataframe)
    shdp = SalesHistoryDisplayPipeline()
    display_data_with_pipeline(selected_dataframe_dict, selected_visualization, shdp, "Time Series", filter)
    dtp = DisplayTrendsPipeline()
    display_data_with_pipeline(selected_dataframe_dict, selected_visualization, dtp, "Trends", filter)
    csdp = CumulativeStatisticsDisplayPipeline()
    display_data_with_pipeline(selected_dataframe_dict, selected_visualization, csdp, "Cumulative", filter)

    st.divider()

    display_menu_engineering(dataframe_dict, categories_dataframe)

if __name__ == "__main__":
    main()