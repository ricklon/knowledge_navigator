import streamlit as st
import pandas as pd

# Initialize global session state variables if they don't exist
if 'scanned_urls' not in st.session_state:
    st.session_state['scanned_urls'] = {}

if 'selected_urls' not in st.session_state:
    st.session_state['selected_urls'] = pd.DataFrame()

st.title('Knowledge Navigator')
