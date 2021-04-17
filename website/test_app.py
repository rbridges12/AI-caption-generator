
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import tweepy

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['SECRET_KEY'] = 'something'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def image_caption():
    # tweet("model.png","test image")
    return render_template('ImageMLWebsite.html')


@app.route('/file_upload', methods=['POST'])
def file_upload():

    # check if an image was uploaded
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['image']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join("uploads/", filename))
        return redirect(url_for('uploaded_file', filename=filename))


# TODO: write HTML page for after the image is uploaded to show caption with a button to tweet
@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    flash(filename)
    return '''
    <!doctype html>
    <title>File is uploaded</title>
    <body> hey there </body>
    '''

def get_caption(image_filename):
    

def tweet(image, caption):
    auth = tweepy.OAuthHandler(
        "s6j20sJFJRabXx5ImyM0QEEaD", "N6MmSc19jfCqESX3wAInJUhLEW0oidUptDiMNF6XgPahgqnSYg")
    auth.set_access_token("2733437449-7tAXSHbYjQJapC9ITqxLmsDtHCcHcwDhL6AJ0Lf",
                          "ih6BSfqlTAV4eYE5MzrzBeqhYXZMkbWSYQ7FclXATKUen")

    api = tweepy.API(auth)
    media = api.media_upload(image)  # Image file

    post_result = api.update_status(status=caption, media_ids=[media.media_id])
