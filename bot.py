import tweepy
import requests
import os
from time import sleep
from scraper import anime_list, get_airing_date, save_file


# Your tokens here
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def main():
    post_list, img_url_list, post_url_list = anime_list()
    for (title, url, post_url) in zip(post_list, img_url_list, post_url_list):
        air_date = get_airing_date(post_url)
        message = f"'{title}' : {air_date}  #Anime #Manga\n{post_url}"
        tweet_image(url, message)
        save_file(title)
        print(f"'{title}'\nHas Been Posted\nWaiting For Next Post ...")
        sleep(3600)


def tweet_image(url, message):
    filename = 'temp/temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=message)
        os.remove(filename)
    else:
        print("Unable to download image")


if __name__ == '__main__':
    main()