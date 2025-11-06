import firebase_admin
from firebase_admin import credentials, firestore, storage
from flask import Flask, render_template, request, url_for, session, redirect, jsonify
import os
from werkzeug.utils import secure_filename
import logging
from login import *

app = Flask(__name__)

# Initialize Firebase Admin SDK
service_account_path = "config/serviceAccountKey.json"
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'cuddlencare-63e0f.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()
app.secret_key = 'secret'

def get_pets_from_firestore():
    pets_ref = db.collection('pets')
    docs = pets_ref.stream()

    pets = []
    for doc in docs:
        pet = doc.to_dict()
        pets.append(pet)
    return pets

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files')
def files():
    pets = get_pets_from_firestore()
    last_pet = pets[-1] if pets else None
    return render_template('files.html', pet=last_pet)

@app.route('/helpline')
def helpline():
    if 'user' in session:
        user = session['user']
        return render_template('helpline.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        # Get other form data
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        location = request.form.get('location')
        village = request.form.get('village')
        address = request.form.get('address')

        # Upload file to Firebase Storage
        blob = bucket.blob(f'pets/{file.filename}')
        blob.upload_from_file(file)
        file_url = blob.public_url

        # Save metadata to Firestore
        doc_ref = db.collection('pets').document()
        doc_ref.set({
            'name': name,
            'phone_number': phone_number,
            'location': location,
            'village': village,
            'address': address,
            'file_url': file_url
        })
        return redirect(url_for('get_files'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/files', methods=['GET'])
def get_files():
    try:
        pets_ref = db.collection('pets')
        docs = pets_ref.stream()

        pets = []
        for doc in docs:
            pets.append(doc.to_dict())

        return render_template('files.html', pets=pets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def list_files_in_storage(directory='pets'):
    try:
        blobs = bucket.list_blobs(prefix=directory + '/')
        file_urls = [blob.public_url for blob in blobs if blob.exists()]
        logging.info(f"Successfully retrieved file URLs from {directory}/.")
        return file_urls
    except Exception as e:
        logging.error(f"Failed to list files in {directory}/: {e}")
        return []

@app.route('/list_files', methods=['GET'])
def list_files():
    file_urls = list_files_in_storage(directory='pets')
    return render_template('list_files.html', file_urls=file_urls)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    return register_post()

@app.route('/login')
def login():
    return redirect(url_for('service'))

@app.route('/login', methods=['POST'])
def login_post():
    return login_post()

@app.route('/admin')
def admin():
    if 'admin' in session:
        return render_template('admin.html')
    else:
        return render_template('register.html')

@app.route('/service')
def service():
    if 'user' in session:
        user = session['user']
        return render_template('service.html', user=user)
    else:
        return redirect(url_for('register'))

@app.route('/success')
def success():
    return "Registration successful"

@app.route('/reset', methods=['POST'])
def forgot_password():
    return forgot_password()

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin@123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error_message = "Invalid username or password"
            return render_template('admin_login.html', error=error_message)
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    pets = get_pets_from_firestore()
    return render_template('admin_dashboard.html', pets=pets)

@app.route('/admin/add_pet', methods=['GET', 'POST'])
def add_pet():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        address = request.form['address']
        file_url = request.form['file_url']
        pet = {
            'name': name,
            'phone_number': phone_number,
            'address': address,
            'file_url': file_url
        }
        db.collection('pets').add(pet)
        return redirect(url_for('admin_dashboard'))
    return render_template('add_pet.html')

@app.route('/admin/delete_pet/<pet_id>', methods=['POST'])
def delete_pet(pet_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    db.collection('pets').document(pet_id).delete()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
