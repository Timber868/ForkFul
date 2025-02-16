
def test_home_route(client):
    """Test the home route."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"status": True}
