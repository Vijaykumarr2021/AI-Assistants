import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import openai
from config import OPENAI_API_KEY  # Your API key stored safely

# ✅ Initialize TTS engine
engine = pyttsx3.init()

# ✅ Set up voice (e.g., Lekha for Hindi, or female English)
voices = engine.getProperty('voices')
for voice in voices:
    if "Lekha" in voice.name:  # Change "Lekha" if needed
        engine.setProperty('voice', voice.id)
        break  # Stop after setting the first match

# ✅ Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def speak(text):
    print(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your AI assistant. How can I help you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language='en-in')  # You can change language
        print(f"👤 You said: {query}")
    except Exception:
        speak("Sorry, could you say that again?")
        return "None"
    return query.lower()

def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful and smart assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print(e)
        return "Sorry, I couldn't connect to OpenAI right now."

def run_assistant():
    wish_user()
    while True:
        query = take_command()

        if query == "none":
            continue

        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://google.com")

        elif 'time' in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {time}")

        elif 'exit' in query or 'stop' in query:
            speak("Goodbye, see you soon!")
            break

        else:
            speak("Thinking...")
            answer = ask_openai(query)
            speak(answer)

if __name__ == "__main__":
    run_assistant()
g