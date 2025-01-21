import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from groq import Groq

# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# API keys
newsapi = "6507691e062b4ee79c94838ce065eae7"

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    try:
        client = Groq(api_key="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")  # Ensure the API key is valid
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Ensure this model is available
            messages=[{"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
                      {"role": "user", "content": command}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"AI processing error: {e}")
        return "Sorry, I couldn't process that command right now."


def processcommand(command):
    """Process the given voice command."""
    print(f"Command received: {command}")
    
    # Open specific websites based on command
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        try:
            link = musicLibrary.music[song]
            webbrowser.open(link)
        except KeyError:
            speak(f"Sorry, I couldn't find the song {song}.")
    elif "tell me news" in command.lower():
        try:
            # Send request to NewsAPI
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            print("Response status code:", response.status_code)  # Debugging
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                if articles:
                    speak("Here are the top news headlines:")
                    for article in articles[:5]:  # Limit to top 5 headlines
                        title = article.get('title', 'No title available')
                        speak(title)
                else:
                    speak("Sorry, I couldn't find any news articles.")
            else:
                error_message = response.json().get('message', 'Unknown error')
                speak(f"Sorry, there was an issue fetching the news: {error_message}")
                print(f"Error: {error_message}")  # Debugging
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            speak("Sorry, I encountered a network error while fetching the news.")
    else:
        # Let OpenAI handle the request if no specific command was matched
        output = aiProcess(command)
        speak(output)


# Main loop
if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word 'Jarvis'...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Yes?")
                    print("Jarvis activated...")
                    with sr.Microphone() as source:
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        command = recognizer.recognize_google(audio)
                        processcommand(command)
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

