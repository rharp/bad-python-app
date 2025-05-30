import os
from flask import render_template
from pathlib import Path
from util import get_uploads_folder_url


ALLOWED_EXTENSIONS = ['.png', '.jpeg', '.jpg']


def file_upload_page():
    return render_template('file_upload.html', file_url=None)


def file_upload_api(request, app):
    file = request.files['file']

    temp_path = os.path.join(app.config['TEMP_UPLOAD_FOLDER'], file.filename)
    file.save(temp_path)

    resized_path = temp_path + ".min.png"
    os.system(f'convert {temp_path} -resize 50% {resized_path}')

    public_path = os.path.join(app.config['PUBLIC_UPLOAD_FOLDER'], file.filename)
    os.system(f'mv {resized_path} {public_path}')

    return render_template('file_upload.html',
                           file_url=f'{get_uploads_folder_url()}/{file.filename}')

def _validate_file(filename):
    extension = os.path.splitext(filename)[1]
    return extension in ALLOWED_EXTENSIONS


def _save_temp_file(file, app):
    original_file_name = file.filename
    temp_upload_file_path = os.path.join(app.config['TEMP_UPLOAD_FOLDER'],
                                         original_file_name)
    file.save(temp_upload_file_path)

    resized_image_path = f'{temp_upload_file_path}.min.png'
    command = f'convert "{temp_upload_file_path}" -resize 50% "{resized_image_path}"'
    os.system(command)

    return {'saved_path': resized_image_path}
