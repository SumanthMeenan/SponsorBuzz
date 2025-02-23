import streamlit as st
import time
import pandas as pd
import re
import subprocess
import os 

if "processed" not in st.session_state:
    st.session_state.processed = False
if "page" not in st.session_state:
    st.session_state.page = "home"
if "video_url" not in st.session_state:
    st.session_state.video_url = ""  
if "analysis_data" not in st.session_state:  # Initialize analysis data
    st.session_state.analysis_data = None

def run_brand_analysis(video_url):
    # Constructing the command to run video_analyzer.py
    command1 = f'python download_video.py {video_url} "data/daily_motion.mp4" '
    command2 = f'python video_analyzer.py "data/daily_motion.mp4" --csv "output.csv" --json "output.json" '
    try:
        # Run the command using subprocess
        #subprocess.run(command1, shell=True, check=True, text=True, capture_output=True)
        result = subprocess.run(command2, shell=True, check=True, text=True, capture_output=True)
        if os.path.exists("output.csv"):
            df = pd.read_csv("output.csv")
            st.session_state.analysis_data = df 
            st.success(f"Brand analysis completed successfully:\n{result.stdout}")
        else:
            st.error("Brand analysis failed. CSV file not found.")
    
    except subprocess.CalledProcessError as e:
        st.error(f"Error in brand analysis:\n{e.stderr}")
    return result 

def process_video(video_url):
    time.sleep(3) 
    return f"Processed video from {video_url}"

def is_dailymotion_url(url):
    # Regex to check if the URL is a Dailymotion video URL
    return re.match(r'https://www.dailymotion.com/video/([a-zA-Z0-9_-]+)', url) is not None

if st.session_state.page == "home":
    st.title("Video Processing App")

    if not st.session_state.processed:
        st.session_state.video_url = st.text_input("Enter Video URL")  # Store in session state
        
        if st.button("Process") and st.session_state.video_url.strip():
            with st.spinner("Processing... Please wait!"):
                st.session_state.result = process_video(st.session_state.video_url)
            st.session_state.processed = True
            st.rerun()  

    else:
        st.success("Processing Complete!")
        
        if is_dailymotion_url(st.session_state.video_url):
            # Embedding Dailymotion video using iframe format
            video_id = st.session_state.video_url.split("/")[-1]
            video_embed_url = f"https://www.dailymotion.com/embed/video/{video_id}"
            st.markdown(f'<iframe width="640" height="360" src="{video_embed_url}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
        else:
            st.video(st.session_state.video_url)  # This works for other video types like YouTube

        if st.button("Brand Analysis"):
            run_brand_analysis(st.session_state.video_url)
            st.session_state.page = "analysis"
            st.rerun()  

elif st.session_state.page == "analysis":
    st.title("Brand Analysis")
    st.subheader("Analysis Data")

    if st.session_state.analysis_data is not None:
        st.table(st.session_state.analysis_data)
    else:
        st.warning("No analysis data available. Please go back and run the analysis again.")

    if st.button("Back"):
        st.session_state.processed = False  
        st.session_state.video_url = ""  
        st.session_state.analysis_data = None  # Clear stored analysis data
        st.session_state.page = "home"
        st.rerun()