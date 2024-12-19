# bugster
Servicio para agrupar en historias de usuario eventos de interacción de usuario

## Instalación con entorno virtual

1. Clona el repositorio:
   ```bash
   git clone https://github.com/jlchavarriaga/bugster
   cd bugster-api

2. Crea un entorno virtual e instálalo:
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows: env\Scripts\activate
    pip install -r requirements.txt

3. Crea un archivo .env con las variables de entorno necesarias:
    ```bash
    APP_NAME=Bugster API
    DEBUG_MODE=True

4. Correr el Servidor
    uvicorn main:app --reload


