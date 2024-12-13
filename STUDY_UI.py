import streamlit as st
import tempfile

# Title at the top of the app
st.markdown("<h1 style='text-align: center;'>BlankAI Study</h1>", unsafe_allow_html=True)

# Search query input
search_query = st.text_input("Enter your query")
st.subheader("Search Results")

# Microphone button next to the search bar
if st.button("🎤 Mic"):
    st.write("Mic button pressed! (Currently does nothing)")

# Sidebar for uploads
with st.sidebar:
    # Upload PDF files
    st.subheader("Upload PDF Files")
    uploaded_files = st.file_uploader("Choose PDF files", type=["pdf", "ppt"], accept_multiple_files=True)

    # Input URLs
    st.subheader("Upload URLs")
    urls_input = st.text_area("Enter URLs (one per line)", height=50)  # Reduced height

    # Upload MP4/MP3 file
    st.subheader("Upload MP4/MP3 File")
    uploaded_video = st.file_uploader("Choose an MP4 video or MP3 file", type=["mp4", "mp3"])

# Display search results if there's a query
if search_query:
    results = f"Search Results: {search_query}"
    st.write(results)

    # Mock search results
    mock_results = [
        {"title": "Document 1", "description": "Description for document 1", "link": "https://example.com/doc1"},
        {"title": "Document 2", "description": "Description for document 2", "link": "https://example.com/doc2"},
        {"title": "Video 1", "description": "Description for video 1", "link": "https://example.com/video1"},
    ]

    for result in mock_results:
        st.markdown(f"**Title:** {result['title']}")
        st.write(f"**Description:** {result['description']}")
        st.markdown(f"[View More]({result['link']})")
        st.write("---")  # Separator for each result

# Display uploaded PDF previews
if uploaded_files:
    st.subheader("Uploaded PDF Previews")
    for uploaded_file in uploaded_files:
        # Create a temporary file to hold the PDF
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            pdf_url = temp_file.name

        # Display PDF preview using iframe
        st.markdown(f'<iframe src="data:application/pdf;base64,{uploaded_file.getvalue().decode()}" width="700" height="500"></iframe>', unsafe_allow_html=True)
        st.write("---")  # Separator

# Display uploaded video preview
if uploaded_video:
    st.subheader("Uploaded Video Preview")
    st.video(uploaded_video)
