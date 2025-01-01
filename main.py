import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit as pwk
import gemini_req as gem
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fuzzywuzzy import fuzz
from dotenv import load_dotenv
import os
import ctypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import requests
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

load_dotenv()

open_weather_api_key = os.getenv("open_weather_key")
LOCATION = "Agartala, IN"

SPOTIFY_CLIENT_ID = os.getenv("spotify_id")
SPOTIFY_CLIENT_SECRET = os.getenv("spotify_secret") 

SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
scope="playlist-read-private playlist-read-collaborative user-read-playback-state user-modify-playback-state"
PLAYLIST_URI = "spotify:playlist:29TNuukPv8tNq4bqkSVA1X?si=e1a562c80a5d40b2"  

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope))

def get_active_device():
    devices = sp.devices()
    for device in devices['devices']:
        if device['is_active']:
            return device['id']
    return None

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def command():
    content = ""
    while content == "":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            content = r.recognize_google(audio, language="en-in")
            print("You said: " + content)
        except:
            pass
        
    
    return content.lower()

def date():
    today = datetime.date.today()
    day = today.day
    if 10 <= day % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    formatted_date = today.strftime(f"Today is {day}{suffix} %B %Y")
    speak(formatted_date)

def get_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={open_weather_api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return temp, description
    else:
        speak(f"Error: Unable to fetch weather data. HTTP Status Code: {response.status_code}")
        speak(f"Response: {response.text}")
        return None

def increase_volume(step=0.1):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    current_volume = volume.GetMasterVolumeLevelScalar()

    new_volume = min(current_volume + step, 1.0)  
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def decrease_volume(step=0.1):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    current_volume = volume.GetMasterVolumeLevelScalar()

    new_volume = min(current_volume - step, 1.0)  
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def search_spotify(query):
    try:
        results = sp.search(q=query, type="track", limit=10)
        
        if results['tracks']['items']:
            best_match = None
            best_score = 0

            for track in results['tracks']['items']:
                track_name = track['name'].lower()
                artist_name = track['artists'][0]['name'].lower()
                combined_name = f"{track_name} {artist_name}"
                
                match_score = fuzz.partial_ratio(query.lower(), combined_name)
                
                if match_score > best_score: 
                    best_score = match_score
                    best_match = track
            
            if best_match:
                return best_match['name'], best_match['artists'][0]['name'], best_match['uri']
        else:
            return None, None, None
    except Exception as e:
        print(f"Error during Spotify search: {e}")
        return None, None, None

def random_number(max, min):
    return random.randint(min, max)

def play_spotify_track(track_uri):
    try:
        playback_info = sp.current_playback()
        if playback_info and playback_info['device']:
            sp.start_playback(uris=[track_uri])
        else:
            pyautogui.press("super")
            pyautogui.typewrite("spotify")
            pyautogui.sleep(0.5)
            pyautogui.press("enter")
            pyautogui.sleep(7)
            pyautogui.press("space")
            pyautogui.sleep(1)
            pyautogui.press("space")
            sp.start_playback(uris=[track_uri])
            speak("Playing on Spotify.")
    except Exception as e:
        print(f"Error during playback: {e}")
        speak("There was an issue playing the track.")

def next_song():
    try:
        playback_info = sp.current_playback()
        if playback_info and playback_info['device']:
            sp.next_track()
            speak("Skipping to the next song.")
        else:
            speak("No active device found. Please play a song first.")
    except Exception as e:
        print(f"Error while skipping to the next song: {e}")
        speak("There was an error while trying to skip to the next song.")

def previous_song():
    try:
        playback_info = sp.current_playback()
        if playback_info and playback_info['device']:
            sp.previous_track()
            speak("Going back to the previous song.")
        else:
            speak("No active device found. Please play a song first.")
    except Exception as e:
        print(f"Error while going to the previous song: {e}")
        speak("There was an error while trying to go to the previous song.")

def pause_song():
    try:
        playback_info = sp.current_playback()
        if playback_info and playback_info['device']:
            sp.pause_playback()
            pyautogui.sleep(1)
            speak("paused the current song.")

        else:
            speak("No active device found. Please play a song first.")
    except Exception as e:
        print(f"Error while pausing the  song: {e}")
        speak("There was an error while trying to pause the song.")

def resume_song():
    try:
        playback_info = sp.current_playback()
        if playback_info and playback_info['device']:
            speak("resumed the current song.")
            pyautogui.sleep(1)
            sp.start_playback()

        else:
            speak("No active device found. Please play a song first.")
    except Exception as e:
        print(f"Error while resuming the  song: {e}")
        speak("There was an error while trying to resume the song.")

def play_random_song_lang(language, lang_name):
    try:
        device_id = get_active_device()
        if device_id:
            speak("playing" + lang_name + " music")
            sp.shuffle(True, device_id=device_id)
            pyautogui.sleep(1) 
            sp.start_playback(device_id=device_id, context_uri=language)
        else:
            speak("No active device found. opening Spotify.")
            pyautogui.press("super")
            pyautogui.sleep(0.25)
            pyautogui.typewrite("spotify")
            pyautogui.sleep(0.25)
            pyautogui.press("enter")
            pyautogui.sleep(7)
            pyautogui.press("space")
            pyautogui.sleep(1)
            pyautogui.press("space")
            sp.start_playback(device_id=device_id, context_uri=language)
            speak("Playing a random song from the playlist.")
    except Exception as e:
        print(f"Error while fetching or playing a random song from the playlist: {e}")
        speak("An error occurred while trying to play a random song from the playlist.")

def play_random_song():
    language = random.choice(["spotify:playlist:7o2p15uxjCKDZeTTdjkXlX?si=915335c3dbc042a7",
                              "spotify:playlist:7wE4LYM8DtFy81QhFnWSbn?si=9413ccd0eaf244a1",
                              "spotify:playlist:6ODBI3nPGKtWgzhnocRaqF?si=8f9b19e35c3349de"])
    try:
        device_id = get_active_device()
        if device_id:
            speak("playing music")
            sp.shuffle(True, device_id=device_id)          
            pyautogui.sleep(1) 
            sp.start_playback(device_id=device_id, context_uri=language)
        else:
            speak("No active device found. opening Spotify.")
            pyautogui.press("super")
            pyautogui.sleep(0.25)
            pyautogui.typewrite("spotify")
            pyautogui.sleep(0.25)
            pyautogui.press("enter")
            pyautogui.sleep(7)
            pyautogui.press("space")
            pyautogui.sleep(1)
            pyautogui.press("space")
            sp.start_playback(device_id=device_id, context_uri=language)
            speak("Playing a random song from the playlist.")
    except Exception as e:
        print(f"Error while fetching or playing a random song from the playlist: {e}")
        speak("An error occurred while trying to play a random song from the playlist.")

def code_red():
    ctypes.windll.user32.LockWorkStation()

def main_process():
    pyautogui.sleep(0.5)
    speak("Systems are now fully operational")
    while True:
        print("\nListening for 'Jarvis' to activate...")
        request = command()

        if "jarvis" in request:
            request = request.replace("jarvis", "")
            request = request.strip()

            if "code red" in request:
                speak("Code Red activated.")
                code_red()
                break

            elif "open whatsapp in browser" in request or "open whatsapp in chrome" in request:
                speak("Opening WhatsApp in Chrome")
                webbrowser.open("https://web.whatsapp.com/")

            elif "increase volume" in request:
                speak("increasing volume")
                increase_volume()

            elif "decrease volume" in request:
                speak("decreasing volume")
                decrease_volume()

            elif "play hindi songs" in request or "play hindi song" in request:
                language = "spotify:playlist:7o2p15uxjCKDZeTTdjkXlX?si=915335c3dbc042a7"
                play_random_song_lang(language, "Hindi")
            
            elif "play english songs" in request or "play english song" in request:
                language = "spotify:playlist:7wE4LYM8DtFy81QhFnWSbn?si=9413ccd0eaf244a1"
                play_random_song_lang(language, "English")
            
            elif "play japanese songs" in request or "play japanese song" in request:
                    language = "spotify:playlist:6ODBI3nPGKtWgzhnocRaqF?si=8f9b19e35c3349de"
                    play_random_song_lang(language, "Japanese")
            
            elif "play music" in request:
                play_random_song()
      
            elif "play" in request:
                song_name = request.replace("play", "").strip()
                if song_name:
                    speak(f"Searching Spotify for {song_name}")
                    track_name, artist_name, track_uri = search_spotify(song_name)
                    if track_uri:
                        speak(f"Playing {track_name} by {artist_name}")
                        play_spotify_track(track_uri)
                    else:
                        speak("Couldn't find the song on Spotify.")
            
            elif "next song" in request or "skip" in request:
                next_song()
            elif "previous song" in request or "go back" in request:
                previous_song()
            elif "pause" in request or "stop" in request:
                pause_song()
            elif "resume" in request or "start" in request:
                resume_song()
            
            elif "choose a number between" in request:
                try:
                    numbers = request.replace("choose a number between", "").strip()
                    min_num, max_num = numbers.split(" and ")
                    speak("The number is " + str(random_number(int(max_num), int(min_num))))
                except:
                    speak("Invalid input. Please try again.")

            elif "what is the time" in request or "what's the time" in request:
                now_time = datetime.datetime.now().strftime("%I:%M %p")
                speak("Current time is " + str(now_time))

            elif "what is the date" in request or "what's the date" in request:
                date()

            elif "wikipedia" in request:
                request = request.replace("search", "").replace("wikipedia", "").strip()
                print(request)
                result = wikipedia.summary(request, sentences=1)
                print(result)
                speak(result)
            
            elif "what" in request or "where" in request or "when" in request or "explain" in request or "how" in request or "can i" in request:
                request = request + " in less than 40 words"
                response = gem.send_request(request)
                print(response)
                speak(response)
            
            elif "open youtube and search" in request:
                search_yt = request.replace("open youtube and search", "").strip("+")
                if search_yt != "":
                    speak("Opening YouTube")
                    webbrowser.open("https://www.youtube.com/results?search_query=" + search_yt.lower())          
            elif "open youtube" in request:
                speak("Opening YouTube")
                webbrowser.open("https://youtube.com/")
            
            elif "search" in request:
                srh = request.replace("search", "").strip()
                if srh != "":
                    speak("Searching...")
                    webbrowser.open("https://www.google.com/search?q=" + srh.lower())
            
            # elif "send whatsapp" in request:
            #     speak("Sending WhatsApp message")
            #     pwk.sendwhatmsg("+910000000000", "Hello", datetime.now().hour, datetime.now().minute + 1,)
            #     speak("Message sent")
            
            elif "send email" in request:
                speak("opening gmail")
                webbrowser.open("https://mail.google.com/mail/u/0/#inbox?compose=new")

            elif "new task" in request:
                task = request.replace("new task", "").strip()
                if task != "":
                    speak("Adding task: " + task)
                    with open("todo.txt", "a") as file:
                        file.write(task + "\n")
            
            elif "speak task" in request:
                with open("todo.txt", "r") as file:
                    speak("Work we have to do today is: " + file.read())          
            
            elif "show work" in request:
                with open("todo.txt", "r") as file:
                    tasks = file.read()
                    notification.notify(
                        title="Today's Work",
                        message=tasks
                    )
            
            elif "open" in request:
                query = request.replace("open", "").strip()
                speak("Opening " + query)
                pyautogui.press("super")
                pyautogui.typewrite(query)
                pyautogui.sleep(1)
                pyautogui.press("enter")

            
            elif "hello" in request:
                speak("Welcome back sir, how may I help you today?")

            elif "good morning" in request:
                temp, description = get_weather(LOCATION)
                now = datetime.datetime.now()
                current_time = now.strftime("%I:%M %p")

                message = (
                    f"Good morning sir. It's {current_time}. "
                    f"The weather in Agartala is {temp:.1f} degrees Celsius with {description}.")
                speak(message)
            elif "good afternoon" in request:
                temp, description = get_weather(LOCATION)
                now = datetime.datetime.now()
                current_time = now.strftime("%I:%M %p")

                message = (
                    f"Good afternoon sir. It's {current_time}. "
                    f"The weather in Agartala is {temp:.1f} degrees Celsius with {description}.")
                speak(message)
            elif "good evening" in request:
                temp, description = get_weather(LOCATION)
                now = datetime.datetime.now()
                current_time = now.strftime("%I:%M %p")

                message = (
                    f"Good evening sir. It's {current_time}. "
                    f"The weather in Agartala is {temp:.1f} degrees Celsius with {description}.")
                speak(message)

            elif "who are you" in request:
                speak("I am JARVIS, a rather intelligent system designed to assist Mr. Deb roy in all matters.")

            elif "thank you" in request or "thanks" in request or "thank" in request:
                speak("My pleasure sir!")
                break

            elif "exit" in request or "good bye" in request or "goodbye" in request:
                speak("Goodbye!")
                break

main_process()
