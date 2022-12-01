import pandas as pd
import streamlit as st
#import plotly.express as px
from pandas import *
import matplotlib.pyplot as plt


st.set_page_config(page_title="Retail", page_icon=":bar_chart:", layout="wide",initial_sidebar_state= "expanded")

# ---- MAINPAGE ----
st.title(":bar_chart:Supply Chain Dashboard")
st.markdown("##")

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#Read csv
@st.cache
def get_data_from_csv():
    df = pd.read_csv("Retail - Days Of Supply.csv.csv"
    ) 
    return df

df = get_data_from_csv()

# # ---- SIDEBAR ----
st.sidebar.header("Hey! Filter Here:")
Unit_Storage_Cost = st.sidebar.multiselect(
    "Select the Unit Storage Cost",
    options=df["Unit Storage Cost"].unique(),
    default=df["Unit Storage Cost"].unique()
)

# df_selection = df.query(
#     "Unit Storage Cost == @Unit Storage Cost"
# )


# df_selection = df.query(
#     "Unit Storage Cost == @Unit Storage Cost"
# )
# TOP KPI's
Previous_year_Overall_Average_Unit_Storage_Cost = (df["Unit Storage Cost"].mean())
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Previous year Overall AVG Unit Storage Cost")
    st.subheader(f"US $ {Previous_year_Overall_Average_Unit_Storage_Cost}")

Storage_Cost_By_Month= df.groupby(by=["SubDepartment"]).mean()[["Unit Storage Cost"]]
# SubDepartment_unit_Storge_Cost = px.bar(
#     Storage_Cost_By_Month,
#     x= Storage_Cost_By_Month.index,
#     y="Unit Storage Cost",
#     title="<b>Comparison Of Unit Storage Cost By Month</b>",
#     color = 'Unit Storage Cost' ,
#    # color=["#FFFFFF"] * len( Storage_Cost_By_Month),
#     #template="plotly_white"
    
# )
# SubDepartment_unit_Storge_Cost.update_layout(
# xaxis=dict(tickmode="linear"),
# plot_bgcolor="rgba(0,0,0,0)",
# yaxis=(dict(showgrid=False)),
# )

# st.plotly_chart(SubDepartment_unit_Storge_Cost)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
































