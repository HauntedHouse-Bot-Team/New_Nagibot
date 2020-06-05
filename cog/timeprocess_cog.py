from discord.ext import commands,tasks  # Bot Commands Frameworkのインポート
import datetime
import json
import os
import discord
import subprocess
import shutil

# コグとして用いるクラスを定義。
class Time(commands.Cog):

    wait_seconds=60.0
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()
        self.birthday_sned = False
    
    def fortune_reset(self):
       with open("json/bot_id.json", "r") as f:
             dic = json.load(f)
       key=list(dic.keys())
       for i in key:
          dic[i]["fortune"] = False
       with open("json/bot_id.json", "w") as f:
          json.dump(dic, f, indent=3)
          

    

    @tasks.loop(seconds=wait_seconds)
    async def printer(self):
       nowtime = datetime.datetime.now()
       if nowtime.hour == 0 and nowtime.minute == 0 :
          self.fortune_reset()
          with open("json/birthday.json", "r") as f:
             dic = json.load(f)
          if f"{nowtime.month}/{nowtime.day}" in dic and self.birthday_sned == False:
             channel = self.bot.get_channel(557934921960783902)
             birthday = dic[f"{nowtime.month}/{nowtime.day}"]
             for i in birthday:
               if os.path.isdir("picture/download"):
                  shutil.rmtree('picture/download')
               subprocess.run(['python', 'google-images-download/google_images_download/google_images_download.py',
               "-k",i, "-l", "1", "-o", "picture/download"])
               directory = os.listdir(f"picture/download/{i}")
               for file in directory:
                  base, ext = os.path.splitext(file)
                  if ext == '.jpeg' or ext == '.jpg' or ext == '.png' or ext == '.gif':
                     await channel.send(f"{nowtime.month}/{nowtime.day}は{i}の誕生日です。ぱちぱち",
                     file=discord.File(f"picture/download/{i}/{file}"))
             self.birthday_sned = True
             wait_seconds = 60.0

       elif nowtime.hour == 23 and nowtime.minute == 59:
          self.birthday_sned=False
          wait_seconds = 60.0- float(nowtime.second)
       
      


             

          
 
    
# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Time(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
