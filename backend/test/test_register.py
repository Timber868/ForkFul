# Normal Flow
def test_register_success(client):
    response = client.post('/auth/register', json={
        'username': 'new_user',
        'email': 'new_email@example.com',
        'password': 'password',
        'name': 'new_name',
        'phoneNumber': '1234567899'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'User created successfully.'

# Error Flow
def test_register_existing_user(client):
    response = client.post('/auth/register', json={
        'username': 'admin',
        'email': 'new_email1@example.com',
        'password': 'password',
        'name': 'new_name',
        'phoneNumber': '1234567891'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Username already exists.'

# Error Flow
def test_register_missing_data(client):
    response = client.post('/auth/register', json={
        'username': 'new_user2'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Please enter all fields.'

# Error Flow
def test_register_existing_email(client):
    response = client.post('/auth/register', json={
        'username': 'new_user1',
        'email': 'new_email@example.com',
        'password': 'password',
        'name': 'new_name',
        'phoneNumber': '1234567892'
    })
    assert response.status_code == 400 
    assert response.json['message'] == 'Email already exists.'

# Error Flow
def test_register_existing_phoneNumber(client):
    response = client.post('/auth/register', json={
        'username': 'new_user2',
        'email': 'another@example.com',
        'password': 'password',
        'name': 'new_name',
        'phoneNumber': '1234567899'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Phone number already exists.'




