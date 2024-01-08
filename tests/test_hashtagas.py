import json
from .client import client

def test_get_to_do_by_hashtag(client):
    response_register = client.post('/register', json={'username': 'boris', 'email': 'boris@boris.com', 'password': '123'})
    response_login_username = client.post('/login', json={'username': 'boris', 'email': '',  'password': '123'})

    data_login = json.loads(response_login_username.data.decode())
    access_token = data_login['access_token']

    response_create_to_do = client.post(
        '/user/todo',
        json={'to_do': 'td1',
              'date': '2024-01-01',
              'hashtags': [{'hashtag': 'hs1'}, {'hashtag': 'hs2'}]},
              headers={'Authorization': f'Bearer {access_token}'})
    
    response_create_to_do = client.post(
        '/user/todo',
        json={'to_do': 'td2',
              'date': '2024-01-01',
              'hashtags': [{'hashtag': 'hs1'}, {'hashtag': 'hs3'}]},
              headers={'Authorization': f'Bearer {access_token}'})
    

    response_get_todo_by_hashtag = client.get('/todo/hashtag?hashtag=hs1')
    data_todos = json.loads(response_get_todo_by_hashtag.data.decode())
    assert response_get_todo_by_hashtag.status_code == 200
    assert data_todos[0]['to_do'] == 'td1'
    assert data_todos[1]['to_do'] == 'td2'
    