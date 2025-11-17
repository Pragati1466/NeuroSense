import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

import streamlit as st
if not COHERE_API_KEY or not YOUTUBE_API_KEY:
    st.error("Missing API Keys. Please ensure your .env file contains both COHERE_API_KEY and YOUTUBE_API_KEY.")
    st.stop()

import streamlit as st
import random
import requests
from googleapiclient.discovery import build

# NEW IMPORT FOR ML PREDICTION
from model import train_model, predict_next_mood


if not COHERE_API_KEY or not YOUTUBE_API_KEY:
    st.error("Missing API Keys. Please ensure your .env file contains both COHERE_API_KEY and YOUTUBE_API_KEY.")
    st.stop()
    
st.set_page_config(
    page_title="NeuroSense",
    layout="centered"
)

# CSS styles
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
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    .download-btn:hover {
        background-color:#84C5F4;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Greeting messages 
greeting_messages = [
    "Hi {user_name}! You’re 100% awesome!",
    "Welcome back, {user_name}! Let's make today amazing!",
    "Hi {user_name}, let’s get this day started with some positivity!",
    "Hi {user_name}, you’re like a human version of a hug. What’s the plan for today?",
    "{user_name}, you’re proof that the universe really knows how to craft masterpieces!",
    "Hey {user_name}, if today were a movie, you’d be the star everyone’s rooting for!",
    "Greetings, {user_name}! Remember, you’re like an exclamation point in a world of commas!",
    "Hi {user_name}! Did you know your smile is worth at least 1,000 positive vibes per second?",
    "Hey {user_name}, you’re like a walking serotonin boost. How’s it going?",
    "Hi {user_name}! Let’s make today so amazing that tomorrow gets a little intimidated.",
    "{user_name}, you’re like a four-leaf clover: unique, lucky, and awesome!",
    "Hey there, {user_name}! If today’s a puzzle, you’re the missing piece that makes it perfect.",
    "Hello, {user_name}! You’ve got that ‘main character energy’—let’s make it a great day!",
    "{user_name}, you’re like a playlist of everyone’s favorite songs—always lifting the mood!",
    "Hi {user_name}, if happiness had a mascot, it’d definitely look a lot like you!",
    "Hello, {user_name}! Ready to turn this ordinary day into something extraordinary?",
    "Hi {user_name}, you’re the kind of person who makes good things happen wherever you go!"
]

journal_prompts = [
   "Write about how you're feeling today.",
   "Reflect on a recent decision you made.",
   "Describe your favorite part of the day.",
   "List three things you're grateful for.",
   "Write about a recent challenge you overcame.",
   "Think about something you're looking forward to.",
   "Describe a simple moment that made you smile.",
   "Write about a place that brings you peace.",
   "Think about what you hope for tomorrow.",
   "Write about something that made you feel proud."
]

# Helper functions
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

# Main interface
st.markdown("<div class='title-card'>NeuroSense: Your AI Mood Journal 🌈</div>", unsafe_allow_html=True)

# Sidebar with buttons
with st.sidebar:
    user_name = st.text_input("Enter your name:")
    if user_name:
        if "greeting_displayed" not in st.session_state:
            st.session_state.greeting_displayed = False
        if not st.session_state.greeting_displayed:
            greeting = random.choice(greeting_messages).format(user_name=user_name)
            st.markdown(f"<div class='greeting-card'>{greeting}</div>", unsafe_allow_html=True)
            st.session_state.greeting_displayed = True

        # NAVIGATION BUTTONS
        if st.button("Share your mood here?", key="mood_button"):
            st.session_state.page = "mood"
        if st.button("Music Recommendation", key="music_button"):
            st.session_state.page = "music"
        if st.button("Get your Journal Prompt", key="journal_button"):
            st.session_state.page = "journal"
        # NEW BUTTON FOR ML PREDICTION
        if st.button("Predict Tomorrow's Mood", key="predict_button"):
            st.session_state.page = "predict"

# Default page
if "page" not in st.session_state:
    st.session_state.page = "home"

# HOME PAGE
if st.session_state.page == "home":
    st.markdown("### Welcome to NeuroSense!")
    st.markdown("<div class='instruction-box'>"
                "<p>1. Enter your name to get started.</p>"
                "<p>2. Choose a feature from the sidebar.</p>"
                "<p>3. Enjoy mood tracking, journaling, music recommendations, and mood prediction.</p>"
                "</div>", unsafe_allow_html=True)

# MOOD PAGE
elif st.session_state.page == "mood":
    mood = st.text_area("How are you feeling today? (Share in a paragraph)")
    if st.button("Submit Mood"):
        if mood:
            ai_response = generate_ai_response(mood)
            st.write(f"{ai_response}")
        else:
            st.warning("Please enter your mood.")
    
    suggested_advice = random.choice([
        "Take a peaceful walk for 10 minutes.",
        "Drink some water and stretch a bit.",
        "Listen to calming music.",
        "Write one thing you're grateful for."
    ])
    st.write(f"**Suggestion:** {suggested_advice}")

# MUSIC PAGE
elif st.session_state.page == "music":
    st.markdown("### Music Recommendation")
    emotion = st.selectbox("Select your mood:", ["Happy", "Sad", "Relaxed", "Anger", "Stressed", "Energetic", "Motivated", "Calm"])
    
    if st.button("Get Playlist"):
        playlist = fetch_youtube_playlist(emotion)
        if playlist:
            st.markdown(f"**{playlist['title']}**")
            st.markdown(f"<a href='{playlist['url']}' target='_blank' class='download-btn'>Open Playlist</a>", unsafe_allow_html=True)
        else:
            st.warning("No playlist found for your mood.")

# JOURNAL PAGE
elif st.session_state.page == "journal":
    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = random.choice(journal_prompts)
    
    prompt = st.session_state.current_prompt
    st.markdown(f"### Your Journal Prompt: {prompt}")
    
    journal_entry = st.text_area("Write your response:")
    
    if st.button("Download Journal"):
        if journal_entry.strip():
            file_content = f"Journal Prompt: {prompt}\n\nYour Entry:\n{journal_entry}"
            st.download_button("Download as Text File", file_content, file_name="journal.txt")
            st.success("Thanks for expressing yourself! 🌟")
        else:
            st.warning("Please write your response before downloading.")

# NEW: PREDICT TOMORROW’S MOOD (ML MODEL)
elif st.session_state.page == "predict":
    st.markdown("### Predict Tomorrow's Mood")

    sleep = st.slider("Hours slept today", 0, 12, 7)
    steps = st.number_input("Steps walked today", min_value=0, value=3000)
    meditated = st.checkbox("Meditated today?")
    journaled = st.checkbox("Journaled today?")

    if st.button("Predict Mood"):
        try:
            model = train_model()
            prediction = predict_next_mood(
                model,
                sleep,
                steps,
                int(meditated),
                int(journaled)
            )
            st.success(f"Your predicted mood for tomorrow: **{prediction} / 10** 🌟")
        except Exception as e:
            st.error(f"Error: {e}")
