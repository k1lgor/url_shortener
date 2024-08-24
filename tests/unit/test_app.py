import re


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'URL Shortener' in response.data


def test_shorten_url_valid(client, db_session):
    response = client.post('/shorten', data={'url': 'https://google.com'})
    assert response.status_code == 200
    assert 'Shortened URL' in response.data.decode('utf-8')
    assert 'Copy to Clipboard' in response.data.decode('utf-8')


def test_shorten_url_invalid(client):
    response = client.post('/shorten', data={'url': 'not_a_valid_url'})
    assert response.status_code == 400
    assert 'Invalid URL' in response.data.decode('utf-8')


def test_redirect_to_url(client, db_session):
    # First, create a shortened URL
    response = client.post('/shorten', data={'url': 'https://www.example.com'})
    assert response.status_code == 200

    # Extract the short code from the response
    response_text = response.data.decode('utf-8')
    match = re.search(r'href="([^"]+)"', response_text)
    assert match, "Shortened URL not found in response"

    short_url = match.group(1)
    short_code = short_url.split('/')[-1]

    # Now, try to access the shortened URL
    response = client.get(f'/{short_code}')
    assert response.status_code == 302
    assert response.location == 'https://www.example.com'
