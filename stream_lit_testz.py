import streamlit as st
import tempfile
import os

uploaded_file = st.file_uploader("Choose file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    file_extension = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(bytes_data)
        temp_file_path = temp_file.name  # Get the temporary file path

    # Display the temp file path
    st.write(f"Temporary {file_extension} file created at: {temp_file_path}")
