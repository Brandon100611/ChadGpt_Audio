# 💪 ChadGPT — A Local AI Mentor System

**ChadGPT** is a fully local, voice-first AI mentor designed to act as a calm, emotionally-aware older brother — combining the mindset of a therapist with the discipline of a gym coach.

This project was built to explore **multimodal AI interaction** (speech, reasoning, UI) without relying on paid APIs, while maintaining low latency and a natural conversational feel.

---

## 🧠 Why This Exists
Most AI voice assistants rely on cloud APIs, subscriptions, or limited interaction models.  
ChadGPT was built to answer a simple question:

> *Can a free, fully local AI system feel supportive, responsive, and human — without sacrificing control or performance?*

---

## 🔧 Technical Overview

**Core Stack**
- **LLM:** Llama 3 via Ollama (local inference)
- **Speech-to-Text:** Faster-Whisper (offline, low-latency)
- **Text-to-Speech:** edge-tts with neural voices
- **UI:** Tkinter (multi-threaded to avoid blocking audio or inference)
- **Audio Playback:** Pygame
- **Language:** Python

**Key Engineering Challenges Solved**
- Preventing audio playback blocking LLM inference
- Managing concurrent UI + speech + reasoning threads
- Eliminating paid API dependencies
- Handling ambient noise and transcription accuracy
- Designing a personality system prompt that feels supportive but grounded

---

## ✨ Features
- **Voice-First Interaction:** Speak naturally, receive spoken responses
- **Mentor Personality:** Calm, grounded, emotionally intelligent guidance
- **Local & Free:** No OpenAI keys, no subscriptions
- **Persistent Mood Logging:** Simple sentiment tracking for long-term reflection
- **Always-On UI:** Visual presence without interfering with performance

---

## 🚀 Future Roadmap
- Adaptive coaching based on long-term mood trends
- Context-aware reminders (training, coding sessions)
- Modular personality profiles
- Potential integration with game development workflows (Unity / Unreal)

---

## 📌 Notes
This project is experimental and built for learning, exploration, and system design practice.  
It is **not** intended as a replacement for professional therapy or coaching.
