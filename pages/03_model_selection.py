import streamlit as st

st.title('Model Selection')

# Introduction
st.write("Select the embedding model and the large language model (LLM) for processing.")

# Embedding Model Selection
embedding_models = ["thenlper/gte-small", "sentence-transformers/all-MiniLM-L6-v2", "other"]
selected_embedding_model = st.selectbox("Select Embedding Model", options=embedding_models)

# LLM Model Selection
llm_models = ["mistralai/Mistral-7B-Instruct-v0.2", "gpt-3.5-turbo", "other"]
selected_llm_model = st.selectbox("Select LLM Model", options=llm_models)

# Display selections (for demonstration)
st.write("Selected Embedding Model:", selected_embedding_model)
st.write("Selected LLM Model:", selected_llm_model)

# Configuration options for the selected models
st.header("Model Configuration")

# Embedding Model Configuration (example)
if selected_embedding_model == "thenlper/gte-small":
    # Placeholder for model-specific configuration options
    st.write("No additional configuration required for this model.")
else:
    # Configuration for other models
    st.write("Configuration options for other models will appear here.")

# LLM Model Configuration (example)
if selected_llm_model == "mistralai/Mistral-7B-Instruct-v0.2":
    max_tokens = st.slider("Max Tokens", min_value=100, max_value=1000, value=250)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
else:
    # Configuration for other models
    st.write("Configuration options for other models will appear here.")

# Save model selections and configurations
if st.button("Save Model Configuration"):
    st.session_state['selected_embedding_model'] = selected_embedding_model
    st.session_state['selected_llm_model'] = selected_llm_model
    
    # Assuming configurations are more complex and vary per model, you might want to store them differently
    st.session_state['llm_model_config'] = {"max_tokens": max_tokens, "temperature": temperature}
    
    st.success("Model configurations saved.")

if st.button('Proceed to encoding vector storage'):
    st.switch_page('pages/04_encoding_storage.py')