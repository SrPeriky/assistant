from googletrans import Translator

translator = Translator()
def traducir(texto):
    idioma_origen = translator.detect(texto).lang
    idioma_origen = "en"
    traduccion = translator.translate(texto, src=idioma_origen, dest='es')
    return traduccion.text