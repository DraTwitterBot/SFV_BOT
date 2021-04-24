# twitter-stream1.py

#
# note
# https://su-gi-rx.com/archives/942
# https://stackoverflow.com/questions/44378849/bypassing-the-incompleteread-exception
#

import tweepy
from datetime import timedelta
from config import CONFIG
from urllib3.exceptions import ProtocolError

CK = CONFIG["CONSUMER_KEY"]     # Consumer Key
CS = CONFIG["CONSUMER_SECRET"]  # Consumer Secret
AT = CONFIG["ACCESS_TOKEN"]     # Access Token
AS = CONFIG["ACCESS_SECRET"]    # Accesss Token Secert

def doRetweet(tweetId):
    try:
        api.retweet(tweetId) # Retweet
    except Exception as e:
        print('------------- Exception -----------------')
        print(e)

# StreamListenerを継承するクラスListener作成
class Listener(tweepy.StreamListener):
    def on_status(self, status):
        if status.text.find('RT @') != 0: # RTされた投稿は対象外 : RTは先頭に RT @NAME が追加される
            status.created_at += timedelta(hours=9) # 世界標準時から日本時間に
            print('-------------- status.text ----------------')
            print(status.text)
            print('-------------- INFO ----------------')
            print("{name}({screen}) {created} via {src} retweeted={retweeted}\n".format(
                name=status.author.name, screen=status.author.screen_name,
                created=status.created_at, src=status.source, retweeted=status.retweeted))

            doRetweet(status.id)

        return True

    def on_error(self, status_code):
        print('エラー発生: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True

# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

# Listenerクラスのインスタンス
listener = Listener()

# 受信開始
stream = tweepy.Stream(auth, listener)

while True:
    try:
        print('-------------- stream.filter ----------------')
        stream.filter(track = ["#ストVラウンジ募集"]) # 指定の検索ワードでフィルタ
    except ProtocolError:
        print('-------------- ProtocolError -> continue ----------------')
        continue
