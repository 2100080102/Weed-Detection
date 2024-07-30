from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import tensorflow as tf
import numpy as np
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = '12d96271e3d16c372e83ad437f36d50f'  # Set a secret key for session management

# Configure MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'my_database'

mysql = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load the TensorFlow model
model = tf.keras.models.load_model('D:\\Users\\acer\\PycharmProjects\\WeedDetection\\model\\my_model.keras')

# Define a mapping from class IDs to labels
class_id_to_label = {
    0: "Weed Not Present",
    1: "Weed Present",
    2: "Weed Present",
    3: "Weed Present",
    4: "Weed Not Present",
    5: "Weed Not Present",
    6: "Weed Present",
    7: "Weed Not Present",
    8: "Weed Not Present",
}

# Ensure the upload directory exists
UPLOAD_FOLDER = 'static/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Define user class
class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None


@app.route('/')
def index2():
    return render_template('index2.html')


@app.route('/Upload.html')
@login_required
def dashboard():
    return render_template('Upload.html')


@app.route('/AboutPage.html')
def about_page():
    return render_template('AboutPage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user[3], password):
            login_user(User(user[0], user[1], user[2], user[3]))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        existing_user = cur.fetchone()
        cur.close()

        if existing_user:
            flash('Email is already registered.')
            return render_template('signup.html')

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (name, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('Signup successful, please login')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Function to preprocess input image
def preprocess_image(image):
    image = image.resize((256, 256))  # Resize to match model's expected sizing
    image = np.asarray(image) / 255.0  # Normalize
    return image


# Function to predict image label
def predict(image):
    img_array = preprocess_image(image)
    img_array = np.expand_dims(img_array, axis=0)  # Expand dimensions for batch
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0], axis=-1)
    predicted_label = class_id_to_label.get(predicted_class, "Unknown")
    return predicted_label


@app.route('/predict', methods=['POST'])
@login_required
def predict_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Open the saved image file
        image = Image.open(file_path)
        label = predict(image)

        # Optionally, you can remove the file after prediction
        # os.remove(file_path)

        return jsonify({'result': label})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True)