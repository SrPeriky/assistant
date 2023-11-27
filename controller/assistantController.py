import time
from model.responseModel import ResponseModel
from model.speechModel import SpeechModel
from model.userModel import UserModel
from model.programModel import AppModel
from model.weatherModel import WeatherModel
from view.assistantUI import AssistantUI
from threading import Thread
import os


class AssistantController:
    def __init__(self):
        self.program = AppModel()
        self.user = UserModel()
        self.responses = ResponseModel()
        self.speech = SpeechModel()
        self.ui = AssistantUI(self.hablar)
        latitud, longitud = self.user.getLatLog()
        self.weather = WeatherModel(latitud,longitud)
        self.speaking = False

    def start(self):
        self.ui.start()
        return 0

    def hablar(self):
        if not self.speaking:
            self.speaking = True
            # Utiliza threading para ejecutar listen en otro hilo
            self.ui.btnDISABLED()
            self.ui.mostrarImg(self.ui.imagenCarga)
            thread = Thread(target=self.listenAndHandle)
            thread.start()

    def listenAndHandle(self):
        text = self.speech.listen()
        self.ui.show_response(self.user.getName(), f"{text}\n\n")
        self.ui.mostrarImg(self.ui.imagenEscibiendo)
        if text:
            res = self.handleText(text)
            time.sleep(len(res)/100)
            self.ui.show_response(self.ui.name, f"{res}\n")
            if "No encontré ningún programa similar 🥺" in res:
                self.ui.mostrarImg(self.ui.imagenConfition)
                time.sleep(2.5)
            self.ui.mostrarImg(self.ui.imagenLeslie)       
        self.ui.btnNORMAL()
        self.speaking = False


    def abrirArchivoLnk(self, ruta):
        os.startfile(ruta)

    def abrirApp(self, text, res):
        partes = text.split('aplicación')
        text = ''.join(partes[-1]).strip()
        rta = self.program.searchSimilarProgram(text)
        if rta is not None:
            if len(rta) == 0:
                return "No encontré ningún programa similar 🥺"
            elif len(rta) == 1:
                self.abrirArchivoLnk(rta[0]["path"])
                return res.replace("[app]", rta[0]["name"])
            else:
                listText = "\n".join([f"* {item['name']}" for item in rta])
                return f"Encontré:\n{listText}"

    def handleText(self, text):
        replacements = [
            ("[fecha]", self.user.get_date()),
            ("[User]", self.user.getName()),
            ("[hora]", self.user.get_time()),
            ("[chiste]", self.responses.tell_joke()),
            ("[clima]", "\n"+self.weather.getWeather(f"{self.user.fullDate()}"))
        ]
        res = self.responses.obtener_respuesta(text)
        for old, new in replacements:
            if old in res:
                res = res.replace(old, new)
        if "[app]" in res:
            res = self.abrirApp(text, res)
        
        return res