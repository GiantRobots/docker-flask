from flask import Flask, redirect, make_response, request, Response, abort, render_template
import random
import requests
import datetime
import logging
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
CHUNK_SIZE = 1024
LOG = logging.getLogger("main.py")

base_url = "http://10.80.1.69:81/"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):

    try:
        zone_cookie = request.cookies.get('zone', 0)
        url_fetch = request.url.replace(request.url_root, base_url)

        if zone_cookie != 0:
            #response = Response() #make_response(requests.get(url_fetch, stream=True).text)
            #response.headers["Cookie"] = request.headers.get("Cookie", "")
            #response.headers["HTTP_X_FORWARDED_HOST"] = 'http://radnews.net'
            returnstuff = proxy(url_fetch)
            return returnstuff
        else:
            redirect_to_index = redirect('/')
            response = make_response(redirect_to_index)
            response.set_cookie('zone', value=str(random.randint(1, 2)))

            response.headers['Last-Modified'] = datetime.datetime.now()
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


def proxy(url):
    """Fetches the specified URL and streams it out to the client.

    If the request was referred by the proxy itself (e.g. this is an image fetch for
    a previously proxied HTML page), then the original Referer is passed."""
    r = get_source_rsp(url)
    LOG.info("Got %s response from %s",r.status_code, url)
    headers = dict(r.headers)

    return Response(r.raw.read(), headers=headers)


def get_source_rsp(url):
    LOG.info("Fetching %s", url)
    # Ensure the URL is approved, else abort

    # Pass original Referer for subsequent resource requests
    proxy_ref = proxy_ref_info(request)
    headers = { "Referer" : "http://%s/%s" % (proxy_ref[0], proxy_ref[1])} if proxy_ref else {}
    # Fetch the URL, and stream it back
    LOG.info("Fetching with headers: %s, %s", url, headers)
    return requests.get(url, stream=True , params = request.args, headers=headers)



def split_url(url):
    """Splits the given URL into a tuple of (protocol, host, uri)"""
    proto, rest = url.split(':', 1)
    rest = rest[2:].split('/', 1)
    host, uri = (rest[0], rest[1]) if len(rest) == 2 else (rest[0], "")
    return (proto, host, uri)


def proxy_ref_info(request):
    """Parses out Referer info indicating the request is from a previously proxied page.

    For example, if:
        Referer: http://localhost:8080/p/google.com/search?q=foo
    then the result is:
        ("google.com", "search?q=foo")
    """
    ref = request.headers.get('referer')
    if ref:
        _, _, uri = split_url(ref)
        if uri.find("/") < 0:
            return None
        first, rest = uri.split("/", 1)
        if first in "pd":
            parts = rest.split("/", 1)
            r = (parts[0], parts[1]) if len(parts) == 2 else (parts[0], "")
            LOG.info("Referred by proxy host, uri: %s, %s", r[0], r[1])
            return r
    return None


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
