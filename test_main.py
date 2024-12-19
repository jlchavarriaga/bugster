import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_post_events():
    # Leemos aca el archivo JSON
    with open("events.json", "r") as file:
        data = json.load(file)

    # Enviar la solicitud POST con el JSON cargado
    response = client.post(
        "/api/v1/events",
        json=data
    )

    # Validar la respuesta
    assert response.status_code == 200
    assert response.json()["message"] == "Events stored successfully"
