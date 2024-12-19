from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class EventProperties(BaseModel):
    distinct_id: str
    session_id: str
    journey_id: str
    current_url: str = Field(alias="$current_url")  # Usamos alias para "$current_url"
    host: str = Field(alias="$host")
    pathname: str = Field(alias="$pathname")
    browser: str = Field(alias="$browser")
    device: str = Field(alias="$device")
    screen_height: int = Field(alias="$screen_height")
    screen_width: int = Field(alias="$screen_width")
    eventType: str
    elementType: str
    elementText: Optional[str]
    elementAttributes: Dict[str, str]
    timestamp: str
    x: int
    y: int
    mouseButton: int
    ctrlKey: bool
    shiftKey: bool
    altKey: bool
    metaKey: bool

class Event(BaseModel):
    event: str
    properties: EventProperties
    timestamp: str

class EventList(BaseModel):
    events: List[Event]
