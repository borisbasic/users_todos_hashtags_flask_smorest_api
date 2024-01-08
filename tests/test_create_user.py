import json
from .client import client


def test_register(client):
    response_register = client.post('/register', json={'username': 'boris', 'email': 'boris@boris.com', 'password': '123'})

    data_register = json.loads(response_register.data.decode())

    assert response_register.status_code == 200
    assert data_register['message'] == 'User created successfully!'


    response_register_same_username = client.post('/register', json={'username': 'boris', 'email': 'boris@boris.com', 'password': '123'})

    data_register_same_username = json.loads(response_register_same_username.data.decode())
    assert response_register_same_username.status_code == 409
    assert data_register_same_username['message'] == 'User with that name exists'

    response_register_same_email = client.post('/register', json={'username': 'boris_1', 'email': 'boris@boris.com', 'password': '123'})

    data_register_same_email = json.loads(response_register_same_email.data.decode())
    assert response_register_same_email.status_code == 409
    assert data_register_same_email['message'] == 'User with that email exists'


def test_login(client):
    response_login_username = client.post('/login', json={'username': 'boris', 'email': '',  'password': '123'})

    data_login = json.loads(response_login_username.data.decode())
    assert response_login_username.status_code == 200
    assert data_login['message'] == 'User logged!'
    assert 'access_token' in data_login

    response_login_email = client.post('/login', json={'username': '', 'email': 'boris@boris.com',  'password': '123'})

    data_login = json.loads(response_login_email.data.decode())
    assert response_login_email.status_code == 200
    assert data_login['message'] == 'User logged!'
    assert 'access_token' in data_login

    response_login_invalid_credentials = client.post('/login', json={'username': 'boris_1', 'email': '',  'password': '123'})
    
    data_login = json.loads(response_login_invalid_credentials.data.decode())
    assert response_login_invalid_credentials.status_code == 401
    assert data_login['message'] == 'Invalid credentials!'


def test_logut(client):
    response_login_username = client.post('/login', json={'username': 'boris', 'email': '',  'password': '123'})

    data_login = json.loads(response_login_username.data.decode())
    access_token = data_login['access_token']

    response_logout = client.post('/logout', headers={'Authorization': f'Bearer {access_token}'})

    assert response_logout.status_code == 200