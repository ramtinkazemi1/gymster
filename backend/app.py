from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import Form, StringField, PasswordField, validators
from werkzeug.utils import secure_filename
from sqlalchemy import func
from uszipcode import SearchEngine
import os
from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2

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
    
    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'street_address_1': self.street_address_1,
            'street_address_2': self.street_address_2,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'country': self.country,
            'user_type': self.user_type,
            'profile_picture': self.profile_picture
        }

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
        try:
            # Initialize the search engine
            search = SearchEngine()

            # Retrieve the user's zipcode and selected radius from the form
            user_zipcode = request.json.get('zipcode')
            radius = int(request.json.get('radius'))

            if user_zipcode is not None and radius is not None:
                print("User Zip Code:", user_zipcode)
                result = search.by_zipcode(user_zipcode)
                user_lat = result.lat
                user_lng = result.lng
                
                print("User Latitude:", user_lat)
                print("User Longitude:", user_lng)
                
                # Query the database for coaches within the specified radius of the user's zipcode
                coaches_within_radius = User.query.filter(User.user_type == 'trainer').all()
                print("Coaches retrieved from the database:", coaches_within_radius)
                
                # Filter coaches based on the distance from the user
                coaches_within_radius = [coach for coach in coaches_within_radius if calculate_distance(user_zipcode, coach.zipcode) <= radius]
                print("Coaches within the specified radius:", coaches_within_radius)
                
                # Serialize the coaches to JSON along with distance
                serialized_coaches = [{
                    'id': coach.id,
                    'first_name': coach.first_name,
                    'last_name': coach.last_name,
                    'email': coach.email,
                    'phone_number': coach.phone_number,
                    'street_address_1': coach.street_address_1,
                    'street_address_2': coach.street_address_2,
                    'city': coach.city,
                    'state': coach.state,
                    'zipcode': coach.zipcode,
                    'country': coach.country,
                    'user_type': coach.user_type,
                    'profile_picture': coach.profile_picture,
                    'distance': round(calculate_distance(user_zipcode, coach.zipcode), 1) 
                } for coach in coaches_within_radius]

                # Return JSON response
                return jsonify(coaches=serialized_coaches)
            else:
                # Return error message if zipcode or radius is missing
                return jsonify(error='Zipcode or radius is null or empty'), 400
        except Exception as e:
            print("Error:", e)
            return jsonify(error=str(e)), 500



def calculate_distance(user_zipcode, coach_zipcode):
    # Get the latitude and longitude of the user's zipcode
    search = SearchEngine()
    user_result = search.by_zipcode(user_zipcode)
    user_lat = user_result.lat
    user_lng = user_result.lng
    
    # Get the latitude and longitude of the coach's zipcode
    coach_result = search.by_zipcode(coach_zipcode)
    coach_lat = coach_result.lat
    coach_lng = coach_result.lng
    
    # Radius of the Earth in miles
    R = 3958.8  # Radius of Earth in miles

    # Convert latitudes and longitudes from degrees to radians
    lat1 = radians(user_lat)
    lon1 = radians(user_lng)
    lat2 = radians(coach_lat)
    lon2 = radians(coach_lng)

    # Haversine formula to calculate distance
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Define the upload folder for storing profile pictures
app.config['UPLOAD_FOLDER'] = 'uploads'

if __name__ == '__main__':
    app.run(debug=True)
