import streamlit as st
import os
from menu import menu

st.set_page_config(page_title='Knowledge Navigator', layout='wide')

def main():
    st.title('Knowledge Navigator')

    # Button to go back to Data Collection Page
    if st.button('Go to Data Collection'):
        st.switch_page('pages/01_data_collection.py')

    # Button to navigate to Data Organization Page and pass data
    if st.button('Go to Data Organization with Data'):
        # Navigating to Data Organization Page
        st.switch_page('pages/02_data_organization.py')

    if st.button('Proceed to Model Selection'):
        st.switch_page('pages/03_model_selection.py')

    if st.button('Proceed to encoding vector storage'):
        st.switch_page('pages/04_encoding_storage.py')

    if st.button('Proceed to Q&A Testing'):
        st.switch_page('pages/05_testing_qa.py')

    # Check if 'data' state variable is defined
    if 'data' in st.session_state:
        st.write("Data Available")
        st.write("Data (URL dataframe) is defined.")
    else:
        st.write("Data (URL dataframe) is not defined.")

    # Check if 'docs' state variable is defined
    if 'docs' in st.session_state:
        st.write("Docs (fetched and stored data collection) is defined.")
    else:
        st.write("Docs (fetched and stored data collection) is not defined.")

    # Render the navigation menu
    # menu()

if __name__ == '__main__':
    main()