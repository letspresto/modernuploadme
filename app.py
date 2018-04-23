import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
import subprocess
from random import choice
import json
import requests
from PIL import Image

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
		    flash('No file part')
		    return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
		    flash('No selected file')
		    return redirect(request.url)
		if file and allowed_file(file.filename):
		    filename = secure_filename(file.filename)
		    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		    return redirect(url_for('uploaded_file',
		    						filename=filename))
	return render_template('index.html')

@app.route('/show/<filename>', methods=['GET','POST'])
def uploaded_file(filename):
    response = run_bazel(filename)
    filename = 'http://127.0.0.1:5000/uploads/' + filename
    return render_template('index.html', filename=filename, caption=response)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# @app.route('/caption/<filename>', methods=['GET'])
def run_bazel(filename):

	cmd = ['im2txt/bazel-bin/im2txt/run_inference --checkpoint_path="im2txt/model.ckpt-3000000" --vocab_file="im2txt/word_counts.txt" --input_files="uploads/'+ filename + '"']
	# cmd = ['im2txt/bazel-bin/im2txt/run_inference --checkpoint_path="im2txt/model.ckpt-3000000" --vocab_file="im2txt/word_counts.txt" --input_files="uploads/festival.jpg"']

	p = subprocess.check_output(cmd, shell=True)
    # get the result
	result = str(p,'utf-8')
	result = result.split("0)")[1].split("(")[0].strip().split(".")[0].strip()

	return result
