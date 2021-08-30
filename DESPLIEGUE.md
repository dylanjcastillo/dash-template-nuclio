# ¿Cómo desplegar una aplicación de Dash en Heroku 

1. [Crear cuenta en Heroku](https://signup.heroku.com/)
2. [Instalar Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
3. [Instalar Git](https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-Instalaci%C3%B3n-de-Git)
4. Añadir `server=app.server` debajo de la inicialización de la aplicación de Dash:
   ```python
   app = dash.Dash(__name__)
   server = app.server
   ```
5. Crear un fichero llamado `runtime.txt` en el directorio del proyecto. Allí deberás especificar la versión de Python que utilizaste, por ejemplo:

   ```
   python-3.9.6
   ```
6. Crea un fichero llamado `requirements.txt` con las librerías (y sus versiones) que utilizaste en el proyecto. Además, debes agregar `gunicorn` como requerimiento adicional.

   ```
   pandas==1.3.2
   dash==1.21.0
   dash-labs==0.4.0
   dash-bootstrap-components==0.13.0
   gunicorn==20.1.0
   ```
7. Crea un fichero llamado `Procfile`con lo siguiente:

   ```
   web: gunicorn app:server
   ```
8. Inicializa un repositorio de git en el directorio: `git init`
9. Crear `.gitignore` para evitar subir ficheros irrelevantes 
10. Haz un commit con los ficheros guardados: `git add . && git commit -m 'Primer commit!'`
11. Crea e inicia tu app en Heroku, ejecutando los siguientes comandos desde la terminal:

    ```
    heroku create NOMBRE-APP
    git push heroku master
    heroku ps:scale web=1
    ```
12. Puedes visitar tu app en: https://NOMBRE-APP.herokuapp.com
