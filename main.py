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

if st.checkbox("Show sample data(random)"):
    st.dataframe(sample_df.sample(10))

left, center, right = st.columns(3)

with left:
    participants_no = sample_df.shape[0]
    st.markdown(f"#### {participants_no} participants")

with center:
    percent_awareness = (
        sample_df.Aware_Coronavirus.value_counts(normalize=True)["Yes"] * 100
    )
    st.markdown(f"#### {percent_awareness: .2f}% Awareness")

with right:
    mean_age = sample_df.Age.mean()
    st.markdown(f"#### {mean_age: .2f} - Mean Age")


st.markdown("---")
st.markdown("### Select region")
region_option = st.selectbox('Select a region',['All']+sample_df.Region.unique().tolist())

filtered_df = sample_df if region_option == "All" else sample_df[sample_df.Region == region_option]


left_1, left_2, right_1, right_2 = st.columns([3, 1, 3, 1])

gender_counts = filtered_df.Gender.value_counts()
gender_percent = filtered_df.Gender.value_counts(normalize=True) * 100 

with left_1:
    st.bar_chart(data=gender_counts)

with left_2:
    if 'Female' in gender_percent.index:
        st.write(f"**{gender_percent['Female']:.2f}% female**")
    if 'Male' in gender_percent.index:
        st.write(f"**{gender_percent['Male']:.2f}% male**")

    
# map plot
regions_count = filtered_df.Region.value_counts().to_dict()
regions_percent = filtered_df.Region.value_counts(normalize=True)*100
regions_loc = {
    "Western": [5.5573, -2.3024],
    "Central": [5.6444, -1.2891],
    "Greater Accra": [5.8143, 0.0747],
    "Ashanti": [6.7470, -1.5209],
    "Eastern": [6.5781, -0.4502],
    "Volta": [6.5781, 0.4502],
    "Ahafo": [6.9168, -2.5351],
    "Brong Ahafo": [7.9559, -1.6761],
    "Northern": [9.66, -0.39437],
    "Western North": [6.3, -2.8],
}


map_data = pd.DataFrame(
    np.concatenate(
        [
            np.random.randn(regions_count[key], 2) / [10, 10] + regions_loc[key]
            for key in regions_count.keys()
        ]
    ),
    columns=["lat", "lon"],
)

with right_1:
    st.map(map_data,height=300)

with right_2:
    # st.table(regions_count)
    if region_option == "All":
        st.write(f"{regions_percent[0] + regions_percent[1]:.2f}% of the respondents came from {regions_percent.index[0]} and {regions_percent.index[1]}.")
    else:
        st.write(f"{regions_count[region_option]} respondents came from {region_option}.")
        


st.markdown("---")
st.markdown("### Info Source vs Trusted Channel")

left, right = st.columns(2)

info_source = load_data("info_source")
trust_channel = load_data("trust_channel")

info_source_counts = info_source.Info_Source.value_counts()[:7].to_dict()
trust_channel_counts = trust_channel.Trust_Channel.value_counts()[:7].to_dict()

info_source_vs_trust = {
    key: [info_source_counts.get(key, 0), trust_channel_counts.get(key, 0)]
    for key in set(info_source_counts) | set(trust_channel_counts)
}
info_source_vs_trust_df = pd.DataFrame(info_source_vs_trust).T
info_source_vs_trust_df.columns=["Info Source", "Trusted Channel"]
info_source_vs_trust_df.sort_values(by="Info Source", inplace=True, ascending=False)
with left:
    st.bar_chart(data = info_source_vs_trust_df, stack=False)
with right:
    st.table(info_source_vs_trust_df)
    
st.markdown("---")
st.markdown("### Discriminated Group")

left, right = st.columns(2)
discriminated_group = load_data("discriminated_group")
discriminated_counts = discriminated_group.Discriminated_Group.value_counts()[:3]

with left:
    st.write(f"Although many groups(especially foreigners) were reported to be discriminated during the pandemic, the most reported were {discriminated_counts.index[0]}, {discriminated_counts.index[1]} and {discriminated_counts.index[2]}")
with right:
    st.bar_chart(data=discriminated_counts)
    




