from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord
import random
import re
import linecache
import csv
from discord.utils import get
import json

# コグとして用いるクラスを定義。
class Game(commands.Cog):


   def __init__(self, bot):
        self.bot = bot
        self.handbattle=False
   
   @commands.command("じゃんけん")
   async def funny(self, ctx):
      if self.handbattle == True:
         return
      self.handbattle == True
      await ctx.send("じゃんけんしましょう。最初はパー")
      hand = random.randint(0, 2)
      dic={"グー":0,"チョキ":1,"パー":2}
      ch_webhooks = await ctx.channel.webhooks()
      webhook = discord.utils.get(ch_webhooks, name="久川颯")
      await webhook.send(content="せっ……出せっ！！グーチョキパーだ！早くしろ！",
             username="藤原竜也",
             avatar_url="https://stat.ameba.jp/user_images/20150306/19/tamagochan-deddosusi/3f/05/j/t02200220_0354035413237066758.jpg?caw=800")
      def check(m):
         return m.author.id==ctx.author.id and (m.content == 'グー' or m.content == 'チョキ' or m.content == 'パー') and m.channel == ctx.channel
      
      msg = await self.bot.wait_for('message', check=check)
      await ctx.send(f"{list(dic.keys())[hand]}です")
      with open("json/bot_id.json", "r") as f:
         dic2 = json.load(f)
      
      if dic[msg.content] == (hand + 2) % 3:
         await ctx.send("あなたの勝ちです。ねぎどうぞ")
         dic2[str(ctx.author.id)]["gold"] += 300
      elif dic[msg.content] == (hand + 1) % 3:
         await ctx.send("凪の勝ちです。300みつはもらいますね、わーい")
         dic2[str(ctx.author.id)]["gold"] -= 300
      else:
         await ctx.send("引き分けですね")

      with open("json/bot_id.json", "w") as f:
         json.dump(dic2,f,indent=3)
      self.handbattle == False
      


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Game(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
