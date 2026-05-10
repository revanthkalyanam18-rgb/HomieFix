from flask import Flask, render_template, request, redirect

from flask_login import (
    LoginManager,
    login_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from extensions import db, login_manager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'homiefix_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager.init_app(app)

login_manager.login_view = 'login'

from models.models import User, Service, Booking


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        role = request.form['role']
        address = request.form['address']

        if not name or not email or not password:

            return '''
            <h2>All fields are required!</h2>
            <a href="/register">Go Back</a>
            '''

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            return '''
            <h2>Email already registered!</h2>
            <a href="/login">Login Here</a>
            '''

        hashed_password = generate_password_hash(password)

        user = User(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password,
            role=role,
            address=address
        )

        db.session.add(user)

        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        user = User.query.filter_by(
            email=request.form['email']
        ).first()

        if user and check_password_hash(
            user.password,
            request.form['password']
        ):

            login_user(user)

            return redirect('/dashboard')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():

    return render_template('dashboard.html')


@app.route('/services')
@login_required
def services():

    services = Service.query.all()

    return render_template(
        'services.html',
        services=services
    )


if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(debug=True)