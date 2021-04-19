# AI Caption Generator

This is a web app that allows you to upload an image file, generate a caption for it using deep learning, then automatically post the image an caption to our Twitter bot [@Bot2021U](https://twitter.com/Bot2021U).
- Flask backend
- Keras for deep learning, starter code from [this tutorial](https://machinelearningmastery.com/develop-a-deep-learning-caption-generation-model-in-python/)
- current model based on [Flickr8K dataset](https://academictorrents.com/details/9dea07ba660a722ae1008c4c8afdd303b6f6e53b)
- tested another model based on [InstaCities1M dataset](https://gombru.github.io/2018/08/01/InstaCities1M/)

Developed for [University of Iowa Hackathon 2021](hack.uiowa.edu) by Raymond Yang, Mitchell Hermon, Ethan D'Allesandro, and Riley Bridges. Devpost link [here](https://devpost.com/software/imagecaptionai).

## Host the App

1. Make a `secrets.py` file to store your Twitter API keys:
```python
API_KEY = ''
API_SECRET_KEY = ''
BEARER_TOKEN = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
```
2. Set Flask app to `app.py`:
    - `export FLASK_APP=app.py` on linux

3. `flask run`

## Train the Model

1. Change `image_prep.py`, `text_prep.py`, `progressive_loading.py`, `evaluate.py`, `create_tokenizer.py` to work with the desired dataset
2. `bash train_ai.sh`