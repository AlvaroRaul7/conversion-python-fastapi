from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_bad_conversions():
    response = client.get("/", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 401


def test_get_bad_user_me():
    response = client.get("/users/me/", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 401



def test_create_bad_token():
    response = client.post(
        "/token/",    
        json={"username": "alvaro", "password": "secret"},
    )
    assert response.status_code == 307
  
