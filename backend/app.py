from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, validators
from flask_migrate import Migrate
from flask import send_from_directory


app = Flask(__name__, static_folder='../frontend/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1130@localhost/gymster_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Define your database models
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

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

#Define a signup form with validation
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

@app.route('/signup_success/<first_name>')
def signup_success(first_name):
    return render_template('signup_success.html', first_name=first_name)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
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

        # Store the user data in the database
        new_user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number,
                        password=password, street_address_1=street_address_1, street_address_2=street_address_2,
                        city=city, state=state, zipcode=zipcode, country=country)
        db.session.add(new_user)
        db.session.commit()

        flash('You have successfully signed up!', 'success')

        return redirect(url_for('signup_success', first_name=first_name))

    return render_template('signup.html', form=form)




@app.route('/users')
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
