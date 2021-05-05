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
import sys
import datetime

VERSION = 20210501001

CK = CONFIG["CONSUMER_KEY"]     # Consumer Key
CS = CONFIG["CONSUMER_SECRET"]  # Consumer Secret
AT = CONFIG["ACCESS_TOKEN"]     # Access Token
AS = CONFIG["ACCESS_SECRET"]    # Accesss Token Secert


def doRetweet(tweetId):
    try:
        api.retweet(tweetId)  # Retweet
    except Exception as e:
        print('------------- Exception -----------------')
        print(e)
        print(datetime.datetime.now())
        sys.stdout.flush()


class Listener(tweepy.StreamListener):  # StreamListenerを継承するクラスListener作成
    def on_status(self, status):
        if status.text.find('RT @') != 0:  # RTされた投稿は対象外 : RTは先頭に RT @NAME が追加される
            status.created_at += timedelta(hours=9)  # 世界標準時から日本時間に
            print('-------------- INFO ----------------')
            print("{name}({screen}) {created} via {src} retweeted={retweeted}\n".format(
                name=status.author.name, screen=status.author.screen_name,
                created=status.created_at, src=status.source, retweeted=status.retweeted))
            sys.stdout.flush()
            doRetweet(status.id)
        return True

    def on_error(self, status_code):
        print('エラー発生: ' + str(status_code))
        print(datetime.datetime.now())
        sys.stdout.flush()
        return True

    def on_timeout(self):
        print('Timeout...')
        print(datetime.datetime.now())
        sys.stdout.flush()
        return True


print("ver = {ver} start!!".format(ver=VERSION))
print(datetime.datetime.now())

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
        print(datetime.datetime.now())
        sys.stdout.flush()
        stream.filter(track=["#ストVラウンジ募集"])  # 指定の検索ワードでフィルタ
    except ProtocolError:
        print('-------------- ProtocolError -> continue ----------------')
        print(datetime.datetime.now())
        sys.stdout.flush()
        continue
