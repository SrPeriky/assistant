import fnmatch
import json
import os
from sklearn.metrics.pairwise import cosine_similarity
#from torch import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

class AppModel():

    def __init__(self):
        self.umbral_de_similitud = 0.75

        try:
            with open('./assets/app.json', encoding='utf-8') as archivo_json:
                self.programData = json.load(archivo_json)
        except (FileNotFoundError, json.JSONDecodeError):
            self.programData = self.setJsonData()

        self.vectorizerProgram = CountVectorizer(ngram_range=(1, 1), analyzer='char', dtype=np.int32)
        self.vectorizerCategory = CountVectorizer(ngram_range=(1, 1), analyzer='char', dtype=np.int32)
        self.programNames = [category["name"] for category in self.programData["Programs"]]
        self.vectorizerNames = self.vectorizerProgram.fit_transform(self.programNames).toarray()
        self.programCategory = [category for category, programas in self.programData.items() if category != "Programs" ]
        self.vectorizerCategory = self.vectorizerCategory.fit_transform(self.programCategory).toarray()

    def  searchSimilarProgram(self, nombre_programa):
        try:
            partes = nombre_programa.split('de')
            nombre_programa = ''.join(partes[-1]).strip()
            print(nombre_programa)

            for programa in self.programData["Programs"]:
                if nombre_programa in programa["name"]:
                    return [programa]

            # Vectorizar el nombre del programa
            nombre_programa_vectorizado = self.vectorizerProgram.transform([nombre_programa]).toarray()

            # Calcular la similitud coseno con cada programa (incluyendo nombres de programas)
            similitudes_programs = cosine_similarity(nombre_programa_vectorizado, self.vectorizerNames)


            idx_programs = np.argmax(similitudes_programs)
            similitud_programs = similitudes_programs[0, idx_programs]
            if similitud_programs < self.umbral_de_similitud:
                nombre_category_vectorizado = self.vectorizerCategory.transform([nombre_programa]).toarray()
                similitudes_category = cosine_similarity(nombre_category_vectorizado, self.vectorizerCategory)
                idx_category = np.argmax(similitudes_category)
                similitud_category = similitudes_category[0, idx_category]
                print(similitud_category)
                if similitud_category > self.umbral_de_similitud:
                    valor_asociado = self.programData.get(self.programCategory[idx_category], None)
                    if valor_asociado is not None:
                        el = len(valor_asociado)
                        if el == 0:
                            return []
                        
                        return valor_asociado
                return []
                
                    #return self.getListProgramsInCategory(valor_asociado)
                
            # Si la similitud es alta, devolver la ruta del programa encontrado
            return self.programData["Programs"][idx_programs]
        except:
            return []
    
    def getListProgramsInCategory(self, category):
        #return "bla vla bla"
        return [programa for programa in category]
    
    def setJsonData(self):
        # Define las rutas de las carpetas
        ruta_carpeta_1 = os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')
        ruta_carpeta_2 = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs')

        rutas_carpetas = [ruta_carpeta_1, ruta_carpeta_2]
        patrones = ['*.lnk', '*.url', '*.desktop', '*.appref-ms']

        print("La información se ha guardado en app.json.")
        archivos_encontrados = {}

        for ruta_carpeta in rutas_carpetas:
            for ruta_actual, carpetas, archivos in os.walk(ruta_carpeta):
                for patron in patrones:
                    for archivo in fnmatch.filter(archivos, patron):
                        ruta_completa = os.path.join(ruta_actual, archivo)
                        carpeta = os.path.basename(ruta_actual)

                        if carpeta not in archivos_encontrados:
                            archivos_encontrados[carpeta] = []

                        # Almacena el nombre del programa y la ruta del archivo
                        archivos_encontrados[carpeta].append({"name": archivo.replace('.lnk', "").lower(), "path": ruta_completa})

        with open('./assets/app.json', 'w') as archivo_json:
            json.dump(archivos_encontrados, archivo_json, indent=2)

        return archivos_encontrados