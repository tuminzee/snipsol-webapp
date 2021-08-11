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

towrite = io.BytesIO()
downloaded_file = demo_file.to_excel(towrite, encoding='utf-8', index=False, header=True)
towrite.seek(0)  # reset pointer
b64 = base64.b64encode(towrite.read()).decode()  # some strings
linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="demo.xlsx">Download demo file</a>'
st.markdown(linko, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a XLSX file", type="xlsx")
placeholder = st.empty()

if uploaded_file:
    input_df = pd.read_excel(uploaded_file, header=None, dtype=str)
    db_df = pd.read_excel('./files/db.xlsx', header=None, dtype=str)

    INPUT_ROW_LENGTH, INPUT_COL_LENGTH = input_df.shape
    DB_ROW_LENGTH, DB_COL_LENGTH = db_df.shape
    INPUT_ROW_START_INDEX = 1
    INPUT_COL_START_INDEX = 1
    DB_ROW_START_INDEX = 2
    DB_COL_START_INDEX = 18
    INPUT_HEADER_COL_INDEX = 1
    INPUT_HEADER_ROW_INDEX = 0
    DB_HEADER_COL_INDEX = 18
    DB_HEADER_ROW_INDEX = 1
    INPUT_POSTION_ROW_INDEX = 0
    INPUT_POSTION_COL_INDEX = 0
    DB_POSITION_ROW_INDEX = 0
    DB_POSITION_COL_INDEX = 0

    # st.dataframe(input_df)
    # st.dataframe(db_df)
    input = placeholder.text_input('Message', value="Processing, this will take some time")
    
    output = pd.DataFrame()
    for input_col_index in range(INPUT_COL_START_INDEX, INPUT_COL_LENGTH):
        input_records = []
        for input_row_index in range( INPUT_ROW_START_INDEX , INPUT_ROW_LENGTH):
            input_temp = {'position': input_df.iloc[input_row_index, INPUT_POSTION_COL_INDEX], 'value': input_df.iloc[input_row_index, input_col_index]}
            input_records.append(input_temp)
            input_temp_df = pd.DataFrame.from_records(input_records)
        st.dataframe(input_temp_df.head())
        st.write("length of input", input_df.iloc[INPUT_HEADER_ROW_INDEX, input_col_index]  , len(input_records))
        
        output_dict = {}
        for db_col_index in range(DB_COL_START_INDEX, DB_COL_LENGTH):
            db_records = []
            for db_row_index in range(DB_ROW_START_INDEX, DB_ROW_LENGTH):
                db_temp = {'position': db_df.iloc[db_row_index, DB_POSITION_COL_INDEX], 'value': db_df.iloc[db_row_index, db_col_index]}
                db_records.append(db_temp)
            db_temp_df = pd.DataFrame.from_records(db_records)
            df_diff = pd.concat([input_temp_df,db_temp_df]).drop_duplicates(keep=False)
            diff_row, diff_col = df_diff.shape
            output_dict[db_df.iloc[DB_HEADER_ROW_INDEX, db_col_index]] = ((INPUT_ROW_LENGTH-INPUT_ROW_START_INDEX + DB_ROW_LENGTH-DB_ROW_START_INDEX) - diff_row)/2
        # st.(output_dict)
        output_dict[0] =  input_df.iloc[INPUT_HEADER_ROW_INDEX, input_col_index]
        output = output.append(output_dict, ignore_index=True, sort=True)
    input = placeholder.text_input('Message', value="Completed")
    st.dataframe(output)
    downloaded_file = output.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()  # some strings
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="ans.xlsx">Download Output file</a>'
    st.markdown(linko, unsafe_allow_html=True)
    
