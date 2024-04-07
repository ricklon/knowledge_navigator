import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from langchain.schema import Document
import json
from typing import Iterable
import os
from datetime import datetime
import zipfile
import tempfile

def save_docs_to_jsonl(array:Iterable[Document], file_path:str)->None:
    with open(file_path, 'w') as jsonl_file:
        for doc in array:
            jsonl_file.write(doc.json() + '\n')

def load_docs_from_jsonl(file)->Iterable[Document]:
    array = []
    for line in file:
        data = json.loads(line.decode('utf-8'))
        obj = Document(**data)
        array.append(obj)
    return array

st.title('Encoding and Storage')

# Create output directory
start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_DIR = "./out"

# Check if the directory exists, and if not, create it
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    st.write(f"Directory '{OUTPUT_DIR}' was created.")
else:
    st.write(f"Directory '{OUTPUT_DIR}' already exists.")

# Allow the user to upload the JSON file if missing
# Allow the user to upload the JSONL file if missing
if 'docs' not in st.session_state:
    st.write("Document collection not found in session state.")
    uploaded_file = st.file_uploader("Upload JSONL file", type=["jsonl"])
    if uploaded_file is not None:
        try:
            docs = load_docs_from_jsonl(uploaded_file)
            st.session_state['docs'] = docs
            st.write(f"Loaded {len(docs)} documents from the uploaded file.")
        except Exception as e:
            st.error(f"Error loading JSONL file: {str(e)}")
else:
    docs = st.session_state['docs']
    st.write(f"Loaded {len(docs)} documents from the session state.")
# Show the embedding model
EMBEDDING_MODEL_NAME = st.session_state.get('selected_embedding_model', "thenlper/gte-small")
st.write(f"Selected Embedding Model: {EMBEDDING_MODEL_NAME}")

# Allow the user to select the device (GPU or CPU)
device_form = st.form(key='device_form')
device = device_form.radio("Select Device", ("CUDA", "CPU"))
submit_device = device_form.form_submit_button(label='Submit Device')

if submit_device:
    # Set up the embedding model
    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        multi_process=True,
        model_kwargs={"device": device.lower()},
        encode_kwargs={"normalize_embeddings": True},  # set True for cosine similarity
    )

    # Show the configuration
    st.write("Embedding Model Configuration:")
    st.write(embedding_model)

    # Start the encoding
    if 'docs' in st.session_state:
        progress_bar = st.progress(0)
        total_docs = len(docs)

        collection_vectorstore = FAISS.from_documents(docs, embedding=embedding_model)
        st.session_state['collection_vectorstore'] = collection_vectorstore

        for i in range(total_docs):
            progress_bar.progress((i + 1) / total_docs)

        st.write("Encoding completed.")
    else:
        st.write("No documents found in the session state.")
        
 # Allow saving and downloading the configuration
if st.button("Save and Download Configuration"):
    if 'collection_vectorstore' in st.session_state:
        collection_vectorstore = st.session_state['collection_vectorstore']
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        zip_filename = f"docs_vectors_{timestamp}.zip"

        with tempfile.TemporaryDirectory() as temp_dir:
            collection_vectorstore.save_local(f"{temp_dir}/docs_vectors")

            with zipfile.ZipFile(zip_filename, "w") as zip_file:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_file.write(file_path, os.path.relpath(file_path, temp_dir))

            with open(zip_filename, "rb") as zip_file:
                zip_bytes = zip_file.read()

            st.download_button(
                label="Download Configuration",
                data=zip_bytes,
                file_name=zip_filename,
                mime="application/zip",
            )

        st.success("Configuration saved and downloaded.")
    else:
        st.warning("No vector store found. Please make sure the encoding is completed.")

if st.button('Proceed to Q&A Testing'):
    st.switch_page('pages/05_testing_qa.py')