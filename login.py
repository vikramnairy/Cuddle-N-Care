from flask import *
import pyrebase
from Config import *
from firebase_admin import auth as firebase_auth


firebase = pyrebase.initialize_app(config)

# Get the Firebase Authentication service
auth = firebase.auth()

def login_post():
     
    email = request.form['email']
    password = request.form['password']
    try:
        if(email=="admin@gmail.com" and password == "admin@123"):
            session['admin']=email
            return redirect('/admin')
        user = auth.sign_in_with_email_and_password(email, password)
        session['user_id'] = user['localId']
   
        print("User signed in successfully!")
        return redirect('/service')
    except Exception as e:
        print("Error:", e)
      
        error_message = "Invalid email or password."
        
        return render_template('register.html', error=error_message)
    # email = request.form['email']
    # password = request.form['password']

    # try:
    #     # Special case for admin login
    #     if email == "admin@gmail.com" and password == "admin@123":
    #         session['admin'] = email
    #         print("success")
    #         return render_template('admin.html')

    #     # Regular user login
    #     user = auth.sign_in_with_email_and_password(email, password)
    #     session['user'] = user['localId']
    #     print("Login success")
    #     return redirect(url_for('service'))

    # except Exception as e:
    #     error_message = "Login failed. Please check your email and password."
    #     flash(error_message)
    #     print(f"Error: {e}")  # Print the error for debugging
    #     return redirect(url_for('login'))

# def login_post():
#     email = request.form['email']
#     password = request.form['password']

#     try:
#         if email == "admin@gmail.com" and password == "admin@123":
#             session['admin'] = email
#             return render_template('admin.html')

#         user = auth.sign_in_with_email_and_password(email, password)
#         session['user_id'] = user['localId']
#         print("Login success")
#         return redirect('/service')
#     except Exception as e:
#         error_message = "Login failed. Please check your email and password."
#         flash(error_message)
#         # return redirect('/login')
#         return render_template('register.html')



# def login_post():
#     email = request.form['email']
#     password = request.form['password']

#     try:
#         if(email=="admin1@gmail.com" and password =="admin@123"):
#             session['admin']=email
#             return redirect('/admin')
#         user = auth.sign_in_with_email_and_password(email, password)
#         session['user_id'] = user['localId']
   
#         print("User signed in successfully!")
#         # if(email=="admin@gmail.com" and password=="admin@123"):
#         #     session['admin']=email
#         #     return redirect(url_for('admin'))
            
#         # user = auth.sign_in_with_email_and_password(email, password)
#         # session['user'] = user['uid']  # Store user email in session
#         # print("login success")
#         return redirect(url_for('service'))
#         # # session['user'] = user.uid  # Store user ID in session
#         # return redirect(url_for('index'))  # Redirect to dashboard upon successful login
#     except Exception as e:
       
#         print("Error:", e)
      
#         error_message = "Invalid email or password."
        
#         return redirect(url_for('login'),error=error_message)
        
        
    
    
# def register_post():
#     email = request.form['email']
#     password = request.form['password']

#     try:
#         user = firebase_auth.create_user(
#             email=email,
#             password=password
#         )
#         print("Successfully registered user:", user.email)
#         return redirect(url_for('index'))  # Redirect to login page after successful registration
#     except Exception as e:
#         error_message = f"Registration failed: {str(e)}"
#         return render_template('register.html', error=error_message)

def register_post():
    email = request.form['email']
    password = request.form['password']

    try:
        user = auth.create_user_with_email_and_password(email, password)
        session['user'] = email  # Store user email in session after registration
        print("Successfully registered user:", user['email'])
        return redirect(url_for('index'))  # Redirect to index page after successful registration
    except Exception as e:
        error_message = f"Registration failed: {str(e)}"
        return render_template('register.html', error=error_message)
    
def forgot_password():
    email = request.form['email']
   
    
    try:
        
        auth.send_password_reset_email(email)

        return 'Password reset email sent successfully!'
    except Exception as e:
      
        # You can redirect the user to the forgot password page with an error message or return an error message
        return 'Error: ' + str(e)

def user_logout():
    if  session:
            print(session, "before")  
            session.clear() 
            print(session, "after") 
            return render_template('index.html')  

# def dashboard():
#     if 'user' in session:
#         return "Welcome to the dashboard!"
#     else:
#         return redirect('/')  # Redirect to login page if user is not logged in

# Dashboard page (protected route)
# @app.route('/dashboard')
# def dashboard():
#     if 'user' in session:
#         return "Welcome to the dashboard!"
#     else:
#         return redirect('/')  # Redirect to login page if user is not logged in

# Logout route
# @app.route('/logout')
# def logout():
#     session.pop('user', None)  # Remove user token from session
#     return redirect('/')  # Redirect to login page after logout

