import base64

import pandas as pd
import streamlit as st
from PIL import Image

#   st.set_page_config(layout="wide")
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
        masterConcat = masterConcat[['Name', 'In-meeting duration', 'Date']].pivot(index = 'Name', columns='Date').reset_index().fillna('Absent')
        st.dataframe(masterConcat)
        st.download_button(label='Download csv',data = masterConcat.to_csv(),mime='text/csv' )  
        AttendanceDf = {}
        
