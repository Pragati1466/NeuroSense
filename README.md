# NeuroSense 🌈

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://neuro-sense.streamlit.app/)

An AI-powered mood journaling and wellness assistant that helps you track your emotions, get personalized music recommendations, and maintain a reflective journal - all in one place. Built with ❤️ using Streamlit.

## ✨ Features

- **Mood Tracking** - Share your daily mood and receive empathetic AI responses
- **Music Recommendations** - Get curated YouTube playlists based on your current emotional state
- **Guided Journaling** - Thoughtful prompts to help with self-reflection
- **Downloadable Journal** - Save your journal entries for personal records
- **Personalized Experience** - Custom greetings and suggestions based on your input

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Cohere API key (for AI responses)
- YouTube Data API v3 key (for music recommendations)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/NeuroSense.git
   cd NeuroSense/NeuroSense
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the `NeuroSense` directory with your API keys:
   ```
   COHERE_API_KEY=your_cohere_api_key_here
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

5. **Run the app**
   ```bash
   streamlit run Mentalwellness/app.py
   ```

## 🎯 Features in Detail

### Mood Tracking
- Share how you're feeling in natural language
- Receive empathetic, AI-generated responses
- Get personalized suggestions based on your mood

### Music Recommendations
- Select your current emotional state
- Get curated YouTube playlists matching your mood
- Directly open playlists in YouTube

### Journaling
- Get daily writing prompts
- Save your journal entries
- Download entries as text files

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [Cohere](https://cohere.com/) for the AI text generation
- [YouTube Data API](https://developers.google.com/youtube/v3) for music recommendations
- All contributors who have helped shape this project

## 🌟 Support

If you find this project helpful, please consider giving it a ⭐️ on GitHub!

---
Built with ❤️ by Pragati
