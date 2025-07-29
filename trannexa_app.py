import sounddevice as sd
import wavio
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import pyttsx3
from langdetect import detect
import pycountry
import os


engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice


def speak(text):
    engine.say(text)
    engine.runAndWait()



def record_audio(filename="input.wav", duration=5, fs=44100):
    speak("Recording started. Please speak now.")
    print(" Recording... Please speak.")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write(filename, audio, fs, sampwidth=2)
    print(f" Recording saved to '{filename}'.")


def transcribe_audio(filename):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio = r.record(source)
        text = r.recognize_google(audio)
        print(" Transcription:", text)
        return text
    except sr.UnknownValueError:
        print(" Could not understand audio.")
        return ""
    except sr.RequestError:
        print(" Could not connect to Google's servers.")
        return ""
    
def getLangName(lang_code):
    try:
        return pycountry.languages.get(alpha_2=lang_code).name
    except:
        return lang_code

# languages
language_code_map = {
    'english': 'en',
    'hindi': 'hi',
    'nepali': 'ne',
    'french': 'fr',
    'spanish': 'es',
    'german': 'de',
    'bengali': 'bn',
    'marathi': 'mr',
    'tamil': 'ta',
    'telugu': 'te',
    'malayalam': 'ml',
    'punjabi': 'pa',
    'japanese': 'ja',
    'chinese': 'zh-cn',
    'korean': 'ko',
    'arabic': 'ar',
    'russian': 'ru',
}

# 🚀 Main function
def main():
    print("This is TranNexa, your AI-Powered Language Translator")
    speak("This is Tran Nexa, your A I powered language translator")

    record_audio("input.wav", duration=5)
    input_text = transcribe_audio("input.wav")

    if not input_text:
        speak("Sorry, I could not understand your voice.")
        return


    detected_lang = detect(input_text)
    detected_lang_name = getLangName(detected_lang)
    print(f" Detected Language: {detected_lang_name}")


    speak("Which language should I translate to?")
    record_audio("lang.wav", duration=3)
    to_lang_input = transcribe_audio("lang.wav").lower()

    if to_lang_input not in language_code_map:
        speak("Sorry, I don't support that language yet.")
        return

    target_lang_code = language_code_map[to_lang_input]


    translated_text = GoogleTranslator(source='auto', target=target_lang_code).translate(input_text)
    print(" Translated:", translated_text)
    speak("Here is your translation.")
    speak(translated_text)


    try:
        tts = gTTS(translated_text, lang=target_lang_code)
        tts.save("output.mp3")
        os.system("start output.mp3")  
    except Exception as e:
        print("❌ TTS failed:", e)

if __name__ == "__main__":
    main()  