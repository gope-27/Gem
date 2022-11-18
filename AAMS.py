# Import required modules
import base64
import csv
import os
import sqlite3


import pandas as pd
import streamlit as st
from PIL import Image

#For image 
st.set_page_config(layout="wide")
image = Image.open('GWC.png')
st.image(image,width = 230) 

#Title
st.title(' # Automatic Attendance Management System')
#Description
st.markdown("""
This app retrieves the ** Automated attendence information** where the attendance  list gets updated whenever a file uploaded 
""")
#Sub-title
st.subheader("Upload Dataset")
data_file = st.file_uploader("Upload Dataset",type=["csv","xlsx","xls"])
if data_file is not None:
    st.success('File Uploaded Successfully!')
    if st.button("Process"):
        st.write(type(data_file))

        #Shows file details
        file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
        st.write(file_details)

        #Cleaning data 
        data_file = pd.read_csv(data_file,sep='\t',  on_bad_lines='skip',header = 8,index_col = False)
        date = data_file['First join'].iloc[0].split(',')[0]
        df1 = data_file.iloc[0:list(data_file[data_file['Name'] == '3. In-Meeting activities'].index)[0], :]

        #Sorting by Name
        df1 = df1.sort_values(by=['Name'],ascending=True).reset_index(drop = True)

        #Removing Unwanted Columns
        df1 = df1.drop(['First join','Email','Participant ID (UPN)','Role'],axis = 1)
        df1[['Last leave','Time']] = df1['Last leave'].str.split(',',expand=True)
        df1   = df1.drop(['Time'],axis = 1)
        Cleaned_data = df1.pivot(index='Name', columns='Last leave', values='In-meeting duration').reset_index()
        try:
            #Connection with DB
            conn  = sqlite3.connect('Python for Data Analytics.db')
            
            #Reading data from DB
            Reading_DB = pd.read_sql_query("select * from Python_Table",conn)

            #Mergeing Database and Uploading file
            Merged_Data = pd.merge(Cleaned_data, Reading_DB , how='outer', on=['Name', 'Name']).fillna('Absent')

            #Remove duplicate columns
            Duplicated_Columns = Merged_Data.loc[:,~Merged_Data.T.duplicated(keep='first')]

            #Highlighter            
            def highlighter(cell_value):
  
                if cell_value in ['Absent']:
                    color = 'red'
                else:
                    color = 'black'
                return 'color: %s' % color
 
            Final_output= Duplicated_Columns.style.applymap(highlighter)
            Final_output

            data4 = Cleaned_data.to_sql('Python_Table',con = conn,index = False,if_exists = 'replace')
        except:

            # Creating table to DB
            data1 = Cleaned_data.to_sql('Python_Table',con = conn,index = False,if_exists = 'replace')
