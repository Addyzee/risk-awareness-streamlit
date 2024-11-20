import pandas as pd
import streamlit as st
import os
import numpy as np

DATA_REPO = "data"


@st.cache_data
def get_data(data_repo=DATA_REPO):
    files = os.listdir(os.path.dirname(__file__) + "/" + data_repo)
    file_names = [file.lower().replace(".csv", "") for file in files]
    files_dict = {file_names[i]: f"data/{files[i]}" for i in range(len(files))}
    return files_dict


@st.cache_data
def load_data(name):
    files = get_data()
    data_file = files[name]
    df = pd.read_csv(data_file)
    return df


st.set_page_config(layout="wide")
st.markdown("# Risk awareness")
st.markdown("### Individual Information")

sample_df = load_data("individual_info")

if st.checkbox("Show sample data"):
    st.table(sample_df[:8])

left, center, right = st.columns(3)
