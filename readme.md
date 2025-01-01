# J.A.R.V.I.S

Jarvis is a personal assistant script that can perform various tasks such as playing music, searching the web, sending messages, and more.

## Features

- Voice commands for various tasks
- control music on Spotify
- search gemini
- search wikipedia
- Search the web using Google and YouTube
- Send WhatsApp messages
- Fetch weather information
- Add and speak tasks from a to-do list
- Open applications and websites

## Requirements

- Stable Internet Connection.
- Spotify Premium
- Python 3.7+
- Required Python packages:
  - pyttsx3
  - speech_recognition
  - webbrowser
  - datetime
  - plyer
  - pyautogui
  - wikipedia
  - pywhatkit
  - spotipy
  - fuzzywuzzy
  - python-dotenv
  - requests
  - pycaw
  - comtypes

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/prakashdebroy/JARVIS.git
    cd jarvis
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add the following API key:
    ```env
    gemini_key = YOUR_GEMINI_API_KEY
    spotify_id = YOUR_SPOTIFY_ID
    spotify_secret = YOUR_SPOTIFY_SECRET
    open_weather_key = YOUR_OPEN_WEATHER_API_KEY
    ```

## Commands

- SAY JARVIS [commands]

- Spotify
    - "play hindi songs"
    - "play english songs"
    - "play japanese songs"
    - "play music"
    - "next song" or "skip"
    - "previous song" or "go back"
    - "pause" or "stop"
    - "resume" or "start"

- Random Number: 
    - "choose a number between [start] [finish]"

- Asking Time:
    - "What is the time?"
    - "What's the time?"

- Asking Date
    - "What is the date?"
    - "What's the date?"

- Search on Wikipedia:
    - "Wikipedia [topic]" (e.g., "Wikipedia Python programming")

- General questions to search using gemini:
    - "What [is] [question]?"
    - "Where [is] [place]?"
    - "When [did] [event] happen?"
    - "Explain [topic]."
    - "How [to] [action]?"
    - "Can I [action]?"

- Open and search on YouTube:
    - "Open YouTube and search [topic]"

- Search on Google:
    - "Search [query]"

- Email:
    - "Send Email"

- Whats app
    - "open whats app in browser"
    - "open whats app in chrome"
    - "open whats app"

- Task Manupulation:
    - "New Task [Task]"
    - "Speak Task"
    - "Show Work"

- Greeting and weather:
    - "Good morning"
    - "Good afternoon"
    - "Good evening"
    - "Hello"

- What is JARVIS?:
    - "Who are you?"

- Ending:
    - "Thank You"
    - "Thanks"
    - "Goodbye"
    - "Exit"

## Usage

Run the script:
```sh
python main.py