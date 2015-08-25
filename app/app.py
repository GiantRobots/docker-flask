from flask import Flask, redirect, make_response, request
import random
import urllib
app = Flask(__name__)

base_url = "http://todaysinfo.net/"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):

    zone_cookie = request.cookies.get('zone', 0)
    url_fetch = request.url.replace(request.url_root, base_url)

    if zone_cookie != 0:
        return urllib.urlopen(url_fetch).read()
    else:
        redirect_to_index = redirect('/')
        response = make_response(redirect_to_index)
        response.set_cookie('zone', value=str(random.randint(1, 2)))
        return response


@app.route('/killcookie/')
def kill_cookie():
    response = make_response();
    response.set_cookie('zone', '', expires=0)
    return response


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

#/top-15-reasons-hillary-clinton-is-the-worst-mistake-for-president-even-for-liberals/
