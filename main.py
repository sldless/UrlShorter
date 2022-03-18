from flask import Flask, redirect, request, render_template, url_for
app = Flask(__name__)
import random
import sqlite3
sql = sqlite3.connect('urls.sqlite', check_same_thread=False)
db = sql.cursor()
@app.route('/post', methods=["POST"])
def POSTURL():
  if request.method == "POST":
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_id = ''.join([random.choice(chars) for i in range(9)])
    db.execute("INSERT INTO urls (id, url) VALUES (?, ?)", (random_id, request.form['url']))
    sql.commit()
    return redirect(url_for('index', uri_id=random_id))
@app.route('/', methods=["GET"])
def index():
  uri_id = request.args.get('uri_id')
  db.execute('''CREATE TABLE IF NOT EXISTS urls (id, url)''')
  data =db.execute("SELECT * FROM urls WHERE id = ?", (uri_id,)).fetchone()
  sql.commit()
  if request.method == "GET":
    if uri_id:
      return render_template('index.html', data=data)
  return render_template('index.html', data=data)
@app.route('/s/<uri_id>')
def GETURL(uri_id):
  data = db.execute("SELECT * FROM urls WHERE id = ?", (uri_id,)).fetchone()
  sql.commit()
  if data != None:
    return redirect(data[1])
  return redirect("/")
if __name__ == '__main__':
  app.run(debug=True)