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



st.title(' # Attendance Report App')
st.markdown("""
This app retrieves the ** Automated attendence information** where the attendance  list gets updated whenever a file uploaded 
""")
st.subheader("Upload Dataset")
data_file = st.file_uploader("Upload Dataset",type=["csv","xlsx","xls"])
if data_file is not None:
    st.success('File Uploaded Successfully!')
    if st.button("Process"):
        # Connecting to the sqlite3 database
        conn = sqlite3.connect('users.db')

        # Creating a cursor object to execute
        # SQL queries on a database table
        cursor = conn.cursor()
        
        # Table Definition
        #cursor.execute("""CREATE TABLE IF NOT EXISTS person2
                # (Date TEXT,Name TEXT,In_metting_duration TEXT)""")
        st.write(type(data_file))
        file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
        st.write(file_details)
        AttendanceDf = {} 
        data_file = pd.read_csv(data_file,sep='\t',  on_bad_lines='skip',header = 8,index_col = False)
        #date = list(data_file.reset_index()[data_file.reset_index()['index'] == 'Start time'])[0].split(',')[0]
        date = data_file['First join'].iloc[0].split(',')[0]
        df1 = data_file.iloc[0:list(data_file[data_file['Name'] == '3. In-Meeting activities'].index)[0], :]
        df1.sort_values(by=['Name'],ascending=False).reset_index(drop = True,inplace=True)
        AttendanceDf[date] = df1
        AttendanceDf.keys()
        masterConcat = pd.DataFrame()
        for date, df1 in AttendanceDf.items():
            tempDf = df1
            tempDf['Date'] = date
            masterConcat = pd.concat([masterConcat, tempDf])
        masterConcat = masterConcat[['Date','Name', 'In-meeting duration']].pivot(index = 'Name', columns='Date').reset_index().fillna('Absent')
        st.dataframe(masterConcat)
        data = masterConcat.to_csv('data.csv')
        file = open('data.csv')

        contents = csv.reader(file)

        insert_records = '''INSERT INTO person2 (Date,Name,In_metting_duration) VALUES(?,?,?)'''#,(masterConcat)) 
        cursor.executemany(insert_records,contents)

        select_all = "SELECT * FROM person2"     
        rows = cursor.execute(select_all).fetchall()

        # Output to the console screen
        for column in rows:
            print(column)
            print (type(column))
            cursor.execute(
            f"""ALTER TABLE linksauthor 
            ADD COLUMN {column} 'float'
            """)

 
        # Committing the changes
        conn.commit()
 
        # closing the database connection
        conn.close()
        

        #masterConcat .to_sql('person1', conn, if_exists='append', index = False)
        #rows = cursor.execute(masterConcat).fetchall()
        

       # cursor.execute('''SELECT * FROM person1''').fetchall()
       # cursor.execute('''SELECT * FROM person1 u LEFT JOIN person1 o ON u.name = o.name''')
       # cursor.fetchall()
        #pd.read_sql('''SELECT * FROM person1 u LEFT JOIN person1 o ON u.name= o.name''', conn)
       # cursor.executemany('''INSERT INTO person1 (Name ,In_metting_duration ) VALUES(?,?)''',(masterConcat)) 
        #select_all= "SELECT * FROM person1"
       # for r in masterConcat:
           # print(r)
        #rows = cursor.execute(select_all).fetchall()
        # Output to the console screen
        #for row in  masterConcat
           # masterConcat['Name'].iloc[0]
           # print(row)
        
 
       # conn.commit()
      #  print('complete')
        #conn.close()
       
       # st.download_button(label='Download csv',data = masterConcat.to_csv(),mime='text/csv' ) 
################################################CONNECTING WITH DATABASE################################################################


