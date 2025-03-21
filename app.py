from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    package_name = db.Column(db.String(120), nullable=False)
    package_version = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    main_file = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    packages = Package.query.all()
    return render_template('index.html', packages=packages)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username already exists"}), 409
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return redirect(url_for('index'))
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    return render_template('login.html')

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        username = request.form['username']
        package_name = request.form['package_name']
        package_version = request.form['package_version']
        description = request.form['description']
        main_file = request.form['main_file']
        
        if not main_file.endswith('.mine') and not main_file.endswith('.mn'):
            return jsonify({"message": "Main file must have a .mine or .mn extension"}), 400
        
        new_package = Package(username=username, package_name=package_name, package_version=package_version, description=description, main_file=main_file)
        db.session.add(new_package)
        db.session.commit()
        
        return jsonify({"message": "Package published successfully!"}), 201
    return render_template('publish.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)