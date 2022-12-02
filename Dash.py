import pandas as pd
import streamlit as st
import plotly.express as px
from pandas import *
import matplotlib.pyplot as plt
import altair as alt
import plost


st.set_page_config(page_title="Retail", page_icon=":bar_chart:", layout="wide",initial_sidebar_state= "expanded")


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#Read csv
@st.cache
def get_data_from_csv():
    df = pd.read_csv("Retail - Days Of Supply.csv.csv"
    ) 
    return df

df = get_data_from_csv()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
Dep = st.sidebar.multiselect(
    "Select the Department:",
    options=df["Department"].unique(),
    default=df["Department"].unique(),
)

SubDep = st.sidebar.multiselect(
    "Select the SubDepartment:",
    options=df["SubDepartment"].unique(),
    default=df["SubDepartment"].unique()
)


Mon= st.sidebar.multiselect(
    "Select the Month:",
    options=df["Month"].unique(),
    default=df["Month"].unique()
)


df_selection = df.query(
    "Department == @Dep & SubDepartment ==@SubDep & Month == @Mon"
)

# ---- MAINPAGE ----
st.title(":bar_chart:Supply Chain Dashboard")
st.markdown("##")


# TOP KPI's
Previous_year_Overall_Average_Unit_Storage_Cost = (df_selection["Unit Storage Cost"].mean())
Orders_for_next_3days = df_selection[(df_selection['Next Order Flag'] >= 0) & (df_selection['Next Order Flag'] <= 3)].count()["Next Reorder date (in days)"]
Cost_for_next_3days = df_selection[(df_selection['Next Order Flag'] >= 0) & (df_selection['Next Order Flag'] <= 3)].sum()["Unit cost"]
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Previous year Overall AVG Unit Storage Cost")
    st.subheader(f" $ {Previous_year_Overall_Average_Unit_Storage_Cost}")

with middle_column:
    st.subheader("Orders for next 3days ")
    st.subheader(f"{Orders_for_next_3days}")

with right_column:
    st.subheader("Cost for next 3days ")
    st.subheader(f"{Cost_for_next_3days}")


st.markdown("""---""")

# #CHART_1
Storage_Cost_By_Month= df_selection.groupby(by=["Month"]).mean()[["Unit Storage Cost"]].reset_index()
fig = px.line(Storage_Cost_By_Month,x = 'Month',y='Unit Storage Cost',
title="<b>Comparison Of AVG Unit Storage Cost By Sub-Department</b>"
)

st.plotly_chart(fig)

#CHART-2
Storage_Cost_By_Month= df_selection.groupby(by=["SubDepartment"]).mean()[["Unit Storage Cost"]]
SubDepartment_unit_Storge_Cost = px.bar(Storage_Cost_By_Month,
    x= Storage_Cost_By_Month.index,
    y="Unit Storage Cost",
    title="<b> Comparison Of AVG Unit Storage Cost By Month</b>",
    template="plotly_white"
)
SubDepartment_unit_Storge_Cost.update_layout(
xaxis=dict(tickmode="linear"),
plot_bgcolor="rgba(0,0,0,0)",
yaxis=(dict(showgrid=False)),
)

st.plotly_chart(SubDepartment_unit_Storge_Cost)


#CHART-3
Storage_Cost_By_Month = (
    df_selection.groupby(by=["Department"]).mean()[["Fulfillment TAT post Order Placement(in days)"]].sort_values(by="Fulfillment TAT post Order Placement(in days)")
)
fig_hourly_sales = px.bar(
    Storage_Cost_By_Month,
    x="Fulfillment TAT post Order Placement(in days)",
    y=Storage_Cost_By_Month.index,
    orientation="h",
    title="<b>Department Wise AVG Fulfillment TAT post Order Placement</b>",
    color_discrete_sequence=["#0083B8"] * len(Storage_Cost_By_Month),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#CHART-4
Storage_Cost_By_Month = (
    df_selection.groupby(by=["Department"]).mean()[["Unit Storage Cost","Target Unit Storage cost"]]#.sort_values(by="Fulfillment TAT post Order Placement(in days)")
)
fig_product_sales = px.bar(
    Storage_Cost_By_Month,
    x="Unit Storage Cost",
    y=Storage_Cost_By_Month.index,
    orientation="h",
    title="<b>Comparison Of Unit Storage Cost By Department</b>",
    color_discrete_sequence=["#0083B8"] * len(Storage_Cost_By_Month),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

#CHART-5
Storage_Cost_By_Month= df_selection.groupby(by=["SubDepartment"]).mean()[["Fulfillment TAT post Order Placement(in days)"]]
SubDepartment_unit_Storge_Cost = px.bar(Storage_Cost_By_Month,
    x= Storage_Cost_By_Month.index,
    y="Fulfillment TAT post Order Placement(in days)",
    title="<b> Sub-Department WiseFulfillment TAT post Order Placement</b>",
    template="plotly_white"
)
SubDepartment_unit_Storge_Cost.update_layout(
xaxis=dict(tickmode="linear"),
plot_bgcolor="rgba(0,0,0,0)",
yaxis=(dict(showgrid=False)),
)

st.plotly_chart(SubDepartment_unit_Storge_Cost)


# #CHART-4
# Storage_Cost_By_Month= df_selection.groupby(by=["SubDepartment"]).mean()[["Days Of Supply"]].reset_index()
# SubDepartment_unit_Storge_Cost = px.bar(
#     Storage_Cost_By_Month,
#     x= Storage_Cost_By_Month.index,
#     y="SubDepartment",
#     title="<b>Comparison Of Unit Storage Cost By Month</b>",
#     color=["#FFFFFF"] * len( Storage_Cost_By_Month),
#     template="plotly_white"
    
# )
# SubDepartment_unit_Storge_Cost.update_layout(
# xaxis=dict(tickmode="linear"),
# plot_bgcolor="rgba(0,0,0,0)",
# yaxis=(dict(showgrid=False)),
# )

# st.plotly_chart(SubDepartment_unit_Storge_Cost)

# #CHART-6
# Storage_Cost_By_Month= df_selection.groupby(by=["Department"]).mean()[["Unit Storage Cost"]]
# SubDepartment_unit_Storge_Cost = px.bar(
#     Storage_Cost_By_Month,
#     x= Storage_Cost_By_Month.index,
#     y="Unit Storage Cost",
#     title="<b>Comparison Of Unit Storage Cost By Month</b>",
#     color=["#FFFFFF"] * len( Storage_Cost_By_Month),
#     template="plotly_white"
    
# )
# SubDepartment_unit_Storge_Cost.update_layout(
# xaxis=dict(tickmode="linear"),
# plot_bgcolor="rgba(0,0,0,0)",
# yaxis=(dict(showgrid=False)),
# )

# st.plotly_chart(SubDepartment_unit_Storge_Cost)


# st.plotly_chart(SubDepartment_unit_Storge_Cost)

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("Orders to be placed and it's cost for placing order")
# # TOP KPI's

Orders_for_next_5days = df_selection[(df_selection['Next Order Flag'] <=5 ) & (df_selection['Next Order Flag'] >= 0)].count()["Next Reorder date (in days)"]
Orders_for_next_7days = df_selection[(df_selection['Next Order Flag'] <=7 ) & (df_selection['Next Order Flag'] >= 0)].count()["Next Reorder date (in days)"]
Orders_for_next_15days = df_selection[(df_selection['Next Order Flag'] <=15 ) & (df_selection['Next Order Flag'] >= 0)].count()["Next Reorder date (in days)"]
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Orders For Next 5 Days")
    st.subheader(f"{Orders_for_next_5days}")

with middle_column:
    st.subheader("Orders For Next 7 Days")
    st.subheader(f"{Orders_for_next_7days}")

with right_column:
    st.subheader("Orders For Next 15 Days")
    st.subheader(f"{Orders_for_next_15days}")

cost_for_next_5days = df_selection[(df_selection['Next Order Flag'] >= 0) & (df['Next Order Flag'] <= 5)].sum()["Unit cost"]
cost_for_next_7days = df_selection[(df_selection['Next Order Flag'] >=0 ) & (df_selection['Next Order Flag'] <=7 )].sum()["Unit cost"]
cost_for_next_15days = df_selection[(df_selection['Next Order Flag'] >=0 ) & (df_selection['Next Order Flag'] <=15 )].sum()["Unit cost"]
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Cost For Next 5days")
    st.subheader(f"{cost_for_next_5days}")

with middle_column:
    st.subheader("Cost For Next 7days")
    st.subheader(f"{cost_for_next_7days}")

with right_column:
    st.subheader("Cost For Next 15days")
    st.subheader(f"{cost_for_next_15days}")

st.title("Amount to be returned within payment terms")

return_amount_within_90days = df_selection[(df_selection['Payment terms (in Days)'] <= 90) & (df_selection['Payment terms (in Days)'] >=0) & (df_selection['Next Order Flag'] <=15) & (df_selection['Next Order Flag'] >=0)].sum()["Amount for Placing order"]
return_amount_within_60days = df_selection[(df_selection['Payment terms (in Days)'] <= 60) & (df_selection['Payment terms (in Days)'] >=0) & (df_selection['Next Order Flag'] <=15) & (df_selection['Next Order Flag'] >=0)].sum()["Amount for Placing order"]

left_column,right_column = st.columns(2)
with left_column:
    st.subheader("Amount to be returned within 90days")
    st.subheader(f"{return_amount_within_90days}")

with right_column:
    st.subheader("Amount to be returned within 60days")
    st.subheader(f"{return_amount_within_60days}")

return_amount_within_45days = df_selection[(df_selection['Payment terms (in Days)'] <= 45) & (df_selection['Payment terms (in Days)'] >=0) & (df_selection['Next Order Flag'] <=15) & (df_selection['Next Order Flag'] >=0)].sum()["Amount for Placing order"]

st.subheader("Amount to be returned within 45days")
st.subheader(f"{return_amount_within_45days}")

# st.markdown("""---""")
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)





























