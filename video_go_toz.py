
path = r"C:\Users\Admin\Downloads\4f5fc4f1407b5bb19d1ce9d1274f57fa6e72d850.mp4"
import cv2

def play_video_from_timestamp(video_path, start_time_sec):
    """
    Play video from a specific timestamp.

    Args:
        video_path (str): Path to the input video file.
        start_time_sec (int): Starting timestamp in seconds.
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return
    
    # Set the video position to the start time
    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = int(fps * start_time_sec)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Display the frame
        cv2.imshow('Video', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Example usage
play_video_from_timestamp(path, start_time_sec=840)
