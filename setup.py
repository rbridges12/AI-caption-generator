from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from urllib.request import urlopen
import tweepy
from captionAI.caption_gen import caption_generator

# TODO: save model files to google drive
UPLOADS_FOLDER = 'static/uploads/'
TOKENIZER_PATH = 'captionAI/tokenizer.pkl'
MODEL_PATH = 'captionAI/model_1.h5'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

generator = caption_generator(TOKENIZER_PATH, MODEL_PATH)
app = Flask(__name__)

app.config['SECRET_KEY'] = 'something'
app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER

image_path = ""


@app.route('/')
def image_caption():
    # tweet("model.png","test image")
    return render_template('ImageMLWebsite.html')


@app.route('/file_upload', methods=['POST'])
def file_upload():

    # if a URL was provided, download and save it
    if request.form['fileType'] == 'URL':
        url = request.form['image']
        res = urlopen(url)
        filename = url.replace('.', '') + '.jpg'
        # TODO: fix this
        # filename = filename.replace('/', '')
        filename = "random_name" + str(len(url)) + '.jpg'
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
            f.write(res.read())
        return redirect(url_for('uploaded_file', filename=filename))

    # check if an image was uploaded
    if 'image' not in request.files:
        flash('No file part')
        return redirect('/')

    # if user does not select file, browser also
    # submit an empty part without filename
    file = request.files['image']
    if file.filename == '':
        flash('No selected file')
        return redirect('/')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename))

    flash('Please Select Correct File Type')
    return redirect('/')

# TODO: resize image to fit


@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    global image_path
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    caption = generator.get_caption(image_path)
    return render_template('tweetImage.html', image=image_path, caption=caption)

# TODO: get URL of tweet


@app.route('/tweet_confirmation', methods=['POST'])
def tweet_confirmation():
    caption = request.form.get('caption')
    # image = request.form.get('image')
    url = tweet(image_path, caption)
    return render_template('tweetConfirmation.html', url=url)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# TODO: hide keys in secret file
def tweet(image, caption):
    auth = tweepy.OAuthHandler(
        "s6j20sJFJRabXx5ImyM0QEEaD", "N6MmSc19jfCqESX3wAInJUhLEW0oidUptDiMNF6XgPahgqnSYg")
    auth.set_access_token("2733437449-7tAXSHbYjQJapC9ITqxLmsDtHCcHcwDhL6AJ0Lf",
                          "ih6BSfqlTAV4eYE5MzrzBeqhYXZMkbWSYQ7FclXATKUen")

    # imagePath = os.path.join(
    #     app.config['UPLOAD_FOLDER'], image)
    api = tweepy.API(auth)
    print(image, caption)
    media = api.media_upload(image)  # Image file

    post_result = api.update_status(status=caption, media_ids=[media.media_id])

    if os.path.exists(image_path):
        os.remove(image_path)
    newUrl = "http://twitter.com/mherman05/status/" + str(post_result.id)
    return newUrl
