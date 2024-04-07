import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import tempfile
import zipfile
import os

st.title('Testing and QA')

# Dynamically load the selected models from the session state
EMBEDDING_MODEL_NAME = st.session_state.get('selected_embedding_model', "thenlper/gte-small")
LLM_MODEL_NAME = st.session_state.get('selected_llm_model', "mistralai/Mistral-7B-Instruct-v0.2")

# Initialization block for embedding_model, with a debug message
if 'embedding_model' not in st.session_state:
    EMBEDDING_MODEL_NAME = st.session_state.get('selected_embedding_model', "thenlper/gte-small")
    st.session_state['embedding_model'] = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        multi_process=True,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    st.info("embedding_model has been initialized.")  # Debug message for initialization
else:
    st.info("embedding_model was already initialized.")  # Debug message if already initialized

# Now that we've ensured embedding_model is initialized, we can safely access it
embedding_model = st.session_state['embedding_model']
st.write("Accessing embedding_model...")  # Debug message for accessing

# Form for LLM settings, allowing dynamic model selection
with st.form("llm_settings_form"):
    st.subheader("LLM Settings")
    repo_id = st.text_input("Repo ID", value=LLM_MODEL_NAME, key="repo_id")
    max_new_tokens = st.number_input("Max New Tokens", value=250, key="max_new_tokens")
    top_k = st.number_input("Top K", value=3, key="top_k")
    top_p = st.number_input("Top P", value=0.95, key="top_p")
    typical_p = st.number_input("Typical P", value=0.95, key="typical_p")
    temperature = st.number_input("Temperature", value=0.01, key="temperature")
    repetition_penalty = st.number_input("Repetition Penalty", value=1.035, key="repetition_penalty")

    submitted = st.form_submit_button("Update LLM Settings")
    if submitted:
        st.session_state['llm'] = HuggingFaceEndpoint(
            repo_id=repo_id,
            max_new_tokens=max_new_tokens,
            top_k=top_k,
            top_p=top_p,
            typical_p=typical_p,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
        )
        st.success("LLM settings updated.")

# Vector store upload and setup
if 'collection_vectorstore' not in st.session_state:
    uploaded_file = st.file_uploader("Upload Vector Store ZIP", type=["zip"])
    if uploaded_file is not None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            docs_vectors_path = os.path.join(temp_dir, "docs_vectors")
            st.session_state['collection_vectorstore'] = FAISS.load_local(docs_vectors_path, embeddings=embedding_model, allow_dangerous_deserialization=True)
            st.success("Vector store uploaded and loaded successfully.")

             # Create the retriever as soon as the vector store is created
            st.session_state['retriever'] = st.session_state['collection_vectorstore'].as_retriever()
            st.info("Retriever has been created.")  # Debug message to confirm the retriever's creation


# Check if LLM and vector store are ready
if 'llm' in st.session_state and 'collection_vectorstore' in st.session_state:
    # Use a button to indicate when to update the prompt template
    if st.button("Update Prompt Template"):
        # Assuming you have a text area where users input the new template
        new_template = st.text_area("Enter new prompt template", key="new_prompt_template")
        # Update the session state only when the button is pressed
        st.session_state['prompt_template'] = new_template
        st.success("Prompt template updated.")

    # Ensure there's a default prompt template
    if 'prompt_template' not in st.session_state:
        st.session_state['prompt_template'] = "You are a knowledgeable assistant answering the following question based on the provided documents: {context} Question: {question}"
    
    # Display the current template for editing
    current_template = st.text_area("Edit Prompt Template", value=st.session_state['prompt_template'], key="current_prompt_template")

    # Question input and processing
question = st.text_input("Enter your question", key="question_input")

if question:
    llm = st.session_state['llm']
    prompt = ChatPromptTemplate.from_template(current_template)
    retriever = st.session_state['retriever']
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    if st.button("Ask"):
        result = chain.invoke(question)
        st.subheader("Answer:")
        st.write(result)
else:
    st.warning("Please configure and submit the LLM settings and ensure the vector store is loaded to ask questions.")
