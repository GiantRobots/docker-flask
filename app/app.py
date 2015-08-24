from flask import Flask, redirect, make_response, request
import random
app = Flask(__name__)

@app.route('/')
def index():
    redirect_to_index = redirect('/lolcats/')
    response = make_response( redirect_to_index )
    response.set_cookie('zone', value=str(random.randint(1, 2)))
    return response


@app.route('/lolcats/')
def lolcats():
    return 'Zone Cookie = ' + request.cookies.get('zone', 0)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
