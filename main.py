from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import logging
from models import EventList, Event
from utils import generate_playwright_test

# Configuración de logging
logging.basicConfig(level=logging.INFO, filename="app.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Bugster API")

# Almacenamiento en memoria
event_store: List[Event] = []

@app.post("/api/v1/events")
async def post_events(event_list: EventList):
    try:
        # Validación para evitar duplicados
        for event in event_list.events:
            if event not in event_store:
                event_store.append(event)
        logger.info(f"Stored events: {len(event_store)}")
        return {"message": "Events stored successfully", "count": len(event_list.events)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stories")
async def get_stories(session_id: str = Query(None, description="Filter by session ID")) -> List[Dict]:
    try:
        # Filtrar eventos por session_id si se proporciona
        filtered_events = [
            event for event in event_store
            if session_id is None or event.properties.session_id == session_id
        ]

        if not filtered_events:
            raise HTTPException(
                status_code=404,
                detail=f"No events found for session_id: {session_id}"
            )

        # Agrupar eventos por session_id
        stories = {}
        for event in filtered_events:
            session = event.properties.session_id
            if session not in stories:
                stories[session] = []
            stories[session].append(event)

        # Ordenar los eventos de cada sesión por timestamp
        for session in stories:
            stories[session].sort(key=lambda e: e.properties.timestamp)

        # Convertir a lista de historias
        user_stories = [
            {"session_id": session, "events": [e.dict() for e in events]}
            for session, events in stories.items()
        ]

        return user_stories

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/tests")
async def get_tests(session_id: str = Query(None, description="Filter by session ID")) -> JSONResponse:
    try:
        # Obtener historias de usuario con o sin filtro de session_id
        stories = await get_stories(session_id)

        if not stories:
            return JSONResponse(
                status_code=404,
                content={"detail": "No stories found for the given session_id"}
            )

        # Generar scripts de prueba en formato Playwright
        test_scripts = []
        for story in stories:
            session_id = story["session_id"]
            events = story["events"]
            script = generate_playwright_test(session_id, events)
            test_scripts.append({"session_id": session_id, "test": script})

        return JSONResponse(content={"tests": test_scripts})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/events")
async def post_events(event_list: EventList):
    try:
        event_store.extend(event_list.events)
        return {"message": "Events stored successfully", "count": len(event_list.events)}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))