import os
import speech_recognition as sr
import re
import tkinter as tk
import asyncio
import edge_tts
import pygame
import requests
import time
from threading import Thread
from PIL import Image, ImageTk
from langchain_ollama import ChatOllama
from faster_whisper import WhisperModel

# --- 1. GLOBAL VARIABLES ---
label = None
root = None

# Initialize Pygame Mixer ONCE at the start for stability
pygame.mixer.init()

# --- 2. PERSONALITY SETUP ---
SYSTEM_PROMPT = """You are ChadGPT. A calm, clever, emotionally-aware AI mentor who speaks like a supportive older brother 
and thinks like a therapist who hits the gym. You’re confident, insightful, and chill — never robotic. 
Keep it real. Help Brandon become stronger, wiser, and more self-aware. No emojis."""

# --- 3. INITIALIZE MODELS ---
try:
    # Lower temperature keeps Chad grounded and focused on mentorship
    llm = ChatOllama(model="llama3", temperature=0.3)
except Exception:
    print("[CRITICAL] Ollama server not detected. Run 'ollama serve' first!")

whisper_model = WhisperModel("base.en", device="cpu", compute_type="int8")

# --- 4. STABLE VOICE SYSTEM ---
def speak_text(text):
    # Remove actions from speech
    clean_text = re.sub(r'\*.*?\*', '', text)
    
    async def _generate():
        # 'en-US-ChristopherNeural' is a solid, deep "older brother" voice
        voice = "en-US-ChristopherNeural" 
        communicate = edge_tts.Communicate(clean_text, voice)
        await communicate.save("chad_voice.mp3")

    try:
        asyncio.run(_generate())
        
        pygame.mixer.music.load("chad_voice.mp3")
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.music.unload()
        if os.path.exists("chad_voice.mp3"):
            os.remove("chad_voice.mp3")
    except Exception as e:
        print(f"Voice Playback Error: {e}")

# --- 5. HIGH-RES EARS (Calibrated for New Headset) ---
def recognize_speech():
    global whisper_model
    r = sr.Recognizer()
    
    # 300 is a stable floor for clear headset mics
    r.energy_threshold = 300 
    r.dynamic_energy_threshold = True 

    # Ensure this device_index matches your working headset ID
    with sr.Microphone(device_index=1) as source:
        try:
            print("[Ears] Calibrating to room noise...")
            r.adjust_for_ambient_noise(source, duration=1.5) 
            
            print(f"[Ears] Threshold set to {r.energy_threshold}. Listening for Brandon...")
            audio = r.listen(source, timeout=None, phrase_time_limit=10)
            
            with open("temp_chad_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            # Using Whisper for superior accuracy
            segments, info = whisper_model.transcribe("temp_chad_audio.wav", language="en")
            text = "".join([segment.text for segment in segments]).strip()
            
            # Hallucination Filter
            if len(text) < 2 or text.lower() in ["thank you", "you"]:
                return None
                
            return text
        except Exception as e:
            print(f"Hearing Error: {e}")
            return None

# --- 6. VISUALS (Fixed for Proper Proportion on Standard Monitors) ---
def swap_image(image_path):
    global label
    try:
        img = Image.open(image_path)
        
        # 1. Define a reasonable width for your screen (e.g., 600px)
        # We calculate the height automatically to keep it proportional (1280x1651)
        base_width = 600
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        
        # 2. Resize using the calculated proportional height
        img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
        
        new_photo = ImageTk.PhotoImage(img)
        label.config(image=new_photo)
        label.image = new_photo
        print(f"[Visual] Displaying {image_path} at {base_width}x{h_size}")
    except Exception as e:
        print(f"Image Error: {e}")

def create_window():
    global label, root
    root = tk.Tk()
    root.title("ChadGPT - Mentor System")
    root.attributes("-topmost", True)
    
    # 3. Set the window to match our calculated scale (600 width x ~773 height)
    root.geometry("600x850") 
    root.configure(bg="black")
    
    label = tk.Label(root, bg="black")
    label.pack(pady=10)
    
    swap_image("giga-chad.png") 
    root.mainloop()

# --- 7. THE MAIN LOOP ---
def main_logic():
    print("\n[SYSTEM] ChadGPT is online. The mentor is ready, Brandon.")
    while True:
        user_input = recognize_speech()
        
        if user_input:
            # Name correction logic
            user_input = user_input.replace("London", "Brandon").replace("Glendale", "Brandon")
            print(f"Brandon: {user_input}")
            
            # Mood Tracking
            vibe_score = log_mood(user_input)
            
            full_input = f"{SYSTEM_PROMPT}\n\nHuman: {user_input}\nAI:"
            
            try:
                # Connection check for local Ollama
                requests.get("http://localhost:11434", timeout=1)
                
                print("[SYSTEM] Chad is thinking...")
                response = llm.invoke(full_input)
                ai_text = response.content.strip()
                
                print(f"ChadGPT: {ai_text}")
                speak_text(ai_text)
            except Exception as e:
                print(f"System Error: {e}")

def log_mood(user_input):
    positive_words = ["good", "great", "happy", "gym", "crushed", "worked"]
    negative_words = ["tired", "sad", "fail", "lazy", "stuck", "deli", "bologna"]
    score = 0
    for word in user_input.lower().split():
        if word in positive_words: score += 1
        if word in negative_words: score -= 1
    with open("mood_log.txt", "a") as f:
        f.write(f"Vibe Score: {score} | Input: {user_input}\n")
    return score

if __name__ == "__main__":
    Thread(target=create_window, daemon=True).start()
    main_logic()
