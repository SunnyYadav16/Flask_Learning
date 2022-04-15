import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_learning import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename


def send_mail(user):
    token = user.get_token()
    msg = Message(subject='Password Reset Request', recipients=[user.email], sender='fanatasticsingh99@gmail.com')
    msg.body = f"""
        To reset your password. Please click on the link below.

        {url_for('users.reset_token', token=token, _external=True)}

        If you didn't send the password reset request. Ignore this message.
    """
    mail.send(msg)