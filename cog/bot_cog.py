import asyncio
import json
import os
import random
import re
import datetime
import subprocess
import shutil
import glob

import discord
import MeCab
import requests
from discord.ext import commands  # Bot Commands Frameworkのインポート
from googletrans import Translator
from pykakasi import kakasi

from src import colla,language_judge,roma_judge,wiki_search
from src import yurei_tweet as yt
from src import picture_download as pd

kakasi = kakasi()
num=1
# コグとして用いるクラスを定義。
class Main(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        with open("json/bot_id.json","r")as f:
            self.user_data = json.load(f)
            self.tweet_wait = False
            self.stone = False
            self.tagger = MeCab.Tagger("-d /usr/lib/arm-linux-gnueabihf/mecab/dic/mecab-ipadic-neologd -Owakati")

    def captain(self,text):
       text = text.split("\n")
       text="".join(text)
       text = self.tagger.parse(text)
       text=text.split(" ")
       with open("json/ng_word.json", "r") as f:
          ng_list = json.load(f)

       for i in text:
          for j in ng_list["ng"]:
             if i == j:
                return 1

       for i in text:
          for j in ng_list["dirty"]:
             if i == j:
                return 2

    @commands.command("goodbye")
    async def disconnect(self, ctx):
       """botを切ります"""
       await ctx.send("また会いましょう")
       await self.bot.logout()

    @commands.command()
    async def birthday(self, ctx, idol: str):
       """アイドル名を入れると誕生日を出力します"""
       with open("text/birthday.txt","r")as f:
            target=f.readline()
            while target:
                if idol in target:
                    answer=target.split(" - ")
                    break
                else:
                    target=f.readline()

            await ctx.send(answer[0])

    @commands.command()
    async def repeat(self, ctx,word:str,num:int):
        """同じ言葉を繰り返すコマンドです。引数は(単語,回数)"""
        send_word=""
        if(len(word)*num>2000):
            await ctx.send("文字数が多いですね。欲張りはダメ、絶対")
        for i in range(num):
            send_word+=word
        await ctx.message.delete()
        ch_webhooks = await ctx.channel.webhooks()
        webhook = discord.utils.get(ch_webhooks, name="久川颯")
        await webhook.send(content=send_word,
                username=ctx.author.display_name,
                avatar_url=ctx.author.avatar_url_as(format="png"))

    @commands.command("検索")
    async def search(self, ctx, *, arg):
       with open("json/bot_id.json","r")as f:
           money = json.load(f)
       if money[str(ctx.author.id)]["gold"]>200:
          money[str(ctx.author.id)]["gold"] -= 200
          with open("json/bot_id.json","w")as f:
             json.dump(money,f,indent=3)
       else:
          await ctx.send("みつはが足りません")
          return
       if os.path.isdir("picture/download"):
          shutil.rmtree('picture/download')

       subprocess.run(['python', 'google-images-download/google_images_download/google_images_download.py', "-k", arg, "-l", "1", "-o", "picture/download"])
       directory = os.listdir(f"picture/download/{arg}")
       for file in directory:
         base, ext = os.path.splitext(file)
         if ext == '.jpeg' or ext == '.jpg' or ext == '.png' or ext == '.gif':
            await ctx.send(file=discord.File(f"picture/download/{arg}/{file}"))


    @commands.command("くたばれぶるめて")
    async def senddm(self,ctx):
        user=await self.bot.fetch_user(406030636113985536)
        dm_channel = await user.create_dm()
        text=""
        for i in range(100):
            text+="ちんちん"
        await dm_channel.send(text)

    @commands.command()
    async def logs(self, ctx):
       async for entry in ctx.guild.audit_logs(limit=100):
          print('{0.user} が {0.action} to {0.target}'.format(entry))

    @commands.command("se一覧")
    async def se_list(self, ctx):
       directory = os.listdir('music')
       count=0
       music_list="```"
       for text in directory:
          music_list += text+"   "
          count += 1
          if count == 3:
             music_list += "\n"
             count=0

       music_list += "```\n"
       await ctx.send(music_list)

    @commands.command("リアリティストーン")
    async def reality(self, ctx):
       """メンバー全員の名前をアカウント名と同じにします"""
       if ctx.author.display_name!="サノス" and self.stone!=False:
           await ctx.send("お前にその力を使う資格はない")
           return
       self.stone=True
       for member in ctx.guild.members:
           try:
               await member.edit(nick=member.name)
           except discord.Forbidden:
              pass
       self.stone=False

    @commands.command("パワーストーン")
    async def power(self, ctx,name:str):
       """メンバー全員を任意の名前に一斉変更します。引数は(任意の名前)"""
       if ctx.author.display_name!="サノス" and self.stone!=False:
           await ctx.send("お前にその力を使う資格はない")
           return
       self.stone=True
       for member in ctx.guild.members:
           try:
               await member.edit(nick=name)
           except discord.Forbidden:
               pass
       self.stone=False

    @commands.command("エクスチェンジ")
    async def exchange(self,ctx):
       """botのアイコンで遊べます。未完成です"""
       global num
       ch_webhooks = await ctx.channel.webhooks()
       webhook = discord.utils.get(ch_webhooks, name="久川颯")
       if num==1:
           await webhook.send(content="ど゛う゛し゛て゛な゛ん゛だ゛よ゛お゛お゛ぉ゛お゛！゛！゛！゛ん゛あ゛あ゛あ゛あ゛あ゛ぁ゛ぁ゛あ゛あ゛！゛！゛！゛！゛",
                 username="藤原竜也",
                 avatar_url="https://stat.ameba.jp/user_images/20150306/19/tamagochan-deddosusi/3f/05/j/t02200220_0354035413237066758.jpg?caw=800")
           num=2
       elif num==2:
           await webhook.send(content="凪です",
                 username="久川凪",
                 avatar_url="https://imas.gamedbs.jp/cg/image_sp/card/quest/d30a16b66031de8bce07de107afbd190.png")
           num=3
       elif num==3:
           await webhook.send(content="I am...inevitable",
                 username="サノス",
                 avatar_url="https://contents.newspicks.com/images/news/4210549?updatedAt=20190909142641")
           num=1

    @commands.command()
    async def tf(self, ctx, text: str):
       """藤原竜也変換器です。コマンドの後に変換したい言葉を入れてください"""
       kakasi.setMode('J', 'H')  # J(Kanji) to H(Hiragana)
       conv = kakasi.getConverter()
       text=conv.do(text)
       fujiwara="゛".join(text)+"゛"
       ch_webhooks = await ctx.channel.webhooks()
       webhook = discord.utils.get(ch_webhooks, name="久川颯")
       await webhook.send(content=fujiwara,
             username="藤原竜也",
             avatar_url="https://stat.ameba.jp/user_images/20150306/19/tamagochan-deddosusi/3f/05/j/t02200220_0354035413237066758.jpg?caw=800")


    @commands.command("英語縛り")
    async def funny(self, ctx,id:str):
       """英語で縛ります"""
       with open("json/bot_id.json","r")as f:
           dic=json.load(f)
       if dic[id]["english_switch"]==False:
           await ctx.send(f"いまから<@{id}>は英語しか使えません")
           dic[id]["english_switch"]=True
       else:
           await ctx.send(f"<@{id}>は日本語が使えます")
           dic[id]["english_switch"]=False
       with open("json/bot_id.json","w")as f:
           json.dump(dic,f,indent=3)
       self.user_data=dic

    @commands.command()
    async def wiki(self, ctx, word: str):
        """wikipediaを調べます。引数(単語)"""
        await ctx.send(wiki_search.wikipediaSearch(word))

    @commands.command()
    async def gold(self, ctx):
        """所持みつはを調べます"""
        with open("json/bot_id.json","r")as f:
            gold= json.load(f)
        await ctx.send(str(gold[str(ctx.author.id)]["gold"])+"みつは")



    @commands.command("占い")
    async def fortune(self, ctx):
       """占いをします。1日一回です"""
       with open("json/bot_id.json","r")as f:
           fortune_judge= json.load(f)
       if fortune_judge[str(ctx.author.id)]["fortune"]==True:
           await ctx.send("占いは1日1回までです。欲張ってはいけません")
           return

       dice = random.randint(1, 101) #出る目を指定
       if dice==1:
           fortune_print=["超大吉","daidaikiti"]


       elif dice>1 and dice<11:
           fortune_print=["大吉","daikiti"]
       elif dice>10 and dice<25:
           fortune_print=["中吉","tyukiti"]
       elif dice>24 and dice<50:
           fortune_print=["小吉","syokiti"]
       elif dice>49 and dice<75:
           fortune_print=["吉","kiti"]
       elif dice>74 and dice<93 :
           fortune_print=["凶","kyo"]
       elif dice>92 and dice<100:
           fortune_print=["大凶","daikyo"]
       else:
           fortune_print=["まゆ吉","daidaidaidaikiti"]
       fortune_list=[]
       directory = os.listdir('picture/fortune')
       directory=sorted(directory)
       for i in directory:
           if i.startswith(fortune_print[1]):
               fortune_list.append(i)
       text=random.choice(fortune_list)

       await ctx.send(fortune_print[0])
       await ctx.send(file=discord.File(f"picture/fortune/{text}"))
       fortune_judge[str(ctx.author.id)]["fortune"]=True
       with open("json/bot_id.json","w")as f:
           json.dump(fortune_judge, f, indent=3)
       self.user_data=fortune_judge

    @commands.command()
    async def slot(self, ctx):
        """スロットで遊びます"""
        with open("json/bot_id.json","r")as f:
            gold= json.load(f)
        emoji=""
        judge=[]
        ei=[688263713228455942,688264142360281145,688263965926883356]
        if gold[str(ctx.author.id)]["gold"]<100:
            await ctx.send("みつはが足りません")
            return
        else:
            gold[str(ctx.author.id)]["gold"]-=100
            await ctx.send("100みつはを使いました")

        for i in range(3):
            emoji += str(self.bot.get_emoji(692396383000592384))
        msg=await ctx.send(emoji)
        await asyncio.sleep(2)
        await msg.delete()
        emoji=""

        for i in range(3):
            ran=random.choice(ei)
            judge.append(ran)
            emoji += str(self.bot.get_emoji(ran))
        await ctx.send(emoji)
        if judge[0]==judge[1] and judge[1]==judge[2]:
            await ctx.send("あたり！300みつはゲット！")
            gold[str(ctx.author.id)]["gold"]+=300
        with open("json/bot_id.json","w")as f:
            json.dump(gold, f, indent=3)
        self.user_data=gold

    @commands.command("送金")
    async def send_money(self, ctx, user_id: int, money: int):
        """みつはを誰かに送金できます.引数(ユーザーid,金額)"""
        with open("json/bot_id.json","r") as f:
            gold = json.load(f)

        if money < 0:
            await ctx.send('マイナスなんて存在しません。ぴえん')
            return

        if gold[str(ctx.author.id)]["gold"] < money:
            await ctx.send("お金が足りません。しくしく")
            return

        gold[str(ctx.author.id)]["gold"] -= money
        gold[str(user_id)]["gold"] += money

        with open("json/bot_id.json","w") as f:
            json.dump(gold, f, indent=3)

        me = self.bot.get_user(user_id)
        await ctx.send(me.mention+f"に{money}みつは送金しました")
        self.user_data = gold

    @commands.command("えっちしよ")
    async def edgc(self, ctx):
       if ctx.author.id == 406030636113985536:
          await ctx.author.kick()
          await ctx.send("悪は滅びた")
       else:
          await ctx.send("P、これはつーほー案件でしょうか")

    @commands.command("龍が如く字幕bot")
    async def dragon(self, ctx):
       text = yt.tweet_search()
       await ctx.send(text)



    @commands.Cog.listener()
    async def on_member_join(self,member):
         channel = discord.utils.get (member.guild.text_channels, name="玄関")
         server=member.guild
         e=discord.Embed (description="ようこそ！")
         e.add_field (name="参加ありがとうございます。", value=f"{member.mention}", inline=False)
         await channel.send(embed=e)
         with open("json/bot_id.json","r")as f:
            dic = json.load(f)
         if str(member.id) in dic:
            dic[str(member.id)]["gold"] -=10000
            dm_channel = await member.create_dm()
            with open("text/pink.txt","r")as f:
                text=f.read()
            await dm_channel.send(text)
         else:
            dic[str(member.id)]={"fortune":False,"gold":10000,"english_switch":False,"birthday":None,"playlist":[],"dirty_count":0,"leave_count":0}
         with open("json/bot_id.json","w")as f:
            json.dump(dic, f, indent=3)

    @commands.command()#メンバー登録
    async def member(self, ctx):
       with open("json/bot_id.json","r")as f:
           dic=json.load(f)
       for member in ctx.guild.members:
           if member.bot or str(member.id) in dic:
               pass
           else:
               dic[str(member.id)]={"fortune":False,"gold":10000,"english_switch":False,"fortune":False,"birthday":None,"playlist":[]}

       with open("json/bot_id.json","w")as f:
           json.dump(dic, f, indent=3)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if self.stone == True:
           return
        channel = self.bot.get_channel(557934921960783902)
        if before.display_name!= after.display_name:
            msg = before.display_name+"が"+after.display_name+"に名前を変えたようですよ、ご主人様"
            await channel.send(msg)

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel = self.bot.get_channel(557934921960783902)
        await channel.send(f"{member.display_name}が退出しました")
        with open("json/bot_id.json","r")as f:
           dic = json.load(f)
        if "leave_count" in dic:
           dic[str(member.id)]["leave_count"] +=1
        else:
           dic[str(member.id)]["leave_count"] = 0


        with open("json/bot_id.json","w")as f:
           json.dump(dic, f, indent=3)






    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        if reaction.count==1:
           if reaction.emoji =="🇺🇸":
                translator = Translator()
                trans_en = translator.translate(reaction.message.content, src='ja', dest='en')
                await reaction.message.channel.send(trans_en.text)
           elif reaction.emoji =="🇯🇵":
               translator = Translator()
               lang=translator.detect(reaction.message.content)
               trans_en = translator.translate(reaction.message.content, src=lang.lang, dest='ja')
               await reaction.message.channel.send(trans_en.text)

           elif reaction.emoji =="🇮🇹":
               translator = Translator()
               trans_en = translator.translate(reaction.message.content, src='ja', dest='it')
               await reaction.message.channel.send(trans_en.text)

    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author.bot:
         return

      print(message.content + "by" + message.author.display_name)
      num = self.captain(message.content)
      if num == 1:
         await message.delete()
      elif num == 2:
         await message.channel.send(f"{message.author.mention}言葉が汚いぞ！byキャプテンアメリカ")
         with open("json/bot_id.json", "r") as f:
            dic = json.load(f)
         dic[str(message.author.id)]["dirty_count"]+=1
         with open("json/bot_id.json", "w") as f:
            json.dump(dic,f,indent=3)

      if (language_judge.isalnum(message.content)!=True or roma_judge.judge(message.content)!=True) and self.user_data[str(message.author.id)]["english_switch"]==True:
         await message.delete()

      if message.attachments:
          if message.content=="ミリシタコラ":
              pd.download_img(message.attachments[0].url, "picture/colla/image.png")
              colla.mirikora2()
              await message.delete()
              await message.channel.send(file=discord.File("picture/colla/new.png"))
          elif message.content=="バジリスク":

              pd.download_img(message.attachments[0].url, "picture/colla/image.png")
              colla.bazirisuku()
              await message.delete()
              await message.channel.send(file=discord.File("picture/colla/new.png"))
          elif message.content=="デレステコラ":

              pd.download_img(message.attachments[0].url, "picture/colla/image.png")
              colla.deresute_kora()
              await message.delete()
              await message.channel.send(file=discord.File("picture/colla/new.png"))
          elif message.content=="優しい世界観":

              pd.download_img(message.attachments[0].url, "picture/colla/image.png")
              colla.ppp()
              await message.delete()
              await message.channel.send(file=discord.File("picture/colla/new.png"))
          elif message.content=="全員アウト":

              pd.download_img(message.attachments[0].url, "picture/colla/image.png")
              colla.out()
              await message.delete()
              await message.channel.send(file=discord.File("picture/colla/new.png"))
          elif message.content=="切り抜き":
              #if ctx.author.id!=425142865073799180:
              pd.download_img(message.attachments[0].url, "picture/colla/image.png")
              response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': open('picture/colla/image.png', 'rb')},
                data={'size': 'auto'},
                headers={'X-Api-Key': ''},
              )
              with open("json/count.json","r")as f:
                 dic = json.load(f)
              if response.status_code == requests.codes.ok:
                 with open('picture/colla/no-bg.png', 'wb') as out:
                    out.write(response.content)

                    dic["bg_count"]-=1
                    num=dic["bg_count"]
              else:
                 print("Error:", response.status_code, response.text)
              await message.delete()
              await message.channel.send(file=discord.File("picture/colla/no-bg.png"))
              with open("json/count.json","w")as f:
                 json.dump(dic, f, indent=3)
              await message.channel.send(f"あと{num}回使えます")

          elif message.content == "幽霊屋敷のつぶやき":
             if self.tweet_wait == False:

                print(self.tweet_wait)
                pd.download_img(message.attachments[0].url, "picture/yurei.png")
                yt.tweet_yurei(message.author.display_name)
                self.tweet_wait = True
                await asyncio.sleep(30)
                print("終了")
                self.tweet_wait = False
                print(self.tweet_wait)
          elif message.content == "スクショ":
             if self.tweet_wait == False:

                print(self.tweet_wait)
                pd.download_img(message.attachments[0].url, "picture/yurei.png")
                yt.tweet_screen(message.author.display_name)
                self.tweet_wait = True
                await asyncio.sleep(30)
                print("終了")
                self.tweet_wait = False
                print(self.tweet_wait)
             else:
                await message.channel.send("少し待ってください。凪からのお願いです")
                return



      if "肇ちゃん" in message.content:
         path = "picture/hajime/*.jpg"
         num=glob.glob(path)
         await message.channel.send(file=discord.File(random.choice(num)))

      if "ちえり" in message.content:
         path = "picture/chery/*.jpg"
         num = glob.glob(path)
         await message.channel.send(file=discord.File(random.choice(num)))

      if "なお" in message.content:
         path = "picture/nao/*.jpg"
         num = glob.glob(path)
         await message.channel.send(file=discord.File(random.choice(num)))

      if "!random" in message.content:
          text=message.content.split("!random")
          num=random.randint(0,100)
          await message.channel.send(text[0]+str(num)+text[1])

      if message.content.startswith("https://discordapp.com/channels/557933106544508980"):
          text=message.content.split("557933106544508980/")[1]
          text=text.split("/")
          channel = self.bot.get_channel(int(text[0]))
          messages=await channel.fetch_message(int(text[1]))


          if messages.attachments:
                embed = discord.Embed(title="引用元",description=messages.content)
                embed.set_image(url=messages.attachments[0].url)

                embed.set_author(name=messages.author.display_name,icon_url=messages.author.avatar_url)
          else:
                embed = discord.Embed(title="引用元",description=messages.content)

                embed.set_author(name=messages.author.display_name,icon_url=messages.author.avatar_url)

          await message.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Main(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
