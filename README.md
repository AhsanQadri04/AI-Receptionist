# 🧠 AI Receptionist System for Technology Park

The **AI Receptionist System** is an intelligent virtual assistant designed specifically for technology parks. It streamlines navigation, manages meetings, and enhances visitor experiences with its advanced features, ensuring seamless interactions for all users.

---

## 🚀 Features

### 🌐 Facility Navigation  
- Guides visitors to various **offices**, **cafeterias**, and other locations within the technology park.  
- Provides clear directions to ensure efficient navigation.  

### 🛠 Lost and Found Management  
- Keeps track of **lost and found items**.  
- Helps users register lost items or search for recovered ones easily.  

### 📅 Meeting Management  
- Organizes and accommodates meetings between **park offices** and **external visitors**.  
- Maintains a centralized system for scheduling and coordination.  

### 📸 Facial Record Keeping  
- Captures and stores **photos of visitors** for future reference.  
- Maintains a secure database of visitor records for efficient tracking.  

### 🗣️ Speech-to-Text (STT) and Text-to-Speech (TTS)  
- **Voice interaction** for enhanced accessibility and ease of use.  
- Converts speech to text for chatbot queries and responses.  
- Reads responses aloud for users with text-to-speech functionality.  

### 🤖 Interactive Chatbot  
- **Natural Language Processing (NLP)** enables the chatbot to understand and respond to user queries.  
- Provides an intuitive and conversational interface for user interaction.  

---

## 🛠️ Built With  

### Frontend  
- **PyQt6**: Provides an elegant and responsive GUI.  

### Camera Functionality  
- **OpenCV**: Powers the facial recognition and photo capture system.  

### Speech-to-Text  
- **Google Speech Recognition Library**: Handles STT for seamless voice input.  

### Text-to-Speech  
- **pyttsx3**: Provides TTS for audio responses.  

### Chatbot Functionality  
The intelligent chatbot leverages the following libraries:  
- **nltk**: Tokenizes, processes, and analyzes text.  
- **fuzzywuzzy**: Enables approximate string matching for better query understanding.  

---

## 🏗️ System Architecture  

1. **Frontend (PyQt6)**: User-friendly GUI for interacting with the receptionist system.  
2. **Chatbot (NLP)**: Processes queries and provides intelligent responses.  
3. **Camera Module**: Captures and stores visitor images using OpenCV.  
4. **Speech Integration**:  
   - STT converts spoken queries into text.  
   - TTS provides audio responses for a more interactive experience.  
5. **Database**:  
   - Stores visitor records and facial images securely.  
   - Manages lost and found items and meeting schedules.  

---

## 📦 Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/AI-Receptionist-System.git
   cd AI-Receptionist-System
