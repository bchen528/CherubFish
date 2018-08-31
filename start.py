#!/usr/bin/python3
import sqlite3
from sqlite3 import OperationalError
import requests
from flask import Flask, request, abort, render_template, redirect
from hashlib import md5

def table_check():
    create_table = """
        CREATE TABLE WEBSHORT(
        ID INT PRIMARY KEY,
        URL TEXT NOT NULL,
        SHORT TEXT NOT NULL
        );
        """
    with sqlite3.connect('urls.db') as db:
        cursor = db.cursor()
        try:
            cursor.execute(create_table)
        except OperationalError:
            pass

app = Flask(__name__)
app.url_map.strict_slashes = False
@app.route('/', methods=['POST', 'GET'])
def create_url():

    if request.method == 'POST':
        url = request.form['URL']
        print(url)
        #    response = requests.get(url)
        #   if response.status_code != 200:
        #      abort(400, "Invalid Website")
        short_url = md5(url.encode()).hexdigest()[-6:]
        with sqlite3.connect('urls.db') as conn:
            cursor = conn.cursor()
            insert_row = """
               INSERT INTO WEBSHORT (URL, SHORT)
                   VALUES ('%s','%s')
               """%(url, short_url)
            result_cursor = cursor.execute(insert_row)
        return render_template('test.html', short_url = short_url)
    return render_template('test.html')

'''@app.route('/<short_url>')
def redirect(short_url):
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        select_row = """
                SELECT URL FROM URL
                    WHERE short_url = short_url
                """%(short_url)
    result_cursor = cursor.execute(select_row)
    try:
        redirect_url = result_cursor.fetchone()[0]
    except:
        print('YOU FUCKED UP')

    return redirect(redirect_url)
'''
if __name__ == "__main__":
    table_check()
    app.run(debug=True, host='0.0.0.0', port=5000)
