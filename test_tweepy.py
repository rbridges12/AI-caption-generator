import tweepy
import secrets

auth = tweepy.OAuthHandler(secrets.API_KEY, secrets.API_SECRET_KEY)
auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

api.update_status('hello')

'''
media = api.media_upload(image)  # Image file

post_result = api.update_status(status=caption, media_ids=[media.media_id])

if os.path.exists(image_path):
    os.remove(image_path)
newUrl = "https://twitter.com/Bot2021U/status/" + str(post_result.id)
return newUrl
'''i