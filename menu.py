import streamlit as st

def menu():
    # Show the navigation menu
    st.sidebar.button("Data Collection", on_click=lambda: st.switch_page("pages/data_collection.py"))
    st.sidebar.button("Data Organization", on_click=lambda: st.switch_page("pages/data_organization.py"))
    # st.sidebar.button("Model Selection", on_click=lambda: st.switch_page("model_selection"))
    # st.sidebar.button("Encoding & Storage", on_click=lambda: st.switch_page("encoding_storage"))
    # st.sidebar.button("Testing & QA", on_click=lambda: st.switch_page("testing_qa"))