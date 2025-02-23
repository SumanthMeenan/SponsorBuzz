import streamlit as st
import pandas as pd
import seaborn as sns
import os
import subprocess 
import re, time 
from matplotlib import pyplot as plt
import io 

# Ensure Matplotlib does not use the default GUI backend
import matplotlib
matplotlib.use("Agg")

# Initialize session state variables
if "processed" not in st.session_state:
    st.session_state.processed = False
if "page" not in st.session_state:
    st.session_state.page = "home"
if "video_url" not in st.session_state:
    st.session_state.video_url = ""  
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None
if "truth_data" not in st.session_state:
    st.session_state.truth_data = None
if "accuracy" not in st.session_state:
    st.session_state.accuracy = None

def calculate_accuracy(analysis_df, truth_df):
    """Calculate accuracy of detected brands compared to ground truth."""
    if analysis_df is None or truth_df is None:
        st.error("Missing analysis or truth data.")
        return None

    # Ensure brand names are lowercase for case-insensitive comparison
    detected_brands = set(analysis_df['brand_name'].str.lower())
    true_brands = set(truth_df['brand_name'].str.lower())

    # Calculate correct predictions
    correct_predictions = detected_brands.intersection(true_brands)

    # Compute accuracy
    accuracy = (len(correct_predictions) / len(true_brands)) * 100 if len(true_brands) > 0 else 0
    return accuracy
 
def visualize_advertisement_data(df):
    """Generate plots for brand advertisement data."""
    if df is None or df.empty:
        st.warning("No data available for visualization.")
        return

    # Create a 2x2 grid layout for the plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Advertisement Time by Industry
    sns.barplot(x="industry", y="total_sec_displayed", data=df, hue="industry", palette="coolwarm", ax=axes[0, 0], legend=False)
    axes[0, 0].set_xlabel("Industry")
    axes[0, 0].set_ylabel("Total Seconds Displayed")
    axes[0, 0].set_title("Advertisement Time by Industry")
    axes[0, 0].tick_params(axis='x', rotation=45)

    # 2. Advertisement Type Analysis (Pie Chart)
    ad_type_counts = df["ad_type"].value_counts()
    axes[0, 1].pie(ad_type_counts, labels=ad_type_counts.index, autopct="%1.1f%%", colors=sns.color_palette("viridis", len(ad_type_counts)))
    axes[0, 1].set_title("Advertisement Type Distribution")

    # 3. Brand Representation by Country
    sns.countplot(y="country", data=df, hue="country", palette="magma", order=df["country"].value_counts().index, ax=axes[1, 0], legend=False)
    axes[1, 0].set_xlabel("Count")
    axes[1, 0].set_ylabel("Country")
    axes[1, 0].set_title("Brand Representation by Country")

    # 4. Top Advertisers by Display Time
    sns.barplot(y="brand_name", x="total_sec_displayed", data=df, hue="brand_name", palette="Blues_r", order=df.sort_values("total_sec_displayed", ascending=False)["brand_name"], ax=axes[1, 1], legend=False)
    axes[1, 1].set_xlabel("Total Seconds Displayed")
    axes[1, 1].set_ylabel("Brand Name")
    axes[1, 1].set_title("Top Advertisers by Display Time")

    plt.tight_layout()
    #st.pyplot(fig)  # Display plots in Streamlit
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    
    # Use Streamlit's image display function to show it
    st.image(img_stream, caption="Performance Analysis", use_container_width=True)

    plt.close(fig)  # Close the plot to avoid it being rendered multiple times

 
def compare_with_truth_data():
    """Compare detected brand data with truth data and visualize results."""
    if st.session_state.analysis_data is None or st.session_state.truth_data is None:
        st.error("Analysis or truth data missing.")
        return

    # Calculate accuracy
    accuracy = calculate_accuracy(st.session_state.analysis_data, st.session_state.truth_data)
    st.session_state.accuracy = accuracy
    st.success(f"Brand Name Prediction Accuracy: {accuracy:.2f}%")

    # Visualize the advertisement data from analysis
    st.subheader("Advertisement Data Analysis")
    visualize_advertisement_data(st.session_state.analysis_data)


def run_brand_analysis(video_url):
    # Constructing the command to run video_analyzer.py
    command1 = f'python download_video.py {video_url} "data/daily_motion.mp4" '
    command2 = f'python video_analyzer.py "data/daily_motion.mp4" --csv "output/output.csv" --json "output/output.json" '
    try:
        # Run the command using subprocess
        
        subprocess.run(command1, shell=True, check=True, text=True, capture_output=True)
        print("Video Downloaded")
        result = subprocess.run(command2, shell=True, check=True, text=True, capture_output=True)
        print("csv generated")
        
        if os.path.exists("output/output.csv"):
            df = pd.read_csv("output/output.csv")
            st.session_state.analysis_data = df 
            st.success(f"Brand analysis completed successfully:\n{result.stdout}")
            return df
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
            outp_csv = run_brand_analysis(st.session_state.video_url)
            st.session_state.page = "analysis"
            st.rerun()  

elif st.session_state.page == "analysis":
    st.title("Brand Analysis")
    st.subheader("Analysis Data")

    if st.session_state.analysis_data is not None:
        st.table(st.session_state.analysis_data)

        # Button to compare with truth data
        if st.button("Model Performance Analysis"):
            if os.path.exists("data/truth_data.csv"):
                st.session_state.truth_data = pd.read_csv("data/truth_data.csv")  # Load truth data
                compare_with_truth_data()
            else:
                st.error("Ground truth data file not found.")
    else:
        st.warning("No analysis data available. Please go back and run the analysis again.")

    if st.button("Back"):
        st.session_state.processed = False  
        st.session_state.video_url = ""  
        st.session_state.analysis_data = None  # Clear stored analysis data
        st.session_state.truth_data = None  # Clear ground truth data
        st.session_state.accuracy = None  # Clear accuracy results
        st.session_state.page = "home"
        st.rerun()