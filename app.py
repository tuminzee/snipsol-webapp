import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
st.set_page_config(
    'SNiPSOL',
    page_icon="🔬"
    )

st.title('SNIPSOL')


uploaded_file = st.file_uploader("Choose a XLSX file", type="xlsx")
placeholder = st.empty()

# input = placeholder.text_input('text')
# click_clear = st.button('clear text input', key='clear')
# if click_clear:
#     input = placeholder.text_input('text', value='clear')

if uploaded_file:
    idf = pd.read_excel(uploaded_file,  header=None, names=['position', 'value'], dtype=str)
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
        output_dict[dbdf.iloc[1, i]] = ((idf_row + temp_row) - row)/2

    # print(output_dict)
    input = placeholder.text_input('Message', value='Render Complete')
    dict_items = output_dict.items()
    sorted_ans = sorted(dict_items, key = lambda kv: kv[1], reverse=True)
    first_five = list(sorted_ans)[:5]
    st.write(first_five)