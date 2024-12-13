import streamlit as st
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import WebBaseLoader, PyPDFLoader
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import os
from docx import Document
from io import StringIO
import os
os.environ["COHERE_API_KEY"] = 'pQjiTygxrqjSEjHHilJicUWiFpXPVv7ZapihqKo7'

# Initialize Cohere Embeddings
embd = CohereEmbeddings(model="embed-english-v2.0", user_agent="langchain-agent")

# Initialize Chroma Vector Store
def initialize_vector_store(documents):
    if not documents:
        raise ValueError("No documents to index.")
    
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512,
        chunk_overlap=0
    )
    all_splits = text_splitter.split_documents(documents)
    if not all_splits:
        raise ValueError("No document chunks to index.")
    
    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=embd,
        persist_directory="./chroma_db"
    )
    return vectorstore.as_retriever()

# Load and process documents
def load_documents(uploaded_files, urls):
    documents = []

    # Process uploaded files
    for uploaded_file in uploaded_files:
        # Save uploaded file as temporary file
        file_extension = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        # Add temp file path to documents list
        if uploaded_file.type == "application/pdf":
            pdf_docs = PyPDFLoader(temp_file_path).load()
            documents.extend(pdf_docs)
        elif uploaded_file.type in ["application/vnd.ms-powerpoint", "application/vnd.openxmlformats-officedocument.presentationml.presentation"]:
            # Implement PPT processing here (add temp_file_path to documents list after processing)
            pass
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            docx_text = read_docx(temp_file_path)
            documents.append({"text": docx_text, "source": temp_file_path})
        elif uploaded_file.type in ["audio/mpeg", "video/mp4"]:
            # Process MP4/MP3 file (you can add transcription or video file path here)
            pass

    # Process URLs
    for url in urls:
        web_docs = WebBaseLoader(url).load()
        documents.extend(web_docs)

    return documents

# Read DOCX file
def read_docx(temp_file_path):
    doc = Document(temp_file_path)
    doc_text = []
    for para in doc.paragraphs:
        doc_text.append(para.text)
    return "\n".join(doc_text)

# Transcribe video to text
def transcribe_video(video_path, chunk_length=30):
    video = VideoFileClip(video_path)
    audio_path = r"extracted_audio.wav"
    video.audio.write_audiofile(audio_path)
    recognizer = sr.Recognizer()
    timestamps_texts = []
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        duration = len(audio.frame_data) / audio.sample_rate / audio.sample_width
        for start_time in range(0, int(duration), chunk_length):
            start_frame = int(start_time * audio.sample_rate * audio.sample_width)
            end_frame = int((start_time + chunk_length) * audio.sample_rate * audio.sample_width)
            audio_chunk = sr.AudioData(audio.frame_data[start_frame:end_frame], audio.sample_rate, audio.sample_width)
            try:
                text = recognizer.recognize_google(audio_chunk)
                timestamps_texts.append((start_time, text))
            except sr.UnknownValueError:
                timestamps_texts.append((start_time, "[Unintelligible]"))
            except sr.RequestError as e:
                print(f"Error with the Speech Recognition service: {e}")
                break
    os.remove(audio_path)
    return timestamps_texts

# Title at the top of the app
st.markdown("<h1 style='text-align: center;'>Note.AI</h1>", unsafe_allow_html=True)

# Sidebar for uploads
with st.sidebar:
    st.subheader("Upload PDF/PPT Files")
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "ppt", "pptx", "docx", "mp4", "mp3"], accept_multiple_files=True)

    st.subheader("Input URLs")
    urls_input = st.text_area("Enter URLs (one per line)", height=50)
    urls = urls_input.splitlines()

# Load and index documents
if uploaded_files or urls:
    documents = load_documents(uploaded_files, urls)
    vectorstore_retriever = initialize_vector_store(documents)

# Search query input
search_query = st.text_input("Enter your query")
if search_query:
    results = vectorstore_retriever.get_relevant_documents(search_query)

    # Display search results
    st.subheader("Search Results")
    for result in results:
        snippet = result.page_content
        metadata = result.metadata
        citation = metadata.get('source', 'Unknown source')
        
        if 'Video at' in citation:
            timestamp = citation.split('at ')[1]
            citation = f"Video timestamp: {timestamp}s"
        
        st.markdown(f"**Snippet:** {snippet}")
        st.write(f"**Citation:** {citation}")

        # Handle file display
        if 'pdf' in citation or 'ppt' in citation:
            st.markdown(f"**[View Document]({citation})**")
        elif 'video' in citation:
            st.video(citation)
        elif 'audio' in citation:
            st.audio(citation)

    st.write("---")  # Separator for each result
