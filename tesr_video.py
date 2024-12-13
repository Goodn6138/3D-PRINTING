import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import WebBaseLoader, PyPDFLoader
import tempfile
import os
os.environ["COHERE_API_KEY"] = 'pQjiTygxrqjSEjHHilJicUWiFpXPVv7ZapihqKo7'
# Initialize Cohere Embeddings
embd = CohereEmbeddings(model="embed-english-v2.0", user_agent="langchain-agent")

# Initialize an empty list to store documents
all_docs_list = []

# Streamlit layout
st.set_page_config(layout="wide")
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.header("Uploaded Files")
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        st.write("PDF files loaded:")
        for uploaded_file in uploaded_files:
            st.write(f"- {uploaded_file.name}")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

                # Load PDF documents
                pdf_docs = PyPDFLoader(temp_file_path).load()
                all_docs_list.extend(pdf_docs)

        st.write("PDF files loaded successfully.")

with col2:
    st.header("Web Page Content")
    urls_input = st.text_area("Enter URLs (one per line)")

    if urls_input:
        urls = urls_input.splitlines()
        web_docs = [WebBaseLoader(url).load() for url in urls]
        web_docs_list = [item for sublist in web_docs for item in sublist]
        all_docs_list.extend(web_docs_list)
        st.write("Web pages loaded successfully.")

    # Display selected web page content
    if st.button("Show Content"):
        if all_docs_list:
            st.write("Showing content of selected documents...")
            # Display content from the documents
            for doc in all_docs_list:
                st.write(doc.page_content)

with col3:
    st.header("AI Chat")
    st.text_area("Enter your query:")

    # Input box for the query
    query = st.text_input("Enter your query:")

    # Process query when button is pressed
    if st.button("Search"):
        if all_docs_list:
            # Split documents into chunks for better embedding performance
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=512,  # Size of each chunk
                chunk_overlap=0  # No overlap between chunks
            )
            # Split all documents
            all_splits = text_splitter.split_documents(all_docs_list)

            # Initialize the Chroma vector store
            vectorstore = Chroma.from_documents(
                documents=all_splits,
                embedding=embd,
                persist_directory="./chroma_db"  # Directory to store the database
            )

            # Set up retriever for querying the vector store
            retriever = vectorstore.as_retriever()

            def search_query(query):
                # Retrieve relevant documents (chunks) for the query
                results = retriever.get_relevant_documents(query)

                # Extract snippets and their citations
                response = []
                for result in results:
                    snippet = result.page_content  # Get the first 300 characters as a snippet, adjust as necessary
                    metadata = result.metadata  # Access metadata if available, like source or page numbers

                    # Assuming metadata contains a "source" field for citation (modify based on your loader)
                    citation = metadata.get('source', 'Unknown source')

                    response.append((snippet, citation))
                    break  # Adjust this if you want more than one result

                return response

            st.write("Searching...")
            results = search_query(query)

            for snippet, citation in results:
                st.write(f"**Snippet:** {snippet}")
                st.write(f"**Citation:** {citation}")
        else:
            st.write("No documents available to search.")

# Video Upload Section
st.header("Upload and Play Videos")

# Upload video file
uploaded_video = st.file_uploader("Upload an MP4 file", type="mp4")

# Check if a video is uploaded and display it
if uploaded_video:
    # Display the video using Streamlit's video component
    st.video(uploaded_video)
