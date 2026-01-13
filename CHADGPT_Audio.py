import speech_recognition as sr
import pyttsx3
import re
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
from langchain_ollama import ChatOllama

# --- 1. PERSONALITY ---
# This turns the Llama3 brain into your mentor/older brother
SYSTEM_PROMPT = """You are ChadGPT. A calm, clever, emotionally-aware AI mentor who speaks like a supportive older brother 
and thinks like a therapist who hits the gym. You’re confident, insightful, and chill — never robotic. 
Keep it real. Help the user become stronger, wiser, and more self-aware."""

# --- 2. INITIALIZE OLLAMA ---
llm = ChatOllama(model="llama3", temperature=0.7)

# --- 3. VOICE ENGINE ---
def speak_text(text):
    """Re-initializes the engine every time to fix the 'one-time voice' bug."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        # Setting to voices[0] for the male voice
        if len(voices) > 0:
            engine.setProperty('voice', voices[0].id) 
        
        engine.setProperty('rate', 170) # Chad is chill, so we slow him down a bit
        
        clean_text = re.sub(r'\*.*?\*', '', text)
        engine.say(clean_text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"Voice Error: {e}")

# --- 4. EARS ---
def recognize_speech():
    r = sr.Recognizer()
    r.energy_threshold = 300 
    with sr.Microphone(device_index=3) as source:
        try:
            audio = r.listen(source, timeout=None, phrase_time_limit=5)
            return r.recognize_google(audio)
        except:
            return None

# --- 5. VISUAL WINDOW ---
def create_window():
    root = tk.Tk()
    root.title("ChadGPT - Mentor System")
    root.attributes("-topmost", True)
    # Adjusted window size to be slightly smaller and fit the resize
    root.geometry("1280x800") 
    root.configure(bg="black")
    
    try:
        # Load your giga-chad.png image
        img = Image.open("giga-chad.png")
        # Resize to fit the 1280 width nicely
        img = img.resize((1280, 720)) 
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(root, image=photo, bg="black")
        label.image = photo 
        label.pack(pady=20)
    except Exception as e:
        print(f"Image Error: {e}")
        label = tk.Label(root, text="[ChadGPT is waiting for the image...]\nPut giga-chad.png in this folder!", 
                         fg="gold", bg="black", font=("Arial", 16))
        label.pack(expand=True)
    
    root.mainloop()

# --- 6. THE MAIN LOOP ---
def main_logic():
    print("\n[SYSTEM] ChadGPT is online. The mentor is ready, Brandon.")
    while True:
        print("\n--- Chad is listening ---")
        user_input = recognize_speech()
        
        if user_input:
            user_input = user_input.replace("London", "Brandon").replace("Glendale", "Brandon")
            print(f"You: {user_input}")
            
            print("Chad is thinking...")
            full_input = f"{SYSTEM_PROMPT}\n\nHuman: {user_input}\nAI:"
            
            try:
                response = llm.invoke(full_input)
                ai_text = response.content.strip()
                print(f"ChadGPT: {ai_text}")
                
                speak_text(ai_text)
            except Exception as e:
                print(f"Brain Error: {e}")

# --- 7. EXECUTION ---
if __name__ == "__main__":
    # Start the visual window on a background thread
    Thread(target=create_window, daemon=True).start()
    # Start the hearing/thinking loop on the main thread
    main_logic()