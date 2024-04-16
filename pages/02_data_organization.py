# Import necessary libraries
import streamlit as st
import pandas as pd
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain.schema import Document
from pydantic import BaseModel

from crewai import Agent, Task, Crew
from crewai_tools import BaseTool
import json
import asyncio
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Define the custom tool for analyzing HTML content
class HtmlContentAnalyzer(BaseTool):
    name: str = "HTML Content Analyzer"
    description: str = "Analyzes HTML content to find and report image and video tags."

    def _run(self, html_content: str) -> str:
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []

        # Extract all image tags
        for img in soup.find_all('img'):
            img_details = {
                'tag': 'img',
                'src': img.get('src'),
                'alt': img.get('alt', 'N/A')
            }
            results.append(img_details)

        # Extract all video tags
        for video in soup.find_all('video'):
            video_details = {
                'tag': 'video',
                'src': [source.get('src') for source in video.find_all('source')]
            }
            results.append(video_details)

        return json.dumps(results)

# Define the HTML Reviewer agent and task
html_reviewer = Agent(
    role='HTML Reviewer',
    goal='Identify and report HTML tags related to images and videos.',
    verbose=True,
    memory=True,
    backstory=(
        "As an HTML Reviewer, you meticulously scan through web pages, identifying "
        "and cataloging every image and video, ensuring no visual content is overlooked."
    ),
    tools=[HtmlContentAnalyzer()],
    allow_delegation=True
)

review_html_task = Task(
    description=(
        "Analyze the HTML content of documents to find image and video tags. "
        "Report the URLs and other relevant attributes of these tags."
    ),
    expected_output='A JSON string with details of all image and video tags found.',
    tools=[HtmlContentAnalyzer()],
    agent=html_reviewer,
)

document_review_crew = Crew(
    agents=[html_reviewer],
    tasks=[review_html_task]
)

# Async function to fetch documents
async def fetch_documents(urls):
    loader = AsyncHtmlLoader(urls)
    docs = await loader.aload()
    return docs

# Review documents function
def review_documents(docs):
    html_content = ' '.join(doc.text for doc in docs if hasattr(doc, 'text'))
    result = document_review_crew.kickoff(inputs={'html_content': html_content})
    return json.loads(result)  # Convert JSON string to Python object for easier processing

# Main function for Streamlit app
def fetch_clean_organize_page():
    st.title("Fetch, Clean, and Organize Documents")

    # Check session state
    if 'data' not in st.session_state:
        st.warning("No data found. Please go back to the previous page and scan URLs first.")
        return

    data = st.session_state['data']
    st.write("URLs to fetch and clean:")
    st.write(data)

    # Filter and fetch documents
    valid_urls = data[(data['Ignore'] == False) & (data['URL'].apply(is_valid_url))]['URL'].tolist()
    if st.button("Fetch Documents"):
        docs = asyncio.run(fetch_documents(valid_urls))
        st.session_state['docs'] = docs
        st.write(f"Fetched {len(st.session_state['docs'])} documents.")

    # Review documents and display results in a DataFrame
    if 'docs' in st.session_state and st.button("Review HTML Content"):
        results = review_documents(st.session_state['docs'])
        st.session_state['review_results'] = results
        df = pd.DataFrame(results)
        st.write("Reviewed Data:")
        st.dataframe(df)

    # Additional UI components for saving and downloading reviewed content
    if 'review_results' in st.session_state and st.button("Save Reviewed Data"):
        with open("reviewed_data.json", "w") as file:
            json.dump(st.session_state['review_results'], file)
        with open("reviewed_data.json", "rb") as file:
            st.download_button("Download Reviewed Data", data=file, file_name="reviewed_data.json")

# Call the main function
fetch_clean_organize_page()
