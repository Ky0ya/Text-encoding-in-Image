from flask import Flask, render_template, request, redirect, send_from_directory
from new import encode, decode
import cv2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt_page():
    if request.method == 'POST':
        file = request.files['image']
        text = request.form['text']
        if file and text:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            image = cv2.imread(filepath)
            updated_filename = encode(image, text, filepath)
            return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.basename(updated_filename), as_attachment=True)
    
    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt_page():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            image = cv2.imread(filepath)
            decrypted_text = decode(image)
            return render_template('decrypt.html', text=decrypted_text)
    
    return render_template('decrypt.html', text=None)

if __name__ == '__main__':
    app.run(debug=True)