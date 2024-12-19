from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict

from dotenv import load_dotenv
import os
from models import EventList, Event

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "FastAPI App"))

# Almacenamiento en memoria
event_store: List[Event] = []


@app.post("/api/v1/events")
async def post_events(event_list: EventList):
    try:
        event_store.extend(event_list.events)
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
