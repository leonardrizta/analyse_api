import os
from flask import Flask, request, jsonify, send_file
from playfair import encrypt, decrypt
from steganography_lsb import encode, decode

app = Flask(__name__)
app.secret_key = "tubes_crypt_api"
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def main():
    return 'This is Analyse Team API for LSB and Playfair modification'


@app.route('/encrypt', methods=['POST'])
def encrypt_image():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No image in the request'})
        resp.status_code = 400
        return resp
    if 'plain_text' not in request.form:
        resp = jsonify({'message': 'No plain text in the request'})
        resp.status_code = 400
        return resp
    if 'key' not in request.form:
        resp = jsonify({'message': 'No key in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist('file')
    filename = "encrypted_image.png"
    errors = {}
    success = False
    for file in files:
        if file and allowed_file(file.filename):
            success = True
        else:
            errors["message"] = 'File type of {} is not allowed'.format(file.filename)
    cypher_text = encrypt(request.form.get('plain_text'), request.form.get('key'))
    image_file = UPLOAD_FOLDER + filename
    encode(cypher_text, image_file)
    if success:
        resp = jsonify({'endpoint': '/getimage'})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp


@app.route('/decrypt', methods=['POST'])
def decrypt_image():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No image in the request'})
        resp.status_code = 400
        return resp
    if 'key' not in request.form:
        resp = jsonify({'message': 'No key in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist('file')
    filename = "decrypted_image.png"
    errors = {}
    success = False
    for file in files:
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
    image_file = UPLOAD_FOLDER + filename
    binary_decode = decode(image_file).split()
    cypher_text = ''
    for char in binary_decode:
        cypher_text += chr(int(char, 2))
    plain_text = decrypt(cypher_text, "leo")
    if success:
        resp = jsonify({'plain_text': plain_text})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


@app.route('/getimage', methods=['GET'])
def get_image():
    return send_file(UPLOAD_FOLDER + "encrypted_image.png", mimetype='image/jpg')

if __name__ == '__main__':
    app.run(debug=True)
