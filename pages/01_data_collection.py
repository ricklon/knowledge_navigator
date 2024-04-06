import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

def find_linked_urls_and_title(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            urls = {link.get('href') for link in links if link.get('href') is not None}
            title_tag = soup.find('title')
            page_title = title_tag.text if title_tag else 'No Title Found'
            return urls, page_title
        else:
            st.write(f"Failed to retrieve {url}")
            return set(), 'No Title Found'
    except Exception as e:
        st.write(f"An error occurred with {url}: {e}")
        return set(), 'No Title Found'

def convert_to_absolute_urls(base_url, links):
    return {urljoin(base_url, link) if not link.startswith('http') else link for link in links}

def categorize_links(base_url, links):
    internal_links, external_links = set(), set()
    for link in links:
        if urlparse(link).netloc == urlparse(base_url).netloc:
            internal_links.add(link)
        else:
            external_links.add(link)
    return internal_links, external_links

def display_editable_table(df):
    edited_df = st.data_editor(data=df, key="data_editor_key", num_rows="dynamic")  # Add num_rows="dynamic" to allow adding/deleting rows
    return edited_df

def prepare_dataframe(df):
    if "Ignore" not in df.columns:
        df["Ignore"] = False  # Initialize all values as False
    return df

def store_data(df):
    st.session_state['data'] = df

def main():
    st.title("Data Source Configuration")
    
    # Initialize 'scanned_urls' with all columns, including 'Ignore'
    if 'scanned_urls' not in st.session_state:
        st.session_state['scanned_urls'] = pd.DataFrame(columns=['URL', 'Type', 'Page Name', 'Scanned DateTime', 'Ignore'])
    
    st.subheader("Scan Websites for URLs")
    url_input = st.text_area("Enter URLs to scan, separated by new lines:", "https://fubarlabs.org")
    url_list = [url.strip() for url in url_input.strip().split('\n') if url.strip()]
    scan_button_clicked = st.button("Scan URLs")
    
    if scan_button_clicked:
        for url in url_list:
            unique_urls, page_title = find_linked_urls_and_title(url)
            scan_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            absolute_urls = convert_to_absolute_urls(url, unique_urls)
            internal_links, external_links = categorize_links(url, absolute_urls)
            
            new_entries = pd.DataFrame([(url, 'Internal', page_title, scan_datetime, False) for url in internal_links] + 
                                       [(url, 'External', page_title, scan_datetime, False) for url in external_links],
                                       columns=['URL', 'Type', 'Page Name', 'Scanned DateTime', 'Ignore'])  # Include 'Ignore' column
            st.session_state['scanned_urls'] = pd.concat([st.session_state['scanned_urls'], new_entries]).drop_duplicates().reset_index(drop=True)
            store_data(st.session_state['scanned_urls'])

    if not st.session_state['scanned_urls'].empty:
        # Prepare the dataframe, this now includes the 'Ignore' column from the start
        prepared_df = prepare_dataframe(st.session_state['scanned_urls'])
        
        # Display the editable table with an "Ignore" column
        edited_df = display_editable_table(prepared_df)
        
        if edited_df is not None:
            st.session_state['scanned_urls'] = edited_df

        # Access the edits made to the table
        if "data_editor_key" in st.session_state:
            edits = st.session_state["data_editor_key"]
            st.write("Edits made to the table:")
            st.write(edits)

        if st.button('Proceed to Data Organization'):
            st.switch_page('pages/02_data_organization.py')

if __name__ == "__main__":
    main()