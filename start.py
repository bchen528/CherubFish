#!/usr/bin/python3
from app import app, db
import sqlite3
import requests
from flask import Flask, request, abort, render_template
from hashlib import md5

@app.route('/', methods=['POST', 'GET'])
def create_url():

    if request.method == 'POST':
        url = request.form.get('url')
        #    response = requests.get(url)
        #   if response.status_code != 200:
        #      abort(400, "Invalid Website")
        short_url = md5(url.encode()).hexdigest()[-6:]
        with sqlite3.connect('app.db') as conn:
            cursor = conn.cursor()
            insert_row = """
               INSERT INTO Url (URL, SHORT_URL)
                   VALUES ('%s, %s')
               """%(url, short_url)
            result_cursor = cursor.execute(insert_row)
        return render_template('/test.html', short_url)
    return render_template('/test.html')

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
    app.run(host="0.0.0.0", port=5000)
