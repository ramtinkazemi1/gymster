from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import Form, StringField, PasswordField, validators
from werkzeug.utils import secure_filename
from sqlalchemy import func
from uszipcode import SearchEngine
import os

app = Flask(__name__, static_folder='../frontend/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1130@localhost/gymster_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your database models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    street_address_1 = db.Column(db.String(100), nullable=False)
    street_address_2 = db.Column(db.String(100))
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'coach' or 'trainee'
    profile_picture = db.Column(db.String(255))

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

# Define a signup form with validation
class SignupForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=50)])
    last_name = StringField('Last Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Email(), validators.Length(min=6, max=120)])
    phone_number = StringField('Phone Number', [validators.Length(min=6, max=20)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=8)
    ])
    street_address_1 = StringField('Street Address 1', [validators.Length(min=1, max=100)])
    street_address_2 = StringField('Street Address 2', [validators.Optional(), validators.Length(max=100)])
    city = StringField('City', [validators.Length(min=1, max=50)])
    state = StringField('State', [validators.Length(min=1, max=50)])
    zipcode = StringField('Zip Code', [validators.Length(min=1, max=20)])
    country = StringField('Country', [validators.Length(min=1, max=50)])

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    data = request.json  # Retrieve data from the JSON request body

    phone_number = data.get('phone_number')
    password = data.get('password')

    print("Received phone number:", phone_number)  # Debug statement

    # Check if the user exists in the database
    user = User.query.filter(User.phone_number == phone_number).first()

    if user:
        print("User found in the database:", user)  # Debug statement

        # Check if the password matches
        if user.password == password:
            print("Password matched")  # Debug statement

            # Store user info in session for later access
            session['user_id'] = user.id

            # Redirect based on user type
            if user.user_type == 'trainee':
                print("Redirecting to member dashboard")  # Debug statement
                # Redirect to member dashboard
                return redirect(url_for('member_dashboard'))
            elif user.user_type == 'trainer':
                print("Redirecting to coach dashboard")  # Debug statement
                # Redirect to coach dashboard
                return redirect(url_for('coach_dashboard'))

    # Redirect to sign-in page with error message
    print("Authentication failed")  # Debug statement
    flash('Invalid phone number or password', 'error')
    return redirect(url_for('index'))


@app.route('/signup_success/<first_name>')
def signup_success(first_name):
    return render_template('signup_success.html', first_name=first_name)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        signup_type = request.form.get('signup-type')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        phone_number = form.phone_number.data
        password = form.password.data
        street_address_1 = form.street_address_1.data
        street_address_2 = form.street_address_2.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        country = form.country.data
        user_type = 'trainer' if signup_type == 'trainer' else 'trainee'

        # Store the user data in the database
        new_user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number,
                        password=password, street_address_1=street_address_1, street_address_2=street_address_2,
                        city=city, state=state, zipcode=zipcode, country=country, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()

        flash('You have successfully signed up!', 'success')

        return redirect(url_for('signup_success', first_name=first_name))

    return render_template('signup.html', form=form)


@app.route('/users')
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)


@app.route('/member-dashboard', methods=['GET', 'POST'])
def member_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = db.session.get(User, user_id)
        if user:
            if request.method == 'POST':
                # Check if the POST request contains file data
                if 'profile_picture' in request.files:
                    file = request.files['profile_picture']
                    if file.filename != '':
                        # Secure the filename to prevent directory traversal
                        filename = secure_filename(file.filename)
                        # Ensure the UPLOAD_FOLDER directory exists
                        upload_folder = app.config['UPLOAD_FOLDER']
                        os.makedirs(upload_folder, exist_ok=True)
                        # Print the file path before saving
                        print("File path before saving:", os.path.join(upload_folder, filename))
                        # Save the file to the designated directory
                        file.save(os.path.join(upload_folder, filename))
                        # Update the user's profile picture path in the database
                        user.profile_picture = 'uploads/' + filename
                        db.session.commit()
                        # Print the file path after saving
                        print("File path after saving:", os.path.join(upload_folder, filename))
            return render_template('member_dashboard.html', user=user)

    flash('You must be logged in to access this page', 'error')
    return redirect(url_for('index'))


@app.route('/profile-picture/<filename>')
def get_profile_picture(filename):
    # Construct the absolute path to the profile picture
    profile_picture_path = os.path.join(app.root_path, 'uploads', filename)
    # Serve the file to the client
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/coach-dashboard', methods=['GET', 'POST'])
def coach_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = db.session.get(User, user_id)
        if user:
            if request.method == 'POST':
                # Check if the POST request contains file data
                if 'profile_picture' in request.files:
                    file = request.files['profile_picture']
                    if file.filename != '':
                        # Secure the filename to prevent directory traversal
                        filename = secure_filename(file.filename)
                        # Ensure the UPLOAD_FOLDER directory exists
                        upload_folder = app.config['UPLOAD_FOLDER']
                        os.makedirs(upload_folder, exist_ok=True)
                        # Print the file path before saving
                        print("File path before saving:", os.path.join(upload_folder, filename))
                        # Save the file to the designated directory
                        file.save(os.path.join(upload_folder, filename))
                        # Update the user's profile picture path in the database
                        user.profile_picture = 'uploads/' + filename
                        db.session.commit()
                        # Print the file path after saving
                        print("File path after saving:", os.path.join(upload_folder, filename))
            return render_template('coach_dashboard.html', user=user)

    flash('You must be logged in to access this page', 'error')
    return redirect(url_for('index'))


@app.route('/search_coaches', methods=['POST'])
def search_coaches():
    if request.method == 'POST':
        # Retrieve the user's zipcode and selected radius from the form
        user_zipcode = request.form.get('zipcode')
        radius = int(request.form.get('radius'))

        # Query the database for coaches within the specified radius of the user's zipcode
        coaches_within_radius = User.query.filter(User.user_type == 'coach',
                                                  func.ST_DWithin(func.ST_SetSRID(func.ST_MakePoint(User.latitude, User.longitude), 4326),
                                                                  func.ST_SetSRID(func.ST_MakePoint(user_zipcode.latitude, user_zipcode.longitude), 4326),
                                                                  radius)).all()

        return render_template('member_dashboard.html', coaches=coaches_within_radius)




@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Define the upload folder for storing profile pictures
app.config['UPLOAD_FOLDER'] = 'uploads'

if __name__ == '__main__':
    app.run(debug=True)