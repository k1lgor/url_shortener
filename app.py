import validators
from flask import Flask, render_template, request, jsonify, redirect

from database import Session, URL

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten():
    # get the original URL from the form data
    original_url = request.form['url']

    if not validators.url(original_url):
        return '<p class="error">Invalid URL</p>', 400

    session = Session()

    while True:
        short_code = URL.generate_short_code()
        if not session.query(URL).filter_by(short_code=short_code).first():
            break

    new_url = URL(original_url=original_url, short_code=short_code)
    session.add(new_url)
    session.commit()

    short_url = request.url_root + short_code
    return f'''
        <p>Shortened URL: <a href="{short_url}" class="short-url" target="_blank">{short_url}</a></p>
        <button class="copy-btn" data-clipboard-text="{short_url}">Copy to Clipboard</button>
        <button class="go-back-btn" hx-get="/" hx-target="body">Go Back</button>
        '''


@app.route('/<short_code>')
def redirect_to_url(short_code):
    session = Session()
    url_obj = session.query(URL).filter_by(short_code=short_code).first()

    if url_obj:
        return redirect(url_obj.original_url, code=302)
    return jsonify({'error': 'URL not found'}), 404


if __name__ == '__main__':
    app.run()
