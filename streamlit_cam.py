import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from PIL import Image
import io

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame = None

    def recv(self, frame):
        self.frame = frame
        return frame

def main():
    st.title("Capture and Save Photo")

    # Initialize the video stream
    webrtc_streamer(key="example", video_processor_factory=VideoProcessor)

    if st.button("Capture"):
        # Access the frame from the video stream
        video_processor = webrtc_streamer.video_processor_factory()
        if video_processor.frame is not None:
            # Convert the frame to PIL image
            img = Image.fromarray(video_processor.frame.to_ndarray())
            
            # Save the image
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            st.image(img, caption="Captured Image", use_column_width=True)
            st.download_button(
                label="Download Image",
                data=img_bytes,
                file_name="captured_image.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()
