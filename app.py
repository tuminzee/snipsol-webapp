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
demo_file = pd.read_excel('./files/mutiple sample input.xlsx', dtype=str)
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
    db_df = pd.read_excel('./files/sampledb.xlsx', header=None, dtype=str)

    input_row, input_col = input_df.shape
    db_row, db_col = db_df.shape

    # st.dataframe(input_df)
    # st.dataframe(db_df)
    input = placeholder.text_input('Message', value="Processing this will take some time")
    

    output = pd.DataFrame()
    for input_col_index in range(1, input_col):
        input_records = []
        for input_row_index in range(1, input_row):
            input_temp = {'position': input_df.iloc[input_row_index, 0], 'value': input_df.iloc[input_row_index, input_col_index]}
            input_records.append(input_temp)
            input_temp_df = pd.DataFrame.from_records(input_records)
        # st.dataframe(input_temp_df)
        # st.write("length", len(input_records))
        
        output_dict = {}
        for db_col_index in range(1, db_col):
            db_records = []
            for db_row_index in range(1, db_row):
                db_temp = {'position': db_df.iloc[db_row_index, 0], 'value': db_df.iloc[db_row_index, db_col_index]}
                db_records.append(db_temp)
            db_temp_df = pd.DataFrame.from_records(db_records)
            df_diff = pd.concat([input_temp_df,db_temp_df]).drop_duplicates(keep=False)
            diff_row, diff_col = df_diff.shape
            output_dict[db_df.iloc[0, db_col_index]] = ((input_row-1 + db_row-1) - diff_row)/2
        # st.write(output_dict)
        output_dict[0] =  input_df.iloc[0, input_col_index]
        output = output.append(output_dict, ignore_index=True, sort=True)

    input = placeholder.text_input('Message', value="Completed")
    st.dataframe(output)
    downloaded_file = output.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()  # some strings
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="ans.xlsx">Download ans file</a>'
    st.markdown(linko, unsafe_allow_html=True)
