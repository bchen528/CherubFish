#!/usr/bin/python3
"App module"
from flask import Flask, request, redirect, make_response, jsonify, Response, abort, render_template
import os
import requests
from flask_cors import CORS
from dbs import storage
from urlshort import urlshort
from base_entry import ShortURL
from emailentry import Email

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def tear_down(self):
    "tears down"
    storage.close()


@app.errorhandler(404)
def not_found(error):
    "error handler for 404"
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/', strict_slashes=False, methods=['GET', 'POST'])
def testshort():
    if request.method == 'POST':
        try:
            email = request.form['Email']
            obj = {'address': email}
            b = Email(**obj)
            b.save()
            return render_template('index.html')
        except:
            pass
        try:
            url = request.form['URL']
            if not url.startswith('http'):
                url = 'http://'+ url
            try:
                response = requests.get(url)
            except:
                abort(400, "BAD URL")
            #make a short url hash that will be the short url
            #havent dealt with collisions yet
            short = urlshort(url)
            #add to db
            att = {'urlhash':short, 'actualurl':url}
            a = ShortURL(**att)
            a.save()
            print(short)
            return render_template('index.html', short_url=short)
        except:
            pass
    return render_template('index.html')

@app.route('/<string:shorturl>', strict_slashes=False, methods=['GET'])
def testshort2(shorturl):
    #look up in db
    target = storage.get(shorturl)
    if target:
        return redirect(target.actualurl)
    else:
        return "BORKED"

if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST") if os.getenv("HBNB_API_HOST")
            else "0.0.0.0",
            port=int(
                os.getenv("HBNB_API_PORT")) if os.getenv("HBNB_API_PORT")
            else 5000, threaded=True, debug=True)
