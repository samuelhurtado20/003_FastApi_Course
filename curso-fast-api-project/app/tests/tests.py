from fastapi.testclient import TestClient

def test_client(client):
    response = client.get("/datetime")
    #print(response.json())
    assert response.status_code == 200
    #assert response.json() == {"status": "ok"}
    assert "datetime" in response.json()

def test_another_example(client):
    assert type(client) == TestClient