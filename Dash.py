import pandas as pd
import streamlit as st
import plotly.express as px
from pandas import *
import plotly.graph_objects as go
import altair as alt



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
Overall_Average_Unit_Storage_Cost = (df_selection["Unit Storage Cost"].mean())
Orders_for_next_3days = df_selection[(df_selection['Next Order Flag'] >= 0) & (df_selection['Next Order Flag'] <= 3)].count()["Next Reorder date (in days)"]
Cost_for_next_3days = df_selection[(df_selection['Next Order Flag'] >= 0) & (df_selection['Next Order Flag'] <= 3)].sum()["Unit cost"]
left_column, middle_column, right_column = st.columns(3)


with left_column:   
    st.markdown("<h4 style='text-align: center; color: black;'> Overall AVG Unit Storage Cost</h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: blue;'>"+"$ "+str((float("{:.2f}".format(Overall_Average_Unit_Storage_Cost ))))+"</h4>", unsafe_allow_html=True)  


with middle_column:
    st.markdown("<h4 style='text-align: center; color: black;'>Order For Next 3days </h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: blue;'>"+str(round(Orders_for_next_3days))+"</h4>", unsafe_allow_html=True)  


with right_column:
    st.markdown("<h4 style='text-align: center; color: black;'>Cost For Next 3days </h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: blue;'>"+"$ "+str(round(Cost_for_next_3days  /1000,2))+"K"+"</h4>", unsafe_allow_html=True)  

st.markdown("""---""")

# #CHART_1
Storage_Cost_By_Month= df_selection.groupby(by=["Month"]).mean()[["Unit Storage Cost"]].round(2).reset_index()
fig = px.line(Storage_Cost_By_Month,x = 'Month',y='Unit Storage Cost',text=(Storage_Cost_By_Month['Unit Storage Cost']),
title="<b>Comparison Of Unit Storage Cost By Month</b>"
)
fig.update_layout(xaxis_title="Month",
yaxis_title="AVG Unit Storage Cost",
plot_bgcolor="rgba(0,0,0,0)",
yaxis=(dict(showgrid=False)),
xaxis=(dict(showgrid=False))
)
fig.update_traces(marker_color="#3EC1CD")


st.plotly_chart(fig,use_container_width=True)

#CHART-2
Storage_Cost_By_Month = df_selection.groupby(by=["SubDepartment"]).mean()[["Unit Storage Cost"]].round(2).reset_index()
Storage_Cost_By_Month = Storage_Cost_By_Month.sort_values(by='Unit Storage Cost')

fig1 = px.bar(Storage_Cost_By_Month, x='SubDepartment', y='Unit Storage Cost',orientation='v',title="<b>Comparison Of Unit Storage Cost By Sub-Department</b>"
,text=(Storage_Cost_By_Month['Unit Storage Cost']))
fig1.update_layout(xaxis_title="SubDepartment",
yaxis_title="AVG Unit Storage Cost",
plot_bgcolor="rgba(0,0,0,0)",
yaxis=(dict(showgrid=False)))
#fig1.update_traces(marker_color="#3EC1CD")


st.plotly_chart(fig1,use_container_width=True)

#CHART-3
Storage_Cost_By_Month = df_selection.groupby(by=["Department"]).mean()[["Fulfillment TAT post Order Placement(in days)"]].round(2)
Storage_Cost_By_Month = Storage_Cost_By_Month .sort_values(by="Fulfillment TAT post Order Placement(in days)")

fig_hourly_sales = px.bar(Storage_Cost_By_Month,
    x="Fulfillment TAT post Order Placement(in days)",
    y=Storage_Cost_By_Month.index,
    orientation="h",
    title="<b>Department Wise AVG Fulfillment TAT post Order Placement</b>",
    text=(Storage_Cost_By_Month['Fulfillment TAT post Order Placement(in days)']),
    color_discrete_sequence=["#0083B8"] * len(Storage_Cost_By_Month),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# Storage_Cost_By_Month = df_selection.groupby(by=["Department"]).mean()[["Fulfillment TAT post Order Placement(in days)"]].reset_index()#.sort_values(by="Fulfillment TAT post Order Placement(in days)")

# labels = Storage_Cost_By_Month['Department']
# values = Storage_Cost_By_Month['Fulfillment TAT post Order Placement(in days)']

# colours = ["#0C3B5D", "#3EC1CD"]

# fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
# fig.update_traces(marker=dict(colors=colours),
# legendgrouptitle_text="Gender")
# fig.update_layout(height=500, width=600)


#CHART-4
Storage_Cost_By_Month = (
    df_selection.groupby(by=["Department"]).mean()[["Unit Storage Cost","Target Unit Storage cost"]].round(2)
)
fig_product_sales = px.bar(
    Storage_Cost_By_Month,
    x="Unit Storage Cost",
    y=Storage_Cost_By_Month.index,
    orientation="h",
    title="<b>Comparison Of Unit Storage Cost By Department</b>",
    text=(Storage_Cost_By_Month["Unit Storage Cost"]),
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
Storage_Cost_By_Month= df_selection.groupby(by=["SubDepartment"]).mean()[["Fulfillment TAT post Order Placement(in days)"]].sort_values("Fulfillment TAT post Order Placement(in days)").round(2)
SubDepartment_unit_Storge_Cost = px.bar(Storage_Cost_By_Month,
    x= Storage_Cost_By_Month.index,
    y="Fulfillment TAT post Order Placement(in days)",
    title="<b> Sub-Department WiseFulfillment TAT post Order Placement</b>",
    text = 'Fulfillment TAT post Order Placement(in days)',
)
SubDepartment_unit_Storge_Cost.update_layout(
xaxis=dict(tickmode="linear"),
plot_bgcolor="rgba(0,0,0,0)",
yaxis=(dict(showgrid=False)),
)

st.plotly_chart(SubDepartment_unit_Storge_Cost,use_container_width=True)


st.title("Orders to be placed and it's cost for placing order")
# # TOP KPI's

Orders_for_next_5days = df_selection[(df_selection['Next Order Flag'] <=5 ) & (df_selection['Next Order Flag'] >= 0)].count()["Next Reorder date (in days)"]
Orders_for_next_7days = df_selection[(df_selection['Next Order Flag'] <=7 ) & (df_selection['Next Order Flag'] >= 0)].count()["Next Reorder date (in days)"]
Orders_for_next_15days = df_selection[(df_selection['Next Order Flag'] <=15 ) & (df_selection['Next Order Flag'] >= 0)].count()["Next Reorder date (in days)"]
left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.markdown("<h4 style='text-align: center; color: black;'>Order For Next 5days </h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: blue;'>"+str(round(Orders_for_next_5days))+"</h4>", unsafe_allow_html=True)  

with middle_column:
    st.markdown("<h4 style='text-align: center; color: black;'>Order For Next 5days </h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: blue;'>"+str(round(Orders_for_next_7days ))+"</h4>", unsafe_allow_html=True)  

with right_column:
    st.markdown("<h4 style='text-align: center; color: black;'>Order For Next 5days </h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: blue;'>"+str(round(Orders_for_next_15days))+"</h4>", unsafe_allow_html=True)  

cost_for_next_5days = df_selection[(df_selection['Next Order Flag'] >= 0) & (df['Next Order Flag'] <= 5)].sum()["Unit cost"]
cost_for_next_7days = df_selection[(df_selection['Next Order Flag'] >=0 ) & (df_selection['Next Order Flag'] <=7 )].sum()["Unit cost"]
cost_for_next_15days = df_selection[(df_selection['Next Order Flag'] >=0 ) & (df_selection['Next Order Flag'] <=15 )].sum()["Unit cost"]
left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.markdown("<h4 style='text-align: center; color: black;'>Cost For Next 5days </h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: blue;'>"+"$ "+str(round(cost_for_next_5days /1000,2))+"K"+"</h4>", unsafe_allow_html=True)  

with middle_column:
    st.markdown("<h4 style='text-align: center; color: black;'>Cost For Next 7days </h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: blue;'>"+"$ "+str(round(cost_for_next_7days /1000,2))+"K"+"</h4>", unsafe_allow_html=True)
   
with right_column:
    st.markdown("<h4 style='text-align: center; color: black;'>Cost For Next 15days </h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: blue;'>"+"$ "+str(round(cost_for_next_15days /1000,2))+"K"+"</h4>", unsafe_allow_html=True)
   

st.title("Amount to be returned within payment terms")

return_amount_within_90days = df_selection[(df_selection['Payment terms (in Days)'] <= 90) & (df_selection['Payment terms (in Days)'] >=0) & (df_selection['Next Order Flag'] <=15) & (df_selection['Next Order Flag'] >=0)].sum()["Amount for Placing order"]
return_amount_within_60days = df_selection[(df_selection['Payment terms (in Days)'] <= 60) & (df_selection['Payment terms (in Days)'] >=0) & (df_selection['Next Order Flag'] <=15) & (df_selection['Next Order Flag'] >=0)].sum()["Amount for Placing order"]
return_amount_within_45days = df_selection[(df_selection['Payment terms (in Days)'] <= 45) & (df_selection['Payment terms (in Days)'] >=0) & (df_selection['Next Order Flag'] <=15) & (df_selection['Next Order Flag'] >=0)].sum()["Amount for Placing order"]  

left_column,middle_column,right_column = st.columns(3)
with left_column:
    st.markdown("<h4 style='text-align: center; color: black;'>Amount to be returned within 90days </h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: blue;'>"+"$ "+str(round(return_amount_within_90days /1000000,2))+"M"+"</h4>", unsafe_allow_html=True)

with middle_column:
    st.markdown("<h4 style='text-align: center; color: black;'>Amount to be returned within 60days </h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: blue;'>"+"$ "+str(round(return_amount_within_60days /1000,2))+"K"+"</h4>", unsafe_allow_html=True)

with right_column:
    st.markdown("<h4 style='text-align: center; color: black;'>Amount to be returned within 45days </h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: blue;'>"+"$ "+str(round(return_amount_within_45days /1000,2))+"K"+"</h4>", unsafe_allow_html=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
