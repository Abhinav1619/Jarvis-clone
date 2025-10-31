# jarvis_simple.py
import os
import time
import speech_recognition as sr
import pyttsx3
import openai

# load key from environment
openai.api_key = os.getenv("Osk-proj-b32wYxXhHByb01lusUJvpFo8V2VTYybGkY8LbGArUh2UHzGa4jnq82tj4y9ejZqzG0_Oz5GZkBT3BlbkFJbd1QqEKd30bYhB3FECTXBGan-4BxhFyJwQnxiKTmBUrg52wFb0RwVbclsJCD457SaV2Nsoc-sA")

# init speech modules
recognizer = sr.Recognizer()
mic = sr.Microphone()   # uses default system microphone
tts = pyttsx3.init()
tts.setProperty('rate', 170)  # speech speed

def speak(text):
    tts.say(text)
    tts.runAndWait()

def ask_openai(prompt):
    # simple chat call
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",   # if unavailable, change to a model you have
        messages=[{"role":"user","content":prompt}],
        max_tokens=200
    )
    return resp['choices'][0]['message']['content'].strip()

def listen_once(timeout=6, phrase_time_limit=8):
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.6)
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)  # quick cloud fallback STT
        return text
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        print("STT error:", e)
        return None

def main_loop():
    print("Say 'exit' to quit.")
    while True:
        user_text = listen_once()
        if not user_text:
            print("I didn't hear anything. Try again.")
            continue
        print("You said:", user_text)
        if user_text.strip().lower() in ("exit", "quit", "bye"):
            speak("Goodbye.")
            break
        # send to LLM
        reply = ask_openai("You are Jarvis, a helpful assistant. Keep replies short.\nUser: " + user_text)
        print("Jarvis:", reply)
        speak(reply)
        time.sleep(0.2)

if __name__ == "__main__":
    main_loop()
