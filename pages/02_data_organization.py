# 02_data_organization.py
import streamlit as st
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import CharacterTextSplitter

def process_data(df):
    if df is not None:
        # Load documents from the dataframe using Langchain
        loader = DataFrameLoader(df, page_content_column='text')
        documents = loader.load()
        
        # Split documents using Langchain
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        
        # Display the processed data
        st.write(texts)
    else:
        st.warning('No data available. Please collect data first.')

    if st.button('Proceed to Model Selection'):
        st.switch_page('pages/03_model_selection.py')

def main(df):
    st.title('Data Organization')
    process_data(df)