import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/default_image", picture_fn) 

    output_size = (125, 125) #because css only diaplay iimage correclt in 125x125 resolution
    image_sizing = Image.open(form_picture)
    image_sizing.thumbnail(output_size)
    image_sizing.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password reset request", sender="demoappflask@gmail.com", recipients=[user.email])
    msg.body = f""" To reset your password visit the following
link {url_for("users.reset_token", token=token, _external=True)}  
if you did not make he request then simply ignore it"""   #_external used to get url in absolute path
  
    mail.send(msg)