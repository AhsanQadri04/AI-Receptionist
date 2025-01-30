# 🧠 AI Receptionist System for Technology Park  

The **AI Receptionist System** is an advanced virtual assistant designed to enhance visitor experiences within a technology park. It provides seamless navigation assistance, automated interactions, and real-time responses to queries, ensuring an efficient and welcoming environment.  

---

## 🚀 Features  

### 🌐 Intelligent Facility Navigation  
- Provides accurate directions to various **departments**, **offices**, and **facilities**.  
- Uses **speech recognition** to understand visitor inquiries.  
- Integrates with **computer vision** to log visitor details using facial recognition.  

### 🎙️ Advanced Speech Recognition  
- Supports both **Urdu** and **English** for effortless multilingual communication.  
- Uses real-time **voice-to-text conversion** to process spoken queries.  
- Detects spoken language automatically and translates **Urdu** into **English** for accurate responses.  

### 📸 Face-Based Logging  
- Eliminates the need for manual name entry—logs interactions using captured face images.  
- Ensures better visitor tracking and enhanced personalization without storing sensitive data.  

### 🔄 Developer Override & Reinforcement Learning  
- Allows real-time correction of incorrect chatbot responses through a **developer override system**.  
- Uses **reinforcement learning** to adapt and improve over time.  
- Stores voice recognition corrections to avoid repeated errors.  

### 💬 Smart Conversational AI  
- Processes text and voice-based inquiries using an **intent-driven approach**.  
- Leverages **Natural Language Processing (NLP)** to provide intelligent responses.  
- Responds to facility-related questions (e.g., **office locations**, **lost & found**, **working hours**).  

### 🏢 Office & Department Location Assistance  
- Helps visitors find departments, conference rooms, and other important locations.  
- Uses **hardcoded locations** for accurate office directions instead of guessing.  

---

## 📦 Tech Stack  

| **Component**           | **Technology Used**             |  
|--------------------------|----------------------------------|  
| Programming Language     | Python 🐍                       |  
| Speech-to-Text (STT)     | Google Speech Recognition 🎤    |  
| Text-to-Speech (TTS)     | gTTS (Google Text-to-Speech) 🔊 |  
| Machine Learning & NLP   | Scikit-learn, NLTK 📖           |  
| Face Detection           | OpenCV (Haarcascades) 📸        |  
| Data Storage             | JSON (intent-based) 🗂          |  
| GUI Framework            | PyQt6 🖥                        |  
| Translation Module       | Google Translate API 🌍         |  


## 🛠 Installation & Setup  

### 🔹 Step 1: Clone the Repository  
```bash  
git clone https://github.com/your-repo/ai-receptionist.git  
cd ai-receptionist  
