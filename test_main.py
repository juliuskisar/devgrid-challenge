from main import app 

def test_index_route():
    app.test_client().get('/cache/clear')
    response = app.test_client().get('/')

    assert response.status_code == 404

def test_temperature_route():
    app.test_client().get('/cache/clear')
    response = app.test_client().get('/temperature/London')

    assert response.status_code == 200
    assert response.json["city"]["name"] == "London"

def test_fail_temperature_route():
    app.test_client().get('/cache/clear')
    response = app.test_client().get('/temperature/asdasdasdasdasdas')

    assert response.status_code == 503

def test_temperature_cached_route():
    app.test_client().get('/cache/clear')
    app.test_client().get('/temperature/London')
    app.test_client().get('/temperature/Paris')
    app.test_client().get('/temperature/Lisbon')
    response = app.test_client().get('/temperature?max=2')

    assert response.status_code == 200
    assert response.json["data"][0]["city"]["name"] == "Lisbon"
    assert response.json["data"][1]["city"]["name"] == "Paris"
    assert len(response.json["data"]) == 2