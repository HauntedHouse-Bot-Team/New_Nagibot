import tweepy
import os
from os.path import join, dirname
from dotenv import load_dotenv
import random
import json
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
#トークンを入れる
CK= os.environ.get("CK") 
CS= os.environ.get("CS") 
AT= os.environ.get("AT") 
AS= os.environ.get("AS") 

auth= tweepy.OAuthHandler(CK,CS)
auth.set_access_token(AT,AS)
api= tweepy.API(auth)

#ツイートしたい文章
def tweet_yurei(user):
   status= f"#幽霊屋敷の呟き\nby{user}"

   #ツイートに付加したい画像をimagesリストに入れる
   #media_idsは投稿した画像のidを入れるためのリスト
   images= ["picture/yurei.png"]
   media_ids=[]

   #画像は4枚までしか投稿できないので4回ループする
   for i in images:
      img= api.media_upload(i)
      media_ids.append(img.media_id)


   api.update_status(status=status, media_ids=media_ids)

def tweet_screen(user):
   with open("json/count.json", "r") as f:
      num = json.load(f)
   text=str(nuｍ["screen"])
   status = f"#7084枚担当スクショプロジェクト\n{text}枚目\nby{user}"
   

   #ツイートに付加したい画像をimagesリストに入れる
   #media_idsは投稿した画像のidを入れるためのリスト
   images= ["picture/yurei.png"]
   media_ids=[]

   #画像は4枚までしか投稿できないので4回ループする
   for i in images:
      img= api.media_upload(i)
      media_ids.append(img.media_id)


   api.update_status(status=status, media_ids=media_ids)
   num["screen"]+=1
   with open("json/count.json", "w") as f:
      json.dump(num,f,indent=3)

def tweet_search():

   results = api.user_timeline(screen_name="Yakuzasubtitles", count=50)
   return random.choice(results).text

if __name__ == "__main__":
   tweet_search()