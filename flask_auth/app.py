from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, UpdateAccountForm
from models import db, User, bcrypt
from config import Config
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = hashed_password
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('home'))
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route("/")
def home():
    return "Home Page"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

