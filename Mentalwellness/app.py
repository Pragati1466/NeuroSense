from dotenv import load_dotenv
import os
import streamlit as st
import random
import requests
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import base64

load_dotenv() 

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not COHERE_API_KEY or not YOUTUBE_API_KEY:
    st.error("Missing API Keys. Please ensure your .env file contains both COHERE_API_KEY and YOUTUBE_API_KEY.")
    st.stop()
    
st.set_page_config(
    page_title="NeuroSense",
    layout="centered"
)

# --- INITIALIZE SESSION STATE FOR DATA HISTORY ---
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []
if "journal_history" not in st.session_state:
    st.session_state.journal_history = []

# --- CSS STYLES ---
st.markdown("""
    <style>
    .greeting-card {
        padding: 16px;
        background-color: #D6C8FF;
        border-radius: 20px;
        font-size: 20px;
        color: #4B145B;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    .instruction-box {
        background-color: #CDC1FF;
        padding: 15px;
        border-radius: 10px;
        color: #56021F;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .title-card {
        background-color: #A1E3F9;
        padding: 20px;
        border-radius: 15px;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        color: black;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .download-btn {
        background-color: #AEE4F8;
        color: #0D3B66;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        text-decoration: none;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    .download-btn:hover {
        background-color:#84C5F4;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def generate_ai_response(user_input):
    url = "https://api.cohere.ai/v1/generate"
    headers = {"Authorization": f"Bearer {COHERE_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "command-r-plus",
        "prompt": f"User feels: {user_input}. Respond with empathy in 3-4 sentences.",
        "max_tokens": 300,
        "temperature": 0.7
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get('generations', [{}])[0].get('text', '').strip()
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def fetch_youtube_playlist(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    response = youtube.search().list(part="snippet", q=f"{query} music playlist", type="playlist", maxResults=1).execute()
    items = response.get("items", [])
    if items:
        playlist_id = items[0]["id"]["playlistId"]
        title = items[0]["snippet"]["title"]
        return {"title": title, "url": f"https://www.youtube.com/playlist?list={playlist_id}"}
    return None

def generate_pdf(data, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)
    
    for entry in data:
        for key, value in entry.items():
            # Clean text to handle basic unicode issues in standard FPDF
            clean_text = str(value).encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, f"{key.capitalize()}: {clean_text}")
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
    
    return pdf.output(dest='S').encode('latin-1')

# Greeting messages 
greeting_messages = [
     "Hi {user_name}! You’re 100% awesome!",
    "Welcome back, {user_name}! Let's make today amazing!",
    "Hi {user_name}, let’s get this day started with some positivity!",
] 
# (Kept short for brevity, add your full list back here)

journal_prompts = [
   "Write about how you're feeling today.",
    "Reflect on a recent decision you made.",
    "Describe your favorite part of the day.",
]
# (Kept short for brevity, add your full list back here)


# --- MAIN INTERFACE ---
st.markdown("<div class='title-card'>NeuroSense: Your AI Mood Journal 🌈</div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    user_name = st.text_input("Enter your name:")
    if user_name:
        if "greeting_displayed" not in st.session_state:
            st.session_state.greeting_displayed = False
        if not st.session_state.greeting_displayed:
            greeting = random.choice(greeting_messages).format(user_name=user_name)
            st.markdown(f"<div class='greeting-card'>{greeting}</div>", unsafe_allow_html=True)
            st.session_state.greeting_displayed = True

        st.markdown('<div class="sidebar-buttons-container">', unsafe_allow_html=True)
        if st.button("Share your mood here?", key="mood_button"):
            st.session_state.page = "mood"
        if st.button(" Music Recommendation", key="music_button"):
            st.session_state.page = "music"
        if st.button("Get your Journal Prompt", key="journal_button"):
            st.session_state.page = "journal"
        if st.button("💾 Data & Settings", key="data_button"):
            st.session_state.page = "data"
        st.markdown('</div>', unsafe_allow_html=True)

# Navigation Logic
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.markdown("### Welcome to NeuroSense!")
    st.markdown("<div class='instruction-box'>"
                "<p>1. Enter your name to get started.</p>"
                "<p>2. Choose a feature from the sidebar.</p>"
                "<p>3. Use 'Data & Settings' to save or restore your journey.</p>"
                "</div>", unsafe_allow_html=True)

elif st.session_state.page == "mood":
    mood = st.text_area("How are you feeling today?(Share in paragraph)")
    if st.button("Submit Mood"):
        if mood:
            ai_response = generate_ai_response(mood)
            st.write(f" {ai_response}")
            
            # Advice logic
            suggested_advice = random.choice([
                "Spend a few minutes today savoring a cup of tea or coffee mindfully.",
                "Write down one thing you're proud of achieving this week.",
                "Take a walk in nature and appreciate the beauty around you."
            ])
            st.write(f"**Suggestion:** {suggested_advice}")

            # SAVE TO HISTORY
            entry = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Mood": mood,
                "AI Response": ai_response,
                "Advice": suggested_advice
            }
            st.session_state.mood_history.append(entry)
            st.success("Mood logged to history! Go to 'Data & Settings' to export.")
            
        else:
            st.warning("Please enter your mood.")

elif st.session_state.page == "music":
    st.markdown("### Music Recommendation")
    st.markdown("<h5 style='text-align: center; color: gray;'>When your mood meets the perfect playlist. Enjoy the vibe!</h5>", unsafe_allow_html=True)
    emotion = st.selectbox("Select your mood:", ["Happy", "Sad", "Relaxed","Anger","Stressed", "Energetic", "Motivated", "Calm"])
    if st.button("Get Playlist"):
        playlist = fetch_youtube_playlist(emotion)
        if playlist:
            st.markdown(f"**{playlist['title']}**")
            st.markdown(f"<a href='{playlist['url']}' target='_blank' class='download-btn'>Open Playlist</a>", unsafe_allow_html=True)
        else:
            st.warning("No playlist found for your mood.")

elif st.session_state.page == "journal":
    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = random.choice(journal_prompts)
    prompt = st.session_state.current_prompt
    st.markdown(f"### Your Journal Prompt: {prompt}")
    journal_entry = st.text_area("Write your response:")
    
    if st.button("Save Entry"):
        if journal_entry.strip():
            # SAVE TO HISTORY
            entry = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Prompt": prompt,
                "Entry": journal_entry
            }
            st.session_state.journal_history.append(entry)
            st.success("Entry saved to memory! Go to 'Data & Settings' to export.")
            st.session_state.current_prompt = random.choice(journal_prompts) # New prompt for next time
        else:
            st.warning("Please write your response before saving.")

elif st.session_state.page == "data":
    st.markdown("### 💾 Data Management")
    st.info("Export your data to keep a permanent record, or restore previous data from a CSV file.")

    tab1, tab2 = st.tabs(["⬇️ Export Data", "⬆️ Import Data"])

    with tab1:
        st.subheader("Export to CSV")
        col1, col2 = st.columns(2)
        
        # Export Moods CSV
        if st.session_state.mood_history:
            df_mood = pd.DataFrame(st.session_state.mood_history)
            csv_mood = df_mood.to_csv(index=False).encode('utf-8')
            col1.download_button("Download Mood History (CSV)", csv_mood, "my_moods.csv", "text/csv")
        else:
            col1.write("No mood data available.")

        # Export Journal CSV
        if st.session_state.journal_history:
            df_journal = pd.DataFrame(st.session_state.journal_history)
            csv_journal = df_journal.to_csv(index=False).encode('utf-8')
            col2.download_button("Download Journal History (CSV)", csv_journal, "my_journal.csv", "text/csv")
        else:
            col2.write("No journal data available.")

        st.markdown("---")
        st.subheader("Export to PDF")
        
        if st.button("Generate PDF Report"):
            if not st.session_state.mood_history and not st.session_state.journal_history:
                st.error("No data to generate PDF.")
            else:
                # Combine data for PDF
                all_data = st.session_state.mood_history + st.session_state.journal_history
                # Sort by date (assuming Date key exists in all)
                all_data.sort(key=lambda x: x['Date'], reverse=True)
                
                pdf_bytes = generate_pdf(all_data, "NeuroSense Journey Report")
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_bytes,
                    file_name="neurosense_report.pdf",
                    mime="application/pdf"
                )

    with tab2:
        st.subheader("Restore from CSV")
        st.warning("Note: Importing will merge with your current session data.")
        
        upload_type = st.radio("Select data type to import:", ["Mood History", "Journal History"])
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        
        if uploaded_file is not None:
            try:
                df_uploaded = pd.read_csv(uploaded_file)
                data_dict = df_uploaded.to_dict('records')
                
                if st.button("Confirm Import"):
                    if upload_type == "Mood History":
                        st.session_state.mood_history.extend(data_dict)
                        st.success(f"Imported {len(data_dict)} mood entries successfully!")
                    else:
                        st.session_state.journal_history.extend(data_dict)
                        st.success(f"Imported {len(data_dict)} journal entries successfully!")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")