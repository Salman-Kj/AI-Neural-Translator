# ✨ AI Neural Translator

A modern, interactive AI-powered language translation web application built with **Python and Streamlit**. The application allows users to translate text between multiple languages, convert speech into text, and listen to translated text using text-to-speech.

> **CodeAlpha AI Internship — Task 1**

---

## 🚀 Project Overview

**AI Neural Translator** is designed to provide a simple and user-friendly translation experience through a modern web interface.

The application supports:

- 🌐 Multi-language text translation
- 🎙️ Speech input
- 📝 Speech-to-text conversion
- 🔊 Text-to-speech voice output
- 🌙 Dark/Night mode
- ☀️ Light/Day mode
- ✨ Modern glassmorphism user interface
- 📱 Responsive two-column layout
- 🎨 Interactive buttons and animations

---

## 🛠️ Technologies Used

### Programming Language

- **Python**

### Framework

- **Streamlit**

### APIs & Libraries

- **MyMemory Translation API** — Text translation
- **gTTS (Google Text-to-Speech)** — Voice output
- **SpeechRecognition** — Speech-to-text
- **urllib** — API communication
- **JSON** — API response processing
- **HTML/CSS** — Custom user interface styling

---

## 🌍 Supported Languages

The application currently supports:

| Language | Code |
|---|---|
| English | `en` |
| Urdu | `ur` |
| Sindhi | `sd` |
| Spanish | `es` |
| French | `fr` |
| German | `de` |
| Chinese (Simplified) | `zh-CN` |
| Arabic | `ar` |
| Japanese | `ja` |

---

## ✨ Features

### 1. Text Translation

Users can enter text and select:

- Source language
- Target language

The application sends the text to the MyMemory Translation API and displays the translated result.

---

### 2. Speech Input

Users can record their voice directly through the Streamlit audio input.

The recorded speech can then be processed using the speech recognition functionality.

---

### 3. Speech-to-Text

The application uses the `SpeechRecognition` library with Google's speech recognition service to convert recorded speech into text.

This allows users to speak instead of manually typing their text.

---

### 4. Text-to-Speech

Translated text can be converted into spoken audio using **gTTS**.

Users can listen to their translated result directly inside the application.

---

### 5. Day & Night Mode

The application includes a theme switcher that allows users to change between:

- ☀️ Day Mode
- 🌙 Night Mode

The interface dynamically changes its colors and appearance.

---

### 6. Modern UI

The application uses a custom **glassmorphism-inspired interface** with:

- Glass cards
- Gradient backgrounds
- Rounded corners
- Hover effects
- Smooth animations
- Modern typography
- Interactive buttons

---

## 📂 Project Structure

```text
AI-Neural-Translator/
│
├── app.py
├── requirements.txt
└── README.mds
