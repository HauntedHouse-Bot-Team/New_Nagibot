from PIL import Image,ImageDraw,ImageFont
def shazam(text):
    im = Image.new("RGB",(10000,2400),"white")# Imageインスタンスを作る
    draw = ImageDraw.Draw(im)# im上のImageDrawインスタンスを作る
    arial_font=ImageFont.truetype("AoyagiKouzanTOTF.otf",1600,index=0)
    draw.text((0,60),text,fill="black",font=arial_font)
    im.save("sentence.jpg")
