import requests
import time
from csv import reader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from googletrans import Translator
from utils.traslater import traducir

class ResponseModel:
    def __init__(self):
        self.load_data()

    def load_data(self):
        with open('./assets/data.csv', encoding='utf-8') as archivo:
            lector = reader(archivo)
            datos = list(lector)
        self.preguntas = [fila[0] for fila in datos]
        self.respuestas = [fila[1] for fila in datos]
        self.vectorizer_preguntas = CountVectorizer(ngram_range=(1, 1), analyzer='char', dtype=np.int32)
        self.preguntas_vectorizadas = self.vectorizer_preguntas.fit_transform(self.preguntas).toarray()
                
    
    def obtener_respuesta(self, pregunta_usuario):
        pregunta_usuario_vectorizada = self.vectorizer_preguntas.transform([pregunta_usuario]).toarray()
        similitud = cosine_similarity(pregunta_usuario_vectorizada, self.preguntas_vectorizadas)
        idx =np.argmax(similitud)
        return self.respuestas[idx]
    
    
    def tell_joke(self):
        response = requests.get('https://api.chucknorris.io/jokes/random')
        if response.status_code == 200: # Obtener el chiste aleatorio de la respuesta JSON 
            joke = response.json()['value'] # Imprimir el chiste print(joke) 
            return traducir(str(joke)) # Retornar el chiste traducido
        else: # Imprimir un mensaje de error si la solicitud no fue exitosa 
            return '¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.'