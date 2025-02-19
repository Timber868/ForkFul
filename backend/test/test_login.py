# Normal Flow
def test_login_success(client):
    response = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'password'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Logged in successfully.'

# Error Flow
def test_login_invalid_credentials(client):
    response = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'wrong_password'
    })
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid username or password.'

# Error Flow
def test_login_missing_data(client):
    response = client.post('/auth/login', json={
        'username': 'admin'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Please enter both email and password.'