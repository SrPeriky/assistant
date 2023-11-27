import pyttsx3
import tkinter as tk
from PIL import ImageTk, Image

class AssistantUI(): 
    def __init__(self, hablar): 
        self.engine = pyttsx3.init() 
        self.ventana = tk.Tk() 
        self.name = 'Leslie' 
        self.contenedor = None 
        self.imagenLeslie = None 
        self.imagenCarga = None 
        self.imagenConfition = None
        self.hablar = hablar
        
    def container(self):
        self.contenedor = tk.Frame(self.ventana, bg="#FDF0BB")
        self.contenedor.pack()

    def cargarImg(self):
        self.imagenLeslie = Image.open("./assets/leslie.jpg")
        self.imagenLeslie = self.imagenLeslie.resize((160, 140))
        self.imagenLeslie = ImageTk.PhotoImage(self.imagenLeslie)
        self.imagenCarga = Image.open("./assets/leslieListening.jpg")
        self.imagenCarga = self.imagenCarga.resize((160, 140))
        self.imagenCarga = ImageTk.PhotoImage(self.imagenCarga)
        self.imagenConfition = Image.open("./assets/leslieConfution.jpg")
        self.imagenConfition = self.imagenConfition.resize((160, 140))
        self.imagenConfition = ImageTk.PhotoImage(self.imagenConfition)
        self.imagenEscibiendo = Image.open("./assets/leslieEscribiendon.jpg")
        self.imagenEscibiendo = self.imagenEscibiendo.resize((160, 140))
        self.imagenEscibiendo = ImageTk.PhotoImage(self.imagenEscibiendo)

    def btnDISABLED(self):
        self.hablar_button.config(state=tk.DISABLED)

    def btnNORMAL(self):
        self.hablar_button.config(state=tk.NORMAL)


    def mostrarImg(self, imagen):
        if hasattr(self, "imagen_label"):
            self.imagen_label.pack_forget()
        self.imagen_label = tk.Label(self.contenedor, image=imagen, bg="#FDF0BB")
        self.imagen_label.pack(side=tk.LEFT, padx=12, pady=10)

    def cajaRespuesta(self):
        self.respuesta_text = tk.Text(self.ventana, height=12, width=40, wrap="word")
        self.respuesta_text.pack(padx=10, pady=10)

    def show_response(self, user, text):
        #self.respuesta_text.delete('1.0', tk.END)
        self.respuesta_text.insert('1.0', f"{user}: {text}")

    def crearBotones(self):
        self.hablar_button = tk.Button(self.contenedor, text="Hablar", command=self.hablar)
        self.hablar_button.configure(
            bg="#EA3680",  # Color de fondo
            fg="white",  # Color de texto
            font=("Arial", 12, "bold"),  # Fuente y tamaño de texto
            padx=10,  # Espacio horizontal interno
            pady=10  # Espacio vertical interno
        )
        self.hablar_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.ventana.bind('<space>', self.click_hablar_button)
        #self.hablar_button.bind("<space>", self.click_hablar_button)

    def click_hablar_button(self, event):
        self.hablar_button.invoke()

    def start(self):
        self.ventana.title(f"{self.name} - asistente virtual") 
        self.ventana.configure(bg="#FDF0BB")
        self.cargarImg()
        self.container()
        self.crearBotones()
        self.mostrarImg(self.imagenLeslie)
        self.cajaRespuesta()
        self.ventana.geometry("400x400")
        self.ventana.resizable(False, False)
        self.ventana.mainloop()

    # Lógica para hablar
#Crear una instancia de la interfaz de usuario

   