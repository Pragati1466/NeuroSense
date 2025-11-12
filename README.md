# NeuroSense 


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

### API Keys (Choose one option for each)

#### 1. AI Responses (Choose one):
- **Option A: Cohere API** (Recommended)
  - Get a free API key from [Cohere](https://cohere.com/)
  - Free tier available with limited requests

- **Option B: OpenAI API** (Alternative)
  - Get a free API key from [OpenAI](https://platform.openai.com/)
  - Free credits available for new users

#### 2. Music Recommendations (Choose one):
- **Option A: YouTube Data API v3** (Recommended)
  - Enable YouTube Data API v3 in [Google Cloud Console](https://console.cloud.google.com/)
  - Free tier provides 10,000 units/day (1 search ≈ 100 units)

- **Option B: JioSaavn API** (Alternative, no key required)
  - Free and open-source
  - No API key needed
  - Limited to Indian music content

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
   Create a `.env` file in the `NeuroSense` directory with your preferred API keys:
   ```
   # Choose one AI provider
   COHERE_API_KEY=your_cohere_api_key_here  # For Cohere AI
   # OPENAI_API_KEY=your_openai_api_key_here  # Uncomment for OpenAI
   
   # Choose one music provider
   YOUTUBE_API_KEY=your_youtube_api_key_here  # For YouTube
   # JIOSAAVN_ENABLED=True  # Uncomment to use JioSaavn (no API key needed)
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
- [OpenAI](https://openai.com/) as an alternative AI provider
- [YouTube Data API](https://developers.google.com/youtube/v3) for music recommendations
- [JioSaavn](https://www.jiosaavn.com/) as a music recommendation alternative
- All contributors who have helped shape this project

## 🌟 Support

If you find this project helpful, please consider giving it a ⭐️ on GitHub!


