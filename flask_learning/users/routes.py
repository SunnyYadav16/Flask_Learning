from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_learning import bcrypt, db
from flask_learning.models import User, Post
from flask_learning.users.forms import RegistrationForm, LoginForm, ResetForm, ResetPasswordForm, UpdateAccountForm
from flask_learning.users.utils import send_mail, save_picture

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def user_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # flash(f"Account Created {form.username.data} successfully!", 'success')
        flash(f"Account Created Successfully!", 'success')
        return redirect(url_for('users.user_login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        # if form.email.data == "admin@blog.com" and form.password.data == 'admin@12345':
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            # flash(f"Account Created {form.username.data} successfully!", 'success')
            flash(f"Logged in Successfully!", 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home_page'))
        else:
            flash(f"Logged in unsuccessful! Please check Email or Password", 'danger')
    return render_template('login.html', title='Login', form=form, legend="Login")


@users.route("/logout", methods=["POST", "GET"])
def user_logout():
    logout_user()
    return redirect(url_for('main.home_page'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Account Updated Successfully", 'success')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('user_post.html', posts=posts, user=user)


@users.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    form = ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
            flash("Request sent to the email address", "success")
            return redirect(url_for('users.user_login'))
    return render_template('reset_request.html', title='Reset Request', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_token(token)
    if user is None:
        flash("The token is invalid or expired. Please try again.", 'warning')
        return redirect(url_for('users.reset_request'))
    else:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash("Password changed successfully! Login with your new credentials.", 'success')
            return redirect(url_for('users.user_login'))
    return render_template('change_password.html', form=form, legend="Change Password", title="Change Password")
