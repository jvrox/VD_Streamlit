import streamlit as st
import os
from final import run_inference  # Import your custom run_inference function

def main():
    st.title("Violence Detection Dashboard")

    # Sidebar configuration
    st.sidebar.title("Configuration")

    
    # Upload video
    video = st.sidebar.file_uploader("Select input video", type=["mp4", "avi"], accept_multiple_files=False)
    # Display the uploaded video if available
    if video is not None:
        st.video(video)

    # Upload model weights
    weights_file = st.sidebar.file_uploader("Select model weights", type=["pt"], accept_multiple_files=False)

    # Option to save output video
    save_output_video = st.sidebar.radio("Save output video?", ('Yes', 'No'))

    cf = st.sidebar.number_input("Confidence Interval", min_value=0.0, max_value=1.0, value=0.7, step=0.01)


    # Specify where to save the output video if the user chooses to save it
    output_file = st.sidebar.text_input("Output file name", "output.mp4") if save_output_video == 'Yes' else None

    

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

            # # Determine the output path
            output_path ="C:\\Users\\debas\\OneDrive\\Desktop\\VD_Streamlit-master\\temp"
        
            # Display progress
            progress_bar = st.progress(0)
            percentage_display = st.empty()
        
        # Function to update progress (call this during your inference)
            def progress_callback(step, total_steps):
                if total_steps > 0:
                    progress = (step + 1) / total_steps
                     # Clamp progress to ensure it's within [0.0, 1.0]
                    progress = min(max(progress, 0.0), 1.0)
                    progress_bar.progress(progress)
                    percentage_display.write(f"{progress * 100:.2f}%")
                else:
                     # Handle the case where total_steps is zero to avoid division by zero
                    progress_bar.progress(0.0)
                    percentage_display.write("0.00%")
            # Determine the output path based on user input
            if save_output_video == 'Yes' and output_file:
                output_path = os.path.join("temp", output_file)
                
            else:
                output_path = os.path.join("temp", "temp_output.mp4")
        

            # Run inference with the specified model weights and progress callback
            run_inference(temp_video_path, output_path,temp_weights_path,cf,progress_callback)

           
            
            # Display the output video
            if save_output_video == 'Yes' and output_file:
                 output_video_path = os.path.join("temp", output_file)
            else:
                 output_video_path = os.path.join("temp", "temp_output.mp4")
            st.video(output_video_path)

            if save_output_video == 'Yes':
                
                with open(output_path, "rb") as f:
                    st.download_button(label="Download Output Video", data=f, file_name=output_file, mime='video/mp4')
            else:
                
                st.success("Inference completed. The output video is available below.")
                
        else:
            st.warning("Please upload both a video file and a model weights file to start.")

if __name__ == "__main__":
    if not os.path.exists("temp"):
        os.makedirs("temp")
    main()
