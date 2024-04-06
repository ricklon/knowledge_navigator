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
    edited_df = st.data_editor(data=df, key="data_editor_key")
    return edited_df

def main():
    st.title("Data Source Configuration")
    
    if 'scanned_urls' not in st.session_state:
        st.session_state['scanned_urls'] = pd.DataFrame(columns=['URL', 'Type', 'Page Name', 'Scanned DateTime'])
    
    # Handling the clear table action
    if clear_table_clicked:
        st.session_state['scanned_urls'] = pd.DataFrame(columns=['URL', 'Type', 'Page Name', 'Scanned DateTime'])
    
    # Display the table for editing and selection
    if not st.session_state['scanned_urls'].empty:
        selected_rows = st.multiselect("Select rows to delete (by index):", st.session_state['scanned_urls'].index)
        
        # Handling row deletion
        if delete_rows_clicked and selected_rows:
            st.session_state['scanned_urls'] = st.session_state['scanned_urls'].drop(selected_rows).reset_index(drop=True)
        
        edited_df = display_editable_table(st.session_state['scanned_urls'])
        st.session_state['scanned_urls'] = edited_df

        # Convert DataFrame to CSV for download
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download URLs as CSV",
            data=csv,
            file_name='urls.csv',
            mime='text/csv',
        )

    st.subheader("Scan Websites for URLs")
    url_input = st.text_area("Enter URLs to scan, separated by new lines:")
    url_list = [url.strip() for url in url_input.strip().split('\n') if url.strip()]

    scan_button_clicked = st.button("Scan URLs")
    if scan_button_clicked:
        for url in url_list:
            unique_urls, page_title = find_linked_urls_and_title(url)
            scan_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            absolute_urls = convert_to_absolute_urls(url, unique_urls)
            internal_links, external_links = categorize_links(url, absolute_urls)
            new_entries = pd.DataFrame([(url, 'Internal', page_title, scan_datetime) for url in internal_links] +
                                       [(url, 'External', page_title, scan_datetime) for url in external_links],
                                       columns=['URL', 'Type', 'Page Name', 'Scanned DateTime'])
            st.session_state['scanned_urls'] = pd.concat([st.session_state['scanned_urls'], new_entries]).drop_duplicates().reset_index(drop=True)

    if not st.session_state['scanned_urls'].empty:
        edited_df = display_editable_table(st.session_state['scanned_urls'])
        st.session_state['scanned_urls'] = edited_df

        # Convert DataFrame to CSV for download
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download URLs as CSV",
            data=csv,
            file_name='urls.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()
