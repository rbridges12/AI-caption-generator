import mimetypes
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from urllib.request import urlopen
import tweepy
from captionAI.caption_gen import caption_generator
import secrets

UPLOADS_FOLDER = 'static/uploads/'
TOKENIZER_PATH = 'captionAI/models/tokenizer.pkl'
MODEL_PATH = 'captionAI/models/model_19.h5'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


generator = caption_generator(TOKENIZER_PATH, MODEL_PATH)
app = Flask(__name__)

app.config['SECRET_KEY'] = 'something'
app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER

image_path = ""


@app.route('/')
def image_caption():
    return render_template('ImageMLWebsite.html')


@app.route('/file_upload', methods=['POST'])
def file_upload():

    # if a URL was provided, download and save it
    if request.form['fileType'] == 'URL':

        url = request.form['image']
        if not check_url(url):
            flash("Could not read URL")
            return redirect('/')

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


def check_url(url):
    try:
        res = urlopen(url)
        message = res.info()
        return message not in ('image/png', 'image/jpeg', 'image/jpg')
    except:
        return False


@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    global image_path
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    caption = generator.get_caption(image_path)
    caption = caption + " #HackUIowa"
    caption = caption.replace(' in red shirt', '')
    caption = caption.replace('man', 'person')
    captionUpper = caption[0].upper() + caption[1:]
    return render_template('tweetImage.html', image='/'+image_path, caption=captionUpper)



@app.route('/tweet_confirmation', methods=['POST'])
def tweet_confirmation():
    caption = request.form.get('caption')
    url = tweet(image_path, caption)
    return render_template('tweetConfirmation.html', url=url)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def tweet(image, caption):
    auth = tweepy.OAuthHandler(secrets.API_KEY, secrets.API_SECRET_KEY)
    auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)

    if image and image[1] == '/':
        image = image[1:]

    api = tweepy.API(auth)

    # '''
    # try:
    #     api.verify_credentials()
    #     print("Authentication OK")
    # except:
    #     print("Error during authentication")
    # '''

    media = api.media_upload(image)  # Image file

    post_result = api.update_status(status=caption, media_ids=[media.media_id])

    try:
        os.remove(image_path)
    except:
        pass

    newUrl = "https://twitter.com/Bot2021U/status/" + str(post_result.id)
    return newUrl