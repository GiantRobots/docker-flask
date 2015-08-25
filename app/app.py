from flask import Flask, redirect, make_response, request
import random
import requests
import datetime
app = Flask(__name__)

base_url = "http://10.80.1.69/"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):

    try:
        zone_cookie = request.cookies.get('zone', 0)
        url_fetch = request.url.replace(request.url_root, base_url)

        if zone_cookie != 0:
            response = make_response(requests.get(url_fetch).text)
            response.headers["Cookie"] = request.headers.get("Cookie", "")

            return response
        else:
            redirect_to_index = redirect('/')
            response = make_response(redirect_to_index)
            response.set_cookie('zone', value=str(random.randint(1, 2)))

            response.headers['Last-Modified'] = datetime.now()
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, ' \
                                                'post-check=0, pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'

            return response
    except Exception as e:
        return str(e)


@app.route('/killcookie/')
def kill_cookie():
    response = make_response()
    response.set_cookie('zone', '', expires=0)
    return response


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
