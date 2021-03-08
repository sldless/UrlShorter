from flask import Flask, redirect, request, render_template
app = Flask(__name__)
import random
import string
import sqlite3, time, config
sql = sqlite3.connect('sqlite.db', check_same_thread=False)
db = sql.cursor()


@app.route('/', methods = ["GET", "POST"])
def index():
  if request.method == "POST":
    # Create an url id / url (table)
    db.execute('''CREATE TABLE IF NOT EXISTS urls (url_id, url)''')
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@$%^&*()-_=+[{]}|;:<.>?`~"
    #Create the random strings
    random_id = ''.join([random.choice(chars) for i in range(20)])
    ab  =random_id
    # This inserts random strings / url
    db.execute(f"INSERT INTO urls VALUES ('{ab}', '{request.form['url']}')")
    # Save the strings / url
    sql.commit()
    context = {
      'cfg': config,
      'url_id': ab
    }
    db.execute(f"INSERT INTO urls VALUES ('NotARickroll', 'https://youtu.be/dQw4w9WgXcQ')")
    sql.commit()
    return render_template('index.html', **context)
  else:
    return render_template('index.html') 
@app.route('/<url_id>')
def url_id(url_id):
  thing =  db.execute("SELECT url_id, url FROM urls")
  if thing:
    for row in db:
        print(row)
    if row[1].find("http://") != 0 and row[1].find("https://") != 0:
        url = "http://" + row[1]
        return redirect(url)
    else:
      return redirect(row[1])
  else:
    return redirect("/")
if __name__ == '__main__':
    app.run(debug=True)