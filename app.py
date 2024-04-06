import streamlit as st
from pages import data_collection, data_organization
import pandas as pd


st.title('Knowledge Navigator')

def main():
    st.set_page_config(page_title='My App', layout='wide')
    
    # Sidebar navigation
    pages = {
        'Data Collection': data_collection,
        'Data Organization': data_organization,
        # Other pages...
    }
    
    selected_page = st.sidebar.radio('Navigate', list(pages.keys()))
    
    # Load the dataframe from session state
    if 'data' in st.session_state:
        df = st.session_state['data']
    else:
        df = None
    
    # Pass the dataframe to the selected page
    pages[selected_page].main(df)

if __name__ == '__main__':
    main()
    