from database import URL


def test_generate_short_code():
    short_code = URL.generate_short_code()
    assert len(short_code) == 6
    assert short_code.isalnum()


def test_url_model(db_session):
    url = URL(original_url='https://www.google.com', short_code='abcdef')
    db_session.add(url)
    db_session.commit()

    retrieved_url = db_session.query(URL).filter_by(short_code='abcdef').first()
    assert retrieved_url is not None
    assert retrieved_url.original_url == 'https://www.google.com'
    assert retrieved_url.short_code == 'abcdef'
