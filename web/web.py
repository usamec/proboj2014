from flask import Flask, render_template
from flask import request, redirect, session, url_for
from flask import flash, send_file
from werkzeug.utils import secure_filename
import os
import subprocess
import datetime
import shutil

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.secret_key = 'A0Zr98j/dfdafdafdfa'
from local_config import *

def get_user():
  if 'user' in session:
    files = sorted(os.listdir("uploads/%s" % session['user']), reverse=True)
    return session['user'], NAMES[session['user']], files
  return None, None, None

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
    
def get_scores():
  if os.path.exists("logs/scores.txt"):
    f = open("logs/scores.txt")
    scores = {NAMES[i]: int(x) for i,x in enumerate(f)}
    f.close()
  else:
    scores = {x: 0 for x in NAMES}
  return scores

def get_last_games():
  logs = sorted(filter(lambda x: x.endswith('.log') or x.endswith('.log.gz'), os.listdir("logs")), reverse=True)[:3]
  logs = [x[:-4] if x.endswith('.log') else x[:-7] for x in logs]
  last_games = []
  for log in logs:
    f = open("logs/%s.log.scr" % log)
    scores = {NAMES[i]: int(x) for i,x in enumerate(f)}
    f.close()
    last_games.append({"name": log, "scores": scores})

  return last_games

def get_all_games():
  logs = sorted(filter(lambda x: x.endswith('.log') or x.endswith('.log.gz'), os.listdir("logs")), reverse=True)
  logs = [x[:-4] if x.endswith('.log') else x[:-7] for x in logs]
  last_games = []
  for log in logs:
    f = open("logs/%s.log.scr" % log)
    scores = {NAMES[i]: int(x) for i,x in enumerate(f)}
    f.close()
    last_games.append({"name": log, "scores": scores})

  return last_games

@app.route('/get_upload/<file>')
def get_upload(file):
  if os.path.exists("uploads/%s/%s" % (session['user'], file)):
    return send_file("uploads/%s/%s" % (session['user'], file),
                     as_attachment=True, attachment_filename=file)
  else:
    return "ty si chudak!"

@app.route('/downgame/<game>')
def downgame(game):
  if os.path.exists("logs/%s.log.gz" % game):
    return send_file("logs/%s.log.gz" % game, as_attachment=True,
                     attachment_filename="%s.log.gz" % game) 
  if os.path.exists("logs/%s.log" % game):
    return send_file("logs/%s.log" % game, as_attachment=True,
                     attachment_filename="%s.log" % game) 
  else:
    return "ty si chudak!"

@app.route('/')
def main():
  user, name, files = get_user()
  print files
  return render_template('index.html', user=user, name=name, scores=get_scores(),
                         last_games=get_last_games(), files=files)

@app.route('/all_games')
def all_games():
  return render_template('allgames.html', scores=get_scores(),
                         games=get_all_games())


if __name__ == '__main__':
  app.run(debug=True, host='10.47.42.1')

