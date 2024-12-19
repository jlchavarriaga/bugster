from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_post_events():
    response = client.post(
        "/api/v1/events",
        json={
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
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Events stored successfully"
