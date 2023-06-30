import os
import secrets
from PIL import Image
from flask import url_for, current_app
from top_tech import mail


def save_photos(form_picture):
    hex_no = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    photo_filename = hex_no + f_ext
    photo_path = os.path.join(current_app.root_path, 'static/profile_pics', photo_filename)

    size = (130, 130)
    i = Image.open(form_picture)
    i.thumbnail(size)
    i.save(photo_path)

    return photo_filename
