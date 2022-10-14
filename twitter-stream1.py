# twitter-stream1.py

#
# note
# https://su-gi-rx.com/archives/942
# https://stackoverflow.com/questions/44378849/bypassing-the-incompleteread-exception
#

import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')

import tweepy
from datetime import timedelta
from config import CONFIG
from urllib3.exceptions import ProtocolError
import datetime
import ngWord
import blackList


VERSION = 20221015001

DEBUG = False

CK = CONFIG["CONSUMER_KEY"]     # Consumer Key
CS = CONFIG["CONSUMER_SECRET"]  # Consumer Secret
AT = CONFIG["ACCESS_TOKEN"]     # Access Token
AS = CONFIG["ACCESS_SECRET"]    # Accesss Token Secert
BT = CONFIG["BEARER_TOKEN"]    # Accesss Token Secert

BLACK_LIST = blackList.BLACK_LIST
NG_WORD_LIST = ngWord.NG_WORD


def doRetweet(tweetId):
    try:
        if DEBUG:
            print('------------- fake retweet -----------------')
            sys.stdout.flush()
        else:
            client.retweet(tweetId)  # Retweet
    except Exception as e:
        print('------------- Exception -----------------')
        print(e)
        print(datetime.datetime.now())
        sys.stdout.flush()


class StreamListener(tweepy.Stream):  # tweepy.Stream を継承するクラス StreamListener 作成
    def on_status(self, status):
        if status.text.find('RT @') != 0:  # RTされた投稿は対象外 : RTは先頭に RT @NAME が追加される
            status.created_at += timedelta(hours=9)  # 世界標準時から日本時間に
            print('-------------- INFO start ----------------')
            print("status.author.name = {author_name}, status.author.screen_name = {author_screen_name}, status.author.id = {status_author_id}, status.created_at = {status_created_at}\n".format(
                author_name=status.author.name, author_screen_name=status.author.screen_name, status_author_id=status.author.id, status_created_at=status.created_at))
            print('-------------- INFO end ----------------')

            isBlackListUser = status.author.id in BLACK_LIST
            isBlackListUserQuoted = False

            ngWordFlag = False
            findNgWord = ""

            if hasattr(status, 'quoted_status'):
                print('-------------- Quoted INFO start ----------------')
                print("status.quoted_status.author.name = {author_name}, status.quoted_status.author.screen_name = {author_screen_name}, status.quoted_status.author.id = {status_author_id}, status.quoted_status.created_at = {status_created_at}\n".format(
                    author_name=status.quoted_status.author.name, author_screen_name=status.quoted_status.author.screen_name, status_author_id=status.quoted_status.author.id, status_created_at=status.quoted_status.created_at))

                isBlackListUserQuoted = status.quoted_status.author.id in BLACK_LIST

                for ngWord in NG_WORD_LIST:
                    if ngWord in status.quoted_status.text:
                        findNgWord = ngWord
                        ngWordFlag = True
                        break

                print('-------------- Quoted INFO end ----------------')

            sys.stdout.flush()

            if isBlackListUser or isBlackListUserQuoted or ngWordFlag:
                if isBlackListUser:
                    print("-------------- author is Black --------------")
                if isBlackListUserQuoted:
                    print("-------------- quoted author is Black --------------")
                if ngWordFlag:
                    print(
                        "-------------- quoted text in NG WORD = {ng_word} --------------".format(ng_word=findNgWord))
                sys.stdout.flush()
            else:
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

while True:
    try:
        # Twitterオブジェクトの生成
        client = tweepy.Client(consumer_key=CK, consumer_secret=CS,
                               access_token=AT, access_token_secret=AS, bearer_token=BT)

        # Listenerクラスのインスタンス
        streamlistener = StreamListener(
            CK, CS,
            AT, AS
        )

        while True:
            try:
                print('-------------- stream.filter ----------------')
                print(datetime.datetime.now())
                sys.stdout.flush()
                if DEBUG:
                    streamlistener.filter(track=["#draBotTest"])  # テスト用の検索ワード
                else:
                    streamlistener.filter(
                        track=["#ストVラウンジ募集"])  # 指定の検索ワードでフィルタ
            except ProtocolError:
                # 再接続が不要な例外は、filterにハンドリング
                print('-------------- ProtocolError -> continue ----------------')
                print(datetime.datetime.now())
                sys.stdout.flush()
                continue
    except Exception:
        # 再接続が必要な例外は、再接続にハンドリング
        print("Unexpected error:", sys.exc_info()[0])
        continue
