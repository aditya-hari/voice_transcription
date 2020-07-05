import os
import wave
import numpy as np
import json 

from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

import spacy
from deepspeech import Model
from utils import get_text, get_entities

UPLOAD_FOLDER = 'audios'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_page():
    return render_template('frontpage.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav'))
            return redirect('/transcript')
    return render_template('home.html')

@app.route('/transcript', methods=['GET', 'POST'])
def text_from_audio():
    fin = wave.open('audios/audio.wav')
    text = get_text(fin)
    if request.method == 'POST':
        text = request.form['transcript']
        return show_form(text)
    return render_template('transcript.html', message=text)

@app.route('/saveform', methods=['POST'])
def saveform():
    form = request.form
    with open('result.json', 'w') as f:
        json.dump(form, f)
    return render_template('done.html')
    
@app.route('/help')
def howitworks():
    return render_template('howitworks.html')
    
def show_form(text):
    data = get_entities(text)
    return render_template("finalform.html", data=data)
    