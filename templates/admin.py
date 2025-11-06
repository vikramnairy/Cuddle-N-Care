from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Example data
pets = [
    {"id": 1, "name": "Max", "phone_number": "123-456-7890", "address": "123 Main St", "file_url": "#"},
    {"id": 2, "name": "Bella", "phone_number": "987-654-3210", "address": "456 Elm St", "file_url": "#"},
    # Add more pets
]

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    search_query = request.args.get('search')
    filtered_pets = pets
    if search_query:
        filtered_pets = [pet for pet in pets if search_query.lower() in pet['name'].lower()]
    return render_template('admin_dashboard.html', pets=filtered_pets)

@app.route('/add_pet', methods=['POST'])
def add_pet():
    global pets
    new_id = max(pet['id'] for pet in pets) + 1 if pets else 1
    new_pet = {
        "id": new_id,
        "name": request.form['name'],
        "phone_number": request.form['phone_number'],
        "address": request.form['address'],
        "file_url": request.form['file_url']
    }
    pets.append(new_pet)
    return redirect(url_for('admin'))

@app.route('/delete_pet/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    global pets
    pets = [pet for pet in pets if pet['id'] != pet_id]
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
