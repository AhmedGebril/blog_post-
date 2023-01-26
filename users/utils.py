import smtplib
import os
import secrets
from flask import url_for
from run import app


def save_photo(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_file = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_file)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user="ahmedgebril1889@gmail.com", password="gatcrnogtbtxbkdh")
        connection.sendmail(from_addr="ahmedgebril1889@gmail.com",
                            to_addrs=user.email,
                            msg=f"Please follow this link to reset your password {url_for('reset_token', token=token)} if "
                                f"you didnt send it just ignore the email.")