from flask import Blueprint,render_template,redirect,url_for,flash,request
from run import db,User,current_user
from flask_login import LoginManager,login_user,logout_user,login_required
from users.form import Regestration,Request_Reset,Reset_password,Log_in_Form,Account_form
from users.utils import save_photo,send_reset_email

users = Blueprint('users', __name__)


@users.route('/Register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        form = Regestration()
        if form.validate_on_submit():
            user = User(username=form.username.data, password=form.password.data, email=form.email.data,followers=0)
            db.session.add(user)
            db.session.commit()
            print(user)
            flash('you have successfully created an account!', 'success')
            return redirect(url_for('Log_in'))
        return render_template('Registration.html', form=form)


@users.route('/login', methods=['POST', 'GET'])
def Log_in():
    log_in_form = Log_in_Form()
    if log_in_form.validate_on_submit():
        user = User.query.filter_by(email=log_in_form.email.data).first()
        if user and log_in_form.password.data == user.password:
            flash('Logged in successfully', 'success')
            login_user(user, remember=log_in_form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Logging in unsuccessfully Please Check Email or Password!', 'danger')
    return render_template('log_in.html', form=log_in_form)

@users.route('/account', methods=['POST', 'GET'])
@login_required
def Account():
    form = Account_form()
    if form.validate_on_submit():
        if form.picture_file.data:
            user_picture = save_photo(form.picture_file.data)
            current_user.image_file = user_picture
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        flash('you account has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
        image_filee = url_for('static', filename='profile_pics/' + current_user.image_file)
        print(current_user.image_file)
    return render_template('account.html', form=form, image_file=image_filee)


@users.route('/Logout')
def Log_out():
    logout_user()
    flash('logged out successfully', 'danger')
    return redirect(url_for('home'))


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Request_Reset()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = Reset_password()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
