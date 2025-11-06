import firebase_admin.storage
from flask import Flask, render_template, request,url_for,session,redirect
import firebase_admin

from firebase_admin import credentials, firestore, storage
from flask import Flask, request, jsonify
import os

import os
from werkzeug.utils import secure_filename
import logging
from flask_session import Session
from login import *
from flask_mail import Mail,Message








app = Flask(__name__)
app.secret_key='jai ho'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

# Initialize Firebase Admin SDK
service_account_path ="C:/Users/Dell/Downloads/latest (3)/latest/CuddleNCare/config/serviceAccountKey.json"

cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'cuddlencare-63e0f.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()
app.secret_key = 'secret' 

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/')
# def index():
#     return render_template('index.html')

# def get_pets_from_firestore():
#     pets_ref = db.collection('pets')
#     docs = pets_ref.stream()

#     pets = []
#     for doc in docs:
#         pet = doc.to_dict()
#         pets.append(pet)
#     return pets

@app.route('/')
def index():
    # if 'user' in session:
    #     user = session['user']
      
    # else:
        return render_template('index.html')

def get_pets_from_firestore():
    pets_ref = db.collection('pets')
    pets = [doc.to_dict() for doc in pets_ref.stream()]
    return pets

@app.route('/files')
def files():
    pets = get_pets_from_firestore()  # Fetch pets from Firestore
    last_pet = pets[-1] if pets else None  # Get the last pet
    return render_template('files.html',  pet=last_pet)
    

@app.route('/helpline')
def helpline():
    if 'user_id' in session:
         
        user = session['user_id']
        return render_template('helpline.html', user=user)
    else:
        return redirect(url_for('login'))
        
    



@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return 'No file part', 400
            file = request.files['file']
            if file.filename == '':
                return 'No selected file', 400
            
            # Inspect form data
            form_data = {k.strip(): v for k, v in request.form.items()}
            print("Cleaned form data:", form_data)

            # Retrieve cleaned data
            name = form_data.get('name')
            phone = form_data.get('phone_number')
            location = form_data.get('location')
            village = form_data.get('village')
            address = form_data.get('address')
            
            # Debugging statements to check form data
            print(f'name: {name}')
            print(f'phone_number: {phone}')
            print(f'location: {location}')
            print(f'village: {village}')
            print(f'address: {address}')

            print(request.form)

            # Secure the filename
            filename = secure_filename(file.filename)

            # Upload file to Firebase Storage
            blob = bucket.blob(f'pets/{filename}')
            blob.upload_from_file(file)
            file_url = blob.public_url

            # Save metadata to Firestore
            db.collection('pets').document().set({
                'name': name,
                'phone_number': phone,
                'location': location,
                'village': village,
                'address': address,
                'file_url': file_url
                
            })
            return redirect(url_for('files'))
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return render_template('upload.html')

def get_all_users():
    """Retrieves all users from Firebase Authentication and returns them as JSON."""
    try:
        users = []
        page = auth.list_users()
        while page:
            for user in page.users:
                user_data = {
                    "uid": user.uid,
                    "email": user.email,
                    "displayName": user.display_name,
                    
                }
                users.append(user_data)
            page = page.get_next_page()

        return jsonify(users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route('/filess', methods=['GET'])
def get_files():
    try:
        pets_ref = db.collection('pets')
        docs = pets_ref.stream()

        pets = []
        for doc in docs:
            pets.append(doc.to_dict())

        return render_template('display.html', pets=pets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



#


    
def list_files_in_storage(directory='pets'):
    try:
        blobs = bucket.list_blobs(prefix=directory + '/')
        file_urls = [blob.public_url for blob in blobs if blob.exists()]
        logging.info(f"Successfully retrieved file URLs from {directory}/.")
        return file_urls
    except Exception as e:
        logging.error(f"Failed to list files in {directory}/: {e}")
        return []

# Route to display files
@app.route('/list_files', methods=['GET'])
def list_files():
    file_urls = list_files_in_storage(directory='pets')
    return render_template('list_files.html', file_urls=file_urls)




# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'gs://cuddlencare-63e0f.appspot.com'
# })
# bucket = storage.bucket()

# Function to upload a file to Firebase Storage


# # home page
# @app.route('/')
# def index():
#     return render_template('helpline.html')



@app.route('/register')
def register():
    return render_template('register.html')

# Route to handle form submission
@app.route('/register', methods=['POST'])
def registerr():
    return register_post()

# handling login submission
# @app.route('/login')
# def login():
#      return redirect('loginn')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        return login_post()
    return redirect('login')

# @app.route('/login',methods=['POST',])
# def loginn():
#      return login_post()
def get_all_pets():
    # Your logic to get all pets from Firestore or Firebase Realtime Database
    pass

@app.route('/admin')
def admin():
    if 'admin' in session:
        user_list = get_all_users()
        pet_list = get_pets_from_firestore()
        print(user_list)
        return render_template('admin.html', users=user_list,pets=pet_list)
      
    else: 
        return render_template('register.html')
    
@app.route('/delete_pet/<pet_id>', methods=['POST'])
def delete_pet(pet_id):
    
    print(f"Attempting to delete pet with ID: {pet_id}")
    try:
        db.collection('pets').document(pet_id).delete()
        print(f"Successfully deleted pet with ID: {pet_id}")
        return redirect(url_for('admin'))
    except Exception as e:
        print(f"Error deleting pet: {e}")
        return redirect(url_for('admin'))


    

    return redirect(url_for('login'))

# @app.route('/admin')
# def admin_dashboard():
#     user_list = get_all_users()
#     pet_list = get_all_pets()
#     print(user_list)
#     return render_template('admin.html', users=user_list, pets=pet_list)


@app.route('/service')
def service():
    logged_in = 'user_id' in session 
    # user_name = session.get('user_name', 'Logged in')
    print(logged_in)
    return render_template('service.html', logged_in=logged_in)

    # if 'user' in session:
    #     user = session['user']
    #     return render_template('service.html', user=user)
    # else:
    #     return render_template('register.html')
        
     

@app.route('/success')
def success():
    return "Registration successful"



@app.route('/reset',methods=['POST'])
def forgot():
     return forgot_password()

@app.route('/logout', methods=['POST', 'GET'])
def logoutt():
    print(session,"be")
    return user_logout()



            


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboardd():
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

# @app.route('/admin/delete_pet/<pet_id>', methods=['POST'])
# def delete_pet(pet_id):
#     if 'admin' not in session:
#         return redirect(url_for('admin_login'))
#     db.collection('pets').document(pet_id).delete()
#     return redirect(url_for('admin_dashboard'))




# @app.route('/dashboard')
# def dashboard():
#     # if 'user' in session:
#     #     return "Welcome to the dashboard!"
#     # else:
#      return render_template('/') 

# @app.route('/signin')
# def signup():
#     return sign_in()


# Access the auth object from the firebase instance




if __name__ == '__main__':
    app.run(debug=True)

