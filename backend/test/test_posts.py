
def test_get_all_posts(client):
    response = client.get("/posts/")
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 2
    assert json_data[0]["title"] == "First Post"
    assert json_data[0]["content"] == "Content for the first post"
    assert json_data[1]["title"] == "Second Post"
    assert json_data[1]["content"] == "Content for the second post"

def test_get_post(client):
    response = client.get("/posts/1")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["title"] == "First Post"
    assert json_data["content"] == "Content for the first post"