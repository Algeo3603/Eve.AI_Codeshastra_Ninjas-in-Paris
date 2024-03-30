from openai import OpenAI
import openai
import os
from pathlib import Path
from dotenv import load_dotenv,find_dotenv
import textwrap
import google.generativeai as genai
import pyaudio
import wave
import speech_recognition as sr
import wave

load_dotenv()
# load_dotenv(find_dotenv())
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
GEMINI_API = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel('gemini-pro')
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

client = OpenAI(api_key=OPENAI_API_KEY)
def speak(answer):
 response = client.audio.speech.create(
     model="tts-1",
     voice="alloy",
     input=answer,
 )
 response.stream_to_file("output.mp3")

def hear():
 audio_file= open("output.mp3", "rb")
 transcription = client.audio.transcriptions.create(
   model="whisper-1", 
   file=audio_file
 )
 return transcription.text

def process_text(text):
    response = model.generate_content(f"You are an ai assistant that is supposed to behave like ones friend, try to give me a reply to the following query from the user using types of slang that would make you seem like a friend instead of a machine    {text} ")
    return response.text

keyword = "assistant"
r = sr.Recognizer()
def listen_for_keyword():
    with sr.Microphone() as source:
        print("Listening for keyword...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        if keyword in text.lower():
            print("Keyword detected!")
            return True
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Error from Google Speech Recognition service: {e}")

    return False


def record_audio():
    print("Recording audio...")
    chunk = 1024
    audio_frames = []
    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=chunk
    )

    while True:
        data = stream.read(chunk)
        audio_frames.append(data)
        if len(data) == 0:
            break

    stream.stop_stream()
    stream.close()

    audio_data = b''.join(audio_frames)
    return audio_data

def save_as_mp3(audio_data, filename):
    with open("temp.wav", "wb") as f:
        f.write(audio_data)

    wf = wave.open("temp.wav", "rb")
    p = pyaudio.PyAudio()

    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True
    )

    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()
    p.terminate()

    os.remove("temp.wav")  # Remove the temporary WAV file

    audio = openai.Audio.create(
        file="temp.wav",
        model="whisper-1",
        response_format="mp3"
    )

    with open(filename, "wb") as f:
        f.write(audio["data"])


if __name__ == "__main__":
  

#   while True:
#     if listen_for_keyword():
#         audio_data = record_audio()
#         mp3_filename = "output1.mp3"
#         save_as_mp3(audio_data, mp3_filename)
        

#   mp3_filename = "output.mp3"
#   audio_data = record_audio()
#   save_as_mp3(audio_data, mp3_filename)

  
  text=input("Enter query bruv : ")
  answer=process_text(text)
  speak(answer)
