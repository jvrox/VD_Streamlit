import streamlit as st
import cv2
from final import run_inference  # Import your custom run_inference function
import os

def main():
    
    
    st.title("Violence Detection Dashboard")
    
    # Sidebar configuration
    st.sidebar.title("Configuration")

    # Upload video
    video = st.sidebar.file_uploader("Select input video", type=["mp4", "avi"], accept_multiple_files=False)
    
    # Upload model weights
    weights_file = st.sidebar.file_uploader("Select model weights", type=["pt"], accept_multiple_files=False)
    
    # Option to save output video
    save_output_video = st.sidebar.radio("Save output video?", ('Yes', 'No'))
    
    # Specify where to save the output video if the user chooses to save it
    if save_output_video == 'Yes':
        output_file = st.sidebar.text_input("Output file name", "output.mp4")
    else:
        output_file = None

    # Button to start processing
    if st.sidebar.button("Start tracking"):
        if video is not None and weights_file is not None:
            # Save uploaded video to a temporary file
            temp_video_path = os.path.join("temp", video.name)
            with open(temp_video_path, "wb") as f:
                f.write(video.getbuffer())
            
            # Save uploaded weights file to a temporary location
            temp_weights_path = os.path.join("temp", weights_file.name)
            with open(temp_weights_path, "wb") as f:
                f.write(weights_file.getbuffer())
            
            # Determine the output path
            if save_output_video == 'Yes' and output_file:
                output_path = os.path.join("temp", output_file)
            else:
                output_path = os.path.join("temp", "temp_output.mp4")
            
            # Run inference with the specified model weights
            run_inference(temp_video_path, output_path)
            
            # Display the output video
            st.video(output_path)
            
            if save_output_video == 'Yes':
                with open(output_path, "rb") as f:
                    st.download_button(label="Download Output Video", data=f, file_name=output_file, mime='video/mp4')
            else:
                st.success("Inference completed. The output video is temporarily available below.")

        else:
            st.warning("Please upload both a video file and a model weights file to start.")

if __name__ == "__main__":
    if not os.path.exists("temp"):
        os.makedirs("temp")
    main()
