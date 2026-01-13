import speech_recognition as sr
import re
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
from langchain_ollama import ChatOllama
from faster_whisper import WhisperModel
import edge_tts
import pygame
import asyncio
import os

# --- 1. PERSONALITY ---
SYSTEM_PROMPT = """You are ChadGPT. A calm, clever, emotionally-aware AI mentor who speaks like a supportive older brother 
and thinks like a therapist who hits the gym. You’re confident, insightful, and chill — never robotic. 
Keep it real. Help Brandon become stronger, wiser, and more self-aware. No emojis."""

# --- 2. INITIALIZE HARDWARE (Global Scope) ---
llm = ChatOllama(model="llama3", temperature=0.7)
whisper_model = WhisperModel("base.en", device="cpu", compute_type="int8")

# --- 3. THE NEURAL VOICE ---
def speak_text(text):
    clean_text = re.sub(r'\*.*?\*', '', text)
    async def _generate():
        # 'en-US-ChristopherNeural' or 'en-US-GuyNeural' are solid "older brother" voices
        communicate = edge_tts.Communicate(clean_text, "en-US-ChristopherNeural")
        await communicate.save("chad_voice.mp3")

    try:
        asyncio.run(_generate())
        pygame.mixer.init()
        pygame.mixer.music.load("chad_voice.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        if os.path.exists("chad_voice.mp3"):
            os.remove("chad_voice.mp3")
    except Exception as e:
        print(f"Voice Error: {e}")

# --- 4. HIGH-RES EARS ---
def recognize_speech():
    global whisper_model
    r = sr.Recognizer()
    r.energy_threshold = 1000  # Filters out room hum
    r.dynamic_energy_threshold = True
    
    with sr.Microphone(device_index=3) as source:
        try:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("\n--- Chad is listening ---")
            audio = r.listen(source, timeout=None, phrase_time_limit=5)
            
            with open("temp_chad_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            segments, info = whisper_model.transcribe("temp_chad_audio.wav", beam_size=5)
            text = "".join([segment.text for segment in segments]).strip()
            return text
        except Exception as e:
            print(f"Hearing Error: {e}")
            return None

# --- 5. VISUAL WINDOW ---
def create_window():
    root = tk.Tk()
    root.title("ChadGPT - Mentor System")
    root.attributes("-topmost", True)
    root.geometry("1280x800") 
    root.configure(bg="black")
    
    try:
        img = Image.open("giga-chad.png").resize((1280, 720)) 
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(root, image=photo, bg="black")
        label.image = photo 
        label.pack(pady=20)
    except:
        label = tk.Label(root, text="Missing giga-chad.png", fg="gold", bg="black", font=("Arial", 16))
        label.pack(expand=True)
    
    root.mainloop()

# --- 6. THE MAIN LOOP ---
def main_logic():
    print("\n[SYSTEM] ChadGPT is online. The mentor is ready, Brandon.")
    while True:
        user_input = recognize_speech()
        
        if user_input:
            user_input = user_input.replace("London", "Brandon").replace("Glendale", "Brandon")
            print(f"Brandon: {user_input}")
            
            # Log the vibe before responding
            vibe_score = log_mood(user_input)
            
            print("[SYSTEM] Chad is thinking...")
            full_input = f"{SYSTEM_PROMPT}\n\nHuman: {user_input}\nAI:"
            
            try:
                response = llm.invoke(full_input)
                ai_text = response.content.strip()
                print(f"ChadGPT: {ai_text}")
                speak_text(ai_text)
            except Exception as e:
                print(f"Brain Error: {e}")

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