import streamlit as st
import plotly_express as px1
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
st.set_page_config(page_title="SNCU Dashboard", page_icon=":bar_chart:",layout="wide")
st.title (":bar_chart: FBNC Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
fl = st.file_uploader(":file_folder:, Upload your Data File Contained SNCU Online Data", type=(["xls","xlsx"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(filename)
else:
     st.write("Please upload an Excel file.")

col1, col2 = st.columns((2))
df["admision_date"] = pd.to_datetime(df["admision_date"])

startDate = pd.to_datetime(df["admision_date"]).min()
endDate = pd.to_datetime(df["admision_date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["admision_date"]>= date1) & (df["admision_date"]<= date2)].copy()

st.sidebar.header("Choose Your Filters:")
# SNCU Name
sncu = st.sidebar.multiselect("Select SNCU",df["sncu_name"].unique())
if not sncu:
    df2 = df.copy()
else:
    df2 = df[df["sncu_name"].isin(sncu)]

# type_of_admission
type_of_admission = st.sidebar.multiselect("Type of Admission",df2["type_of_admission"].unique())
if not type_of_admission:
    df3 = df2.copy()
else:
    df3 = df2[df2["type_of_admission"].isin(type_of_admission)]
gender_df = df3.groupby(by=["baby_sex"], as_index=False)["baby_sex"].count()
counts = df3['baby_sex'].value_counts()
counts1 = df3['type_of_admission'].value_counts()

with col1:
    st.subheader("Gender Wise Admission")
    fig = px.pie(values=counts, names=counts.index, hole=0.5)
   # fig.update_traces(text=df3["baby_sex"], textposion="outside")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Type of Admission")
    fig = px.pie(values=counts1, names=counts1.index, hole=0.5)
    # fig.update_traces(text=df3["baby_sex"], textposion="outside")
    st.plotly_chart(fig, use_container_width=True)

