# 02_data_organization.py
import streamlit as st
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain.schema import Document
import json
from typing import Iterable
import asyncio
from urllib.parse import urlparse

# Async fetch function
async def fetch_documents(urls):
    loader = AsyncHtmlLoader(urls)
    docs = await loader.aload()
    return docs

def save_docs_to_jsonl(array: Iterable[Document], file_path: str) -> None:
    with open(file_path, 'w') as jsonl_file:
        for doc in array:
            if hasattr(doc, 'to_dict'):
                jsonl_file.write(json.dumps(doc.to_dict()) + '\n')
            else:
                jsonl_file.write(json.dumps(doc.__dict__) + '\n')
                
def load_docs_from_jsonl(file_path) -> Iterable[Document]:
    array = []
    with open(file_path, 'r') as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            obj = Document(**data)
            array.append(obj)
    return array

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def fetch_clean_organize_page():
    st.title("Fetch, Clean, and Organize Documents")

    # Check if 'data' exists in the session state
    if 'data' not in st.session_state:
        st.warning("No data found. Please go back to the previous page and scan URLs first.")
        return

    data = st.session_state['data']
    st.write("URLs to fetch and clean:")
    st.write(data)

    # Filter out URLs marked as "Ignore" and invalid URLs
    valid_urls = data[(data['Ignore'] == False) & (data['URL'].apply(is_valid_url))]['URL'].tolist()

    if st.button("Fetch Documents"):
        docs = asyncio.run(fetch_documents(valid_urls))
        st.session_state['docs'] = docs
        st.write(f"Fetched {len(st.session_state['docs'])} documents.")

    if 'docs' in st.session_state:
        if st.button("Save Documents as JSON"):
            save_docs_to_jsonl(st.session_state['docs'], "documents.jsonl")
            st.success("Documents saved as JSON.")

            # Provide download link (streamlit >= 0.88.0)
            with open("documents.jsonl", "rb") as file:
                btn = st.download_button(
                    label="Download JSON",
                    data=file,
                    file_name="documents.jsonl",
                    mime="application/octet-stream"
                )

# Assuming this function is called in your app
fetch_clean_organize_page()