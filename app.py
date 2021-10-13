import streamlit as st
import base64
import io
import numpy as np
import pandas as pd
import src.assets.calculate as calculate

st.set_page_config(
    'SNiPSoL',
    page_icon="🔬"
    )

st.title('SNiPSoL 🔬')


option = st.sidebar.selectbox(
    'Navigate',
     ['Mutiple Excel Input', 'Manual Input','About'])


st.sidebar.markdown('## Simplified computational program for automated identification of the SNP-Genotypes and drug resistance mutations in genomic datasets of leprosy bacilli')

st.sidebar.markdown('More features coming soon🧬')


if option == 'Mutiple Excel Input':
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
        

elif option == 'Manual Input':
    snp0 = st.text_input('SNP1642875')
    snp1 = st.text_input('SNP2935685')
    snp2 = st.text_input('SNP14676')
    snp_list = list(map(lambda x:x.upper(), [snp0, snp1, snp2])) 
    snptype = None

    if (st.checkbox('Calculate SNP Type')):
        snptype = calculate.snp_type_calculate(snp_list)
        if (snptype == None):
            st.warning("Invalid Input, please check the entered data")
        else:
            st.warning("SNP Type: " + snptype)

        st.subheader("Enter the values for the calulcation of subtypes")
        sub_snp_list = []

        if ( snptype == '1'):
            subsnp0 = st.text_input("SNP84533")
            subsnp1 = st.text_input("SNP313361")
            subsnp2 = st.text_input("SNP61425")
            subsnp3 = st.text_input("SNP1642875", key=0)
            sub_snp_list = list(map(lambda x:x.upper(), [subsnp0, subsnp1, subsnp2, subsnp3])) 
        
        elif( snptype == '2' ):
            subsnp0 = st.text_input("SNP3102778")
            subsnp1 = st.text_input("SNP1104232")
            subsnp2 = st.text_input("SNP2751783")
            subsnp3 = st.text_input("SNP2935685", key=0)
            sub_snp_list = list(map(lambda x:x.upper(), [subsnp0, subsnp1, subsnp2, subsnp3]))


        elif( snptype == '3'):
            subsnp0 = st.text_input("SNP1295192")
            subsnp1 = st.text_input("SNP2312059")
            subsnp2 = st.text_input("SNP413902")
            subsnp3 = st.text_input("SNP20910")
            subsnp4 = st.text_input("SNP14676", key=0)
            sub_snp_list = list(map(lambda x:x.upper(), [subsnp0, subsnp1, subsnp2, subsnp3, subsnp4]))

        elif( snptype == '4' ):
            subsnp0 = st.text_input("INS978586")
            subsnp1 = st.text_input("DELI476522")
            sub_snp_list = list(map(lambda x:x.upper(), [subsnp0, subsnp1]))


        if (st.checkbox('Calculate SNP Sub Type')):
            snp_sub_type = calculate.snp_sub_type_calculate(sub_snp_list)
            if (snp_sub_type == None):
                st.warning("Invalid Input, please check the entered data")
            else:
                st.warning("SNP Sub Type: " + snp_sub_type)




elif option == 'About':
    st.markdown('## **Simplified computational program for automated identification of the SNP-Genotypes and drug resistance mutations in genomic datasets of leprosy bacilli**')

    st.markdown('The emergence of drug resistant strains of Mycobacterium leprae (the causative agent of leprosy) has been reported in recent years. Next generation Sequencing based whole genome analysis of *M. leprae* strains sequencing has also revealed phylogeographic markers in M. leprae strains. The existing SNP-typing scheme makes use of such phylogeographically informative loci (SNPs/Insertions/Deletions etc) for enabling the study of transmission dynamics of the strains. However, correct identification of genotype from these large datasets involving thousands of SNPs is a labour-intensive and error-prone exercise. Therefore we have developed an automated programme to identify the genotype of M. leprae strains ased on user inputs of SNPs identified from the sequencing data excel tables. It also identifies the mutations associated with the drug resistance phenotype. The program can also identify the predominant genotypes by input of just 1-2 SNP loci and hence can be customised based on the geographic location and strain prevalence. The conventional genotyping results are also generated which comprehensively tests for all the informative SNP loci for all the strains. The program takes input of the the nucleotide/s present at key genomic loci and identifies the SNP genotype instantly. The utility of this program lies in its ability to accurately, rapidly and reproducibly identify different strains and their molecular pattern of drug resistance, without the user having to go through the research articles and databases for reliable strain typing schemes and makes the process of choosing appropriate drugs for treatment easier.')


