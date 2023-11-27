## Creación del Entorno Virtual
~~~ bash
python3 -m venv env
source env/bin/activate  # en Windows es env\Scripts\activate
~~~

## Instalación de Dependencias
~~~ bash
pip install -r requirements.txt
~~~

## Ejecución del Proyecto
~~~ bash
python main.py # o el archivo principal de Python
~~~

## Variables de Entorno
El proyecto utiliza las siguientes variables de entorno:
* `meteosource` Llave de API meteosource