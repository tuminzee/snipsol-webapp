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
demo_file = pd.read_excel('./files/input.xlsx', dtype=str)
# st.dataframe(demo_file)

towrite = io.BytesIO()
downloaded_file = demo_file.to_excel(towrite, encoding='utf-8', index=False, header=True)
towrite.seek(0)  # reset pointer
b64 = base64.b64encode(towrite.read()).decode()  # some strings
linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="demo.xlsx">Download demo file</a>'
st.markdown(linko, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a XLSX file", type="xlsx")
placeholder = st.empty()

# input = placeholder.text_input('text')
# click_clear = st.button('clear text input', key='clear')
# if click_clear:
#     input = placeholder.text_input('text', value='clear')

if uploaded_file:
    idf = pd.read_excel(uploaded_file,  header=0, names=['position', 'value'], dtype=str)
    dbdf = pd.read_excel('./files/db.xlsx',  header=None, dtype=str)



    dbrow, dbcol = dbdf.shape
    # idrow, idcol = idf.shape

    # st.dataframe(df)
    # st.table(df)
    output_dict = {}
    input = placeholder.text_input('Iterating over this')

    for i in range(18, dbcol):
        records = []
        for j in range(2, len(dbdf)):
            temp = {'position': dbdf.iloc[j, 0], 'value': dbdf.iloc[j, i]}
            records.append(temp)
        temp_df = pd.DataFrame.from_records(records)
        # st.dataframe(temp_df)
        df_diff = pd.concat([idf,temp_df]).drop_duplicates(keep=False)
        row, col = df_diff.shape
        idf_row, idf_col = idf.shape
        temp_row, temp_col = temp_df.shape
        input = placeholder.text_input('Iterating over', value=dbdf.iloc[1, i])
        # st.write("checking", dbdf.iloc[1, i])
        output_dict[dbdf.iloc[0,i] + " " +  dbdf.iloc[1, i]] = ((idf_row + temp_row) - row)/2

    # print(output_dict)
    input = placeholder.text_input('Message', value='Render Complete')
    dict_items = output_dict.items()
    sorted_ans = sorted(dict_items, key = lambda kv: kv[1], reverse=True)
    first_five = list(sorted_ans)[:5]
    st.write('Top five matches are')
    st.write(first_five)