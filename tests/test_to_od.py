import json
from .client import client

def test_create_to_do(client):
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
    
    data_to_do = json.loads(response_create_to_do.data.decode())
    assert response_create_to_do.status_code == 201
    assert data_to_do['id'] == '1'
    assert data_to_do['username'] == 'boris'
    assert data_to_do['email'] == 'boris@boris.com'
    assert data_to_do['todos'][0]['to_do'] == 'td1'
    assert data_to_do['todos'][0]['hashtags'][0]['hashtag'] == '#hs1'
    assert data_to_do['todos'][0]['hashtags'][1]['hashtag'] == '#hs2'
    to_do_id = data_to_do['todos'][0]['id']

    response_get_to_do_by_id = client.get(f'/user/todo/{to_do_id}',
                                          headers={'Authorization': f'Bearer {access_token}'})
    
    assert response_get_to_do_by_id.status_code == 200
    data_to_do = json.loads(response_get_to_do_by_id.data.decode())
    assert data_to_do['id'] == 1
    assert data_to_do['to_do'] == 'td1'
    assert data_to_do['date'] == '2024-01-01'
    assert data_to_do['user_id'] == 1

    response_change_to_do = client.put(f'/user/todo/{to_do_id}',
                                       json={'to_do': 'td1',
                                            'date': '2024-01-01',
                                            'hashtags': [{'hashtag': 'hs1'}, {'hashtag': 'hs3'}]},
                                       headers={'Authorization': f'Bearer {access_token}'})
    
    
    data_to_do = json.loads(response_change_to_do.data.decode())

    assert response_change_to_do.status_code == 200
    assert data_to_do['to_do'] == 'td1'
    assert data_to_do['hashtags'][1]['hashtag'] == '#hs3'

    response_change_to_do = client.put(f'/user/todo/{2}',
                                       json={'to_do': 'td1',
                                            'date': '2024-01-01',
                                            'hashtags': [{'hashtag': 'hs11'}, {'hashtag': 'hs31'}]},
                                       headers={'Authorization': f'Bearer {access_token}'})
    
    
    data_to_do = json.loads(response_change_to_do.data.decode())

    assert response_change_to_do.status_code == 200
    assert data_to_do['to_do'] == 'td1'
    assert data_to_do['hashtags'][1]['hashtag'] == '#hs31'

    response_hashtags = client.get('/hashtag')

    data_hashtags = json.loads(response_hashtags.data.decode())
    assert data_hashtags[0]['hashtag'] == '#hs1'
    assert data_hashtags[1]['hashtag'] == '#hs2'
    assert data_hashtags[2]['hashtag'] == '#hs3'
    assert data_hashtags[3]['hashtag'] == '#hs11'

    response_delete_to_do = client.delete(f'/user/todo/{2}',
                                          headers={'Authorization': f'Bearer {access_token}'})
    
    assert response_delete_to_do.status_code == 200
    data_to_do = json.loads(response_delete_to_do.data.decode())
    assert data_to_do['message'] == 'ToDo is deleted!'

    response_to_do_not_found = client.get(f'/todo/3',
                                          headers={'Authorization': f'Bearer {access_token}'})
    
    assert response_to_do_not_found.status_code == 404

