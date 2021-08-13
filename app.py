import streamlit as st
import base64
import io
import numpy as np
import pandas as pd
st.set_page_config(
    'SNiPSoL',
    page_icon="🔬"
    )

st.title('SNiPSoL 🔬')

# st.header('Input file configuration')
demo_file = pd.read_excel('./files/mutipleinput.xlsx', dtype=str)
# st.dataframe(demo_file)
db_df = pd.read_excel('./files/db.xlsx', header=None, dtype=str)

towrite = io.BytesIO()
downloaded_file = demo_file.to_excel(towrite, encoding='utf-8', index=False, header=True)
towrite.seek(0)  # reset pointer
b64 = base64.b64encode(towrite.read()).decode()  # some strings
linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="demo.xlsx">Download demo file</a>'
st.markdown(linko, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a XLSX file", type="xlsx")
placeholder = st.empty()

if uploaded_file:
    input = placeholder.text_input('Message', value="Processing, this will take some time")
    input_df = pd.read_excel(uploaded_file, header=None, dtype=str)
    # db_df = pd.read_excel('./files/db.xlsx', header=None, dtype=str)

    INPUT_ROW_LENGTH, INPUT_COL_LENGTH = input_df.shape
    DB_ROW_LENGTH, DB_COL_LENGTH = db_df.shape
    INPUT_ROW_START_INDEX = 1
    INPUT_COL_START_INDEX = 1
    DB_ROW_START_INDEX = 2
    DB_COL_START_INDEX = 18
    INPUT_HEADER_ROW_INDEX = 0
    DB_HEADER_ROW_INDEX = 1
    INPUT_POSTION_ROW_INDEX = 0


    # st.dataframe(input_df)
    # st.dataframe(db_df)
    
    output = pd.DataFrame()
    input_headers = []
    for input_col_index in range(INPUT_COL_START_INDEX, INPUT_COL_LENGTH):
        input_headers.append(input_df.iloc[INPUT_HEADER_ROW_INDEX, input_col_index])
        temp_input_df = input_df.iloc[1:, [0,input_col_index]]
        temp_input_df.dropna(inplace=True)
        temp_input_df.columns = ["position", "value"]
        temp_input_df['position'] = temp_input_df['position'].astype(float)
        temp_input_df['position'] = temp_input_df['position'].astype('int64')
        st.dataframe(temp_input_df.head())
        output_dict = {}
        for db_col_index in range(DB_COL_START_INDEX, DB_COL_LENGTH):
            temp_db_df = db_df.iloc[2: , [0, db_col_index]]
            
            temp_db_df.dropna(inplace=True)
            temp_db_df.columns = ["position", "value"]
            temp_db_df['position'] = temp_db_df['position'].astype(float)
            temp_db_df['position'] = temp_db_df['position'].astype('int64')

            # st.dataframe(temp_db_df)  

            ans = temp_input_df.append(temp_db_df, ignore_index=True)
            output_dict[db_df.iloc[DB_HEADER_ROW_INDEX-1, db_col_index] + " " + db_df.iloc[DB_HEADER_ROW_INDEX, db_col_index]] = int(len(ans)-len(ans.drop_duplicates()))

        output = output.append(output_dict, ignore_index=True)
    
    input = placeholder.text_input('Message', value="Completed")
    st.write(input_headers)
    
    output.insert(loc=0, column='Input Variable', value=input_headers)
    st.dataframe(output)


    downloaded_file = output.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()  # some strings
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="ans.xlsx">Download Output file</a>'
    st.markdown(linko, unsafe_allow_html=True)
    
