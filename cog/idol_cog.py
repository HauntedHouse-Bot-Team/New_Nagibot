import os
import random
import asyncio
import discord
from discord.ext import commands  # Bot Commands Frameworkのインポート
from discord.ext import tasks
import json
import csv
import glob
class Idol(commands.Cog):


   def __init__(self, bot):
      self.bot = bot
   

   @commands.command("アイドル検索")
   async def idol_search(self, ctx, name: str):
      with open("Idol.csv") as f:
         text = [row for row in csv.reader(f)]
      for i in text:
         if i[1] == name:
            num = int(i[0])
      if num == None:
         return
      embed = discord.Embed(title=f"{text[num][1]}({text[num][2]})")
      embed.add_field(name="属性", value=f"{text[num][3]}",inline=False)
      embed.add_field(name="年齢", value=f"{text[num][6]}")
      embed.add_field(name="誕生日", value=f"{text[num][4]}/{text[num][5]}")
      embed.add_field(name="出身地", value=f"{text[num][10]}")
      embed.add_field(name="血液型", value=f"{text[num][8]}")
      embed.add_field(name="利き手", value=f"{text[num][9]}")
      embed.add_field(name="趣味", value=f"{text[num][11]}")
      await ctx.send(embed=embed)
   
   @commands.command("奈緒ルーレット")
   async def nao_roulette(self, ctx):
      msg=await ctx.send(file=discord.File('picture/nao/nao.gif'))
      await asyncio.sleep(5)
      await msg.delete()
      path = "picture/nao/*.jpg"
      num = glob.glob(path)
      await ctx.send(file=discord.File(random.choice(num)))

   @commands.command("肇ルーレット")
   async def hajime_roulette(self, ctx):
      msg=await ctx.send(file=discord.File('picture/hajime/hajime.gif'))
      await asyncio.sleep(5)
      await msg.delete()
      path = "picture/hajime/*.jpg"
      num = glob.glob(path)
      await ctx.send(file=discord.File(random.choice(num)))

         
      
   

       
       


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):

    bot.add_cog(Idol(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
