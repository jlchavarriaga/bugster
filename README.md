# bugster
Servicio para agrupar en "historias de usuario" eventos de interacción de los clientes

## Instalación con entorno virtual

1. Clona el repositorio:
   ```bash
   git clone https://github.com/jlchavarriaga/bugster
   cd bugster-api
   ```

2. Crea un entorno virtual e instálalo:
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. Crea un archivo .env con las variables de entorno necesarias:
   ```plaintext
   APP_NAME=Bugster API
   DEBUG_MODE=True
   ```

4. Correr el servidor:
   ```bash
   uvicorn main:app --reload
   ```

## Documentación de la API

### Endpoints

#### 1. **POST /api/v1/events**
- **Descripción**: Recibe un array de eventos y los almacena en memoria.
- **Cuerpo de la solicitud**:
  ```json
  {
    "events": [
      {
        "event": "$click",
        "properties": {
          "distinct_id": "user1",
          "session_id": "session1",
          "journey_id": "journey1",
          "$current_url": "https://example.com",
          "$host": "example.com",
          "$pathname": "/home",
          "$browser": "Chrome",
          "$device": "Desktop",
          "eventType": "click",
          "elementType": "button",
          "elementText": "Submit",
          "elementAttributes": {
            "class": "btn-primary",
            "href": "/submit"
          },
          "timestamp": "2024-12-19T12:34:56.789Z",
          "x": 100,
          "y": 200,
          "mouseButton": 0,
          "ctrlKey": false,
          "shiftKey": false,
          "altKey": false,
          "metaKey": false
        },
        "timestamp": "2024-12-19T12:34:56.789Z"
      }
    ]
  }
  ```
- **Respuesta**:
  ```json
  {
    "message": "Events stored successfully",
    "count": 1
  }
  ```

#### 2. **GET /api/v1/stories**
- **Descripción**: Retorna historias de usuario agrupadas por `session_id`.
- **Parámetros**:
  - `session_id` (opcional): Filtra las historias por ID de sesión.
- **Respuesta**:
  ```json
  [
    {
      "session_id": "session1",
      "events": [
        {
          "event": "$click",
          "properties": {
            "distinct_id": "user1",
            "session_id": "session1",
            "journey_id": "journey1",
            "$current_url": "https://example.com",
            "$host": "example.com",
            "$pathname": "/home",
            "$browser": "Chrome",
            "$device": "Desktop",
            "eventType": "click",
            "elementType": "button",
            "elementText": "Submit",
            "elementAttributes": {
              "class": "btn-primary",
              "href": "/submit"
            },
            "timestamp": "2024-12-19T12:34:56.789Z",
            "x": 100,
            "y": 200,
            "mouseButton": 0,
            "ctrlKey": false,
            "shiftKey": false,
            "altKey": false,
            "metaKey": false
          },
          "timestamp": "2024-12-19T12:34:56.789Z"
        }
      ]
    }
  ]
  ```

#### 3. **GET /api/v1/tests**
- **Descripción**: Genera scripts de pruebas E2E basados en historias de usuario.
- **Parámetros**:
  - `session_id` (opcional): Filtra las historias por ID de sesión antes de generar los tests.
- **Respuesta**:
  ```json
  {
    "tests": [
      {
        "session_id": "session1",
        "test": "import { test, expect } from '@playwright/test';\n\n" +
                 "test.describe('Session session1', () => {\n\n" +
                 "    test('User Story', async ({ page }) => {\n\n" +
                 "        await page.click('.btn-primary');\n\n" +
                 "    });\n\n" +
                 "});\n"
      }
    ]
  }
  ```

## Decisiones de diseño
- **FastAPI**: Elegido para el reto es ideal por su simplicidad, rendimiento y soporte para documentación automática.
- **Almacenamiento en memoria**: Simplifica el desarrollo inicial y evita dependencias externas.
- **Playwright**: Herramienta moderna y robusta para generar pruebas E2E.
- **Pydantic**: Para garantizar la validación de datos de entrada.

## Trade-offs considerados
- **Almacenamiento en memoria**: No es ideal para producción debido a la volatilidad de los datos, seria ideal usar una base de datos como PostgreSQL o MongoDB para almacenar eventos
- **Escalabilidad**: Este diseño inicial no maneja concurrencia o grandes volúmenes de datos.

## Modo de Uso de Tests

1. **Instalar dependencias de pruebas**:
   Asegúrate de que `pytest` esté instalado:
   ```bash
   pip install pytest
   ```

2. **Ejecutar las pruebas**:
   Usa el siguiente comando desde la raíz del proyecto para ejecutar los tests definidos en `test_main.py`:
   ```bash
   pytest tests/test_main.py
   ```

3. **Resultados Esperados**:
   Si todas las pruebas pasan, deberías ver un resultado similar:
   ```bash
   ======================== test session starts ========================
   collected 1 item

   tests/test_main.py .                                          [100%]

   ========================= 1 passed in 0.12s =========================
   ```
