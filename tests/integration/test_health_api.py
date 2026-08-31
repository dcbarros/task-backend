def test_should_return_health_status(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}