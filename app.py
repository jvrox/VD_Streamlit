import streamlit as st
import os
import time  # Import time for delays
from final import run_inference  # Import your custom run_inference function
from PIL import Image

def main():
    st.title("Violence Detection Dashboard")
    st.subheader("How to Use This Dashboard")
    st.markdown("""
    1. **Upload a video**: Select the video file you want to analyze from the sidebar.
    2. **Upload model weights**: Choose the appropriate model weights for inference.
    3. **Set confidence interval**: Adjust the confidence interval for detection as needed.
    4. **Save the output**: Choose whether you want to save the processed video.
    5. **Start tracking**: Click the 'Start tracking' button to begin processing the video.
    """)

    # Sidebar configuration
    st.sidebar.title("Configuration")

    # Upload video
    video = st.sidebar.file_uploader("Select input video", type=["mp4", "avi"], accept_multiple_files=False)
    if video is not None:
        st.video(video)

    # Upload model weights
    weights_file = st.sidebar.file_uploader("Select model weights", type=["pt"], accept_multiple_files=False)

    # Option to save output video
    save_output_video = st.sidebar.radio("Save output video?", ('Yes', 'No'))

    # Confidence Interval input
    cf = st.sidebar.number_input("Confidence Interval", min_value=0.0, max_value=1.0, value=0.7, step=0.01)

    # Specify where to save the output video
    output_file = st.sidebar.text_input("Output file name", "output.mp4") if save_output_video == 'Yes' else "output.mp4"

    if st.sidebar.button("Start tracking"):
        if video is not None and weights_file is not None:
            # Save uploaded video and weights to temporary files
            temp_video_path = os.path.join("temp", video.name)
            with open(temp_video_path, "wb") as f:
                f.write(video.getbuffer())

            temp_weights_path = os.path.join("temp", weights_file.name)
            with open(temp_weights_path, "wb") as f:
                f.write(weights_file.getbuffer())

            # Determine the output path based on user selection
            output_path = os.path.join("temp", output_file) if save_output_video == 'Yes' else os.path.join("temp", "output.mp4")
            print(output_path)
        
            # Display progress
            progress_bar = st.progress(0)
            percentage_display = st.empty()

            # Function to update progress (call this during your inference)
            def progress_callback(step, total_steps):
                if total_steps > 0:
                    progress = (step + 1) / total_steps
                    progress = min(max(progress, 0.0), 1.0)
                    progress_bar.progress(progress)
                    percentage_display.write(f"{progress * 100:.2f}%")
                else:
                    progress_bar.progress(0.0)
                    percentage_display.write("0.00%")

            # Display the confusion matrix and analysis while the model is running
            confusion_matrix_path = "C:\\Users\\JIYA\\Desktop\\VD_Streamlit-master\\Confusion_matrix.jpg"
            st.image(confusion_matrix_path, caption="Confusion Matrix")

            st.markdown("""
            **Confusion Matrix Analysis:**
            - **Diagonal Dominance**: Indicates correct classifications.
            - **Off-Diagonal Elements**: Highlights misclassifications and errors.
            - **Normalization**: Shows proportional values for comparison across classes.
            """)

            st.markdown("""
            **Special Features of the Model:**
            - **Violence Detection**: The model detects violent activities and marks them with bounding boxes for clear visualization.
            - **Multi-Incident Recognition**: The model tracks multiple violent events simultaneously, ensuring comprehensive analysis even in complex scenarios.
            """)

            col1, col2 = st.columns(2)

            with col1:
                image1 = Image.open("C:\\Users\\JIYA\\Desktop\\VD_Streamlit-master\\1.jpg")
                st.image(image1, caption="Special Feature 1")

            with col2:
                image2 = Image.open("C:\\Users\\JIYA\\Desktop\\VD_Streamlit-master\\2.png")
                st.image(image2, caption="Special Feature 2")

            # Run inference
            run_inference(temp_video_path, output_path, temp_weights_path, cf, progress_callback)
            print(output_path)

            # Wait until the video is ready
            while not os.path.exists(output_path):
                time.sleep(1)  # Wait for 1 second before rechecking

            st.success("Inference completed. Displaying output video...")

            # Display the dynamically saved output video
            if os.path.exists(output_path):
                with open(output_path, "rb") as video_file:
                    video_bytes = video_file.read()
                    st.video(video_bytes)
            else:
                st.error("Output video could not be found.")

            # Option to download the video
            if save_output_video == 'Yes' and os.path.exists(output_path):
                with open(output_path, "rb") as f:
                    k=f.read()
                    st.video(k)
                    st.download_button(label="Download Output Video", data=f, file_name=output_file, mime='video/mp4')
        else:
            st.warning("Please upload both a video file and a model weights file to start.")

if __name__ == "__main__":
    if not os.path.exists("temp"):
        os.makedirs("temp")
    main()
