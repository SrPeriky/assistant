import speech_recognition as sr

# Clase para manejar el reconocimiento de voz
class SpeechModel:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        
    def listen(self):
        self.listening = True
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source) 
                reconocer = self.recognizer.recognize_google(audio, language="es-ES")
                self.listening = False
                return str(reconocer).lower()

            except sr.UnknownValueError:
                self.listening = False
                return False