import os
import pandas as pd
import numpy as np
import torch
import faiss
import requests
from transformers import DPRQuestionEncoderTokenizer, DPRQuestionEncoder
from HumanInterfacing.TextToSpeech import TTSThread
from PyQt6.QtCore import pyqtSignal, QObject
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class RAGModel(QObject):
    response_signal = pyqtSignal(str)

    def __init__(self, csv_file, faiss_index_file):
        super().__init__()
        self.csv_file = csv_file
        self.faiss_index_file = faiss_index_file
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_api_url = os.getenv("GROQ_API_URL")
        self.dpr_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
        self.dpr_model = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
        self.dpr_model.eval()
        self.index = faiss.IndexFlatL2(768)
        self.answers = []
        self.tts_thread = None
        self.load_data()

    def load_data(self):
        df = pd.read_csv(self.csv_file)
        for _, row in df.iterrows():
            question = str(row.get("pattern", "")).strip()
            answer = str(row.get("response", "")).strip()
            if not question or not answer:
                continue
            inputs = self.dpr_tokenizer(question, return_tensors="pt")
            with torch.no_grad():
                embedding = self.dpr_model(**inputs).pooler_output.numpy()
            self.index.add(embedding)
            self.answers.append(answer)
        faiss.write_index(self.index, self.faiss_index_file)
        print("Knowledge base indexed successfully!")

    def retrieve_context(self, query, top_k=3):
        query_inputs = self.dpr_tokenizer(query, return_tensors="pt")
        with torch.no_grad():
            query_embedding = self.dpr_model(**query_inputs).pooler_output.numpy()
        _, indices = self.index.search(query_embedding, top_k)
        return [self.answers[i] for i in indices[0]]

    def generate_response_rag(self, question):
        retrieved_answers = self.retrieve_context(question)
        context = "\n".join(retrieved_answers)
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are an AI Receptionist at a Large Technology Park with multiple offices."},
                {"role": "user", "content": f"Question: {question}\nContext: {context}\nAnswer:"}
            ]
        }
        response = requests.post(self.groq_api_url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return "Error generating response."
        response_json = response.json()
        return response_json.get("choices", [{}])[0].get("message", {}).get("content", "No response generated.")

    def handle_question(self, question):
        response = self.generate_response_rag(question)
        self.response_signal.emit(response)
        self.speak_response(response)

    def speak_response(self, response):
        if self.tts_thread and self.tts_thread.isRunning():
            self.tts_thread.quit()
            self.tts_thread.wait()
        self.tts_thread = TTSThread(response)
        self.tts_thread.start()