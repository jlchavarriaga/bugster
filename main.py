from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from models import EventList

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "FastAPI App"))

# Almacenamiento en memoria
event_store = []

@app.post("/api/v1/events")
async def post_events(event_list: EventList):
    try:
        event_store.extend(event_list.events)
        return {"message": "Events stored successfully", "count": len(event_list.events)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
