from flask import Flask, render_template
from flask import request, redirect, session, url_for
from flask import flash
from werkzeug.utils import secure_filename
import os
import subprocess
import datetime
import shutil

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.secret_key = 'A0Zr98j/dfdafdafdfa'
from config import *

def get_user():
  if 'user' in session:
    return session['user'], NAMES[session['user']]
  return None, None

@app.route('/logout')
def logout():
  session.pop('user', None)
  flash('Logout ok')
  return redirect(url_for('main'))

@app.route('/login', methods=['POST'])
def login():
  ps = request.form['password']
  if ps in PASSWD:
    session['user'] = PASSWD[ps]
    flash('Login ok')
  else:
    flash('Bad password')
  return redirect(url_for('main'))

@app.route('/upload', methods=['POST'])
def upload():
  user, name = get_user()
  if user == None:
    return redirect(url_for('main'))

  if not os.path.exists("uploads/%d/" % user):
    os.makedirs("uploads/%d/" % user)
  if not os.path.exists("players/"):
    os.makedirs("players/")
  file = request.files['file']
  if file:
    filename = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.au")
    print filename
    file.save(("uploads/%d/" % user) + filename)

    errors = ""
    bad = False
    args = ["python", "compile_game.py", "all", "uploads/%d/%s" % (user, filename)] 
    rr = subprocess.Popen(args,stdout = subprocess.PIPE, stderr=subprocess.STDOUT)

    output, error = rr.communicate()
    error = rr.returncode
    if error != 0:
      flash("Errors during compilation")
      flash(output, "error")
    else:
      shutil.copy("uploads/%d/%s" % (user, filename), "players/%d.au" % user) 
      flash("Upload ok")
  return redirect(url_for('main'))
     

@app.route('/')
def main():
  user, name = get_user()
  return render_template('index.html', user=user, name=name)


if __name__ == '__main__':
  app.run(debug=True)

