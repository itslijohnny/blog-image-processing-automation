from PIL import Image, ImageDraw, ImageFont
import tinify
import requests
import sys
import os
import os.path
import re
import pyperclip
import json
print('Drag and drop the image here.')

size = 1600, 728
x_text = 38
y_text = 682
font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 24)

cwd = os.path.dirname(os.path.realpath(__file__))

def img_process(img,size,x_text,y_text,font):
    name=str(os.path.basename(img)).rstrip()
    img = img.rstrip()
    original = Image.open(img)
    cropped = img_crop(original,size)
    cropped.thumbnail(size, Image.ANTIALIAS)
    img_addtext(cropped,name,x_text,y_text,font)
    cropped.save('{}/resizeimage.jpg'.format(cwd), "JPEG")
    keyFile = open('{}/api.txt'.format(cwd), 'r')
    consumer_key = keyFile.readline().rstrip()
    tinify.key = consumer_key
    source = tinify.from_file("{}/resizeimage.jpg".format(cwd))
    source.to_file("{}/optimized.jpg".format(cwd))
    print('Compressed by tinypng')
    img2 = '{}/optimized.jpg'.format(cwd)
    url = "https://sm.ms/api/upload"
    files = {'smfile': ("%s"%name , open(img2.replace("\n", ""), 'rb'), 'image/png')}
    sdata = {'ssl': 1}
    res = requests.post(url=url, data=sdata, files=files)
    the_json = res.text
    the_json = json.loads(the_json)
    print('Uploaded to sm.ms')
    print(the_json["data"]["url"])  # 图片链接
    mk = '![%s](%s )' % (the_json["data"]["filename"], the_json["data"]["url"])
    pyperclip.copy(mk)
    print("copyed in clipboard")


def img_crop(original,size):
    width, height = original.size
    left = 0
    right = width
    h = int((width/size[0])*size[1])
    top = (height - h)/2
    bottom = h+(height - h)/2
    cropped = original.crop((left, top, right, bottom))
    return cropped

def img_addtext(cropped,name,x_text,y_text,font):
    (x, y) = (x_text, y_text)
    if name.find('unsplash') > 0:
        ste = (re.findall(r'.+(?=[a-z])', re.findall(r'.+(?<=[0-9])', name)[0])[0]).replace('-',' ').title()
        message = "Photo by {} on Unsplash".format(ste)
        color = 'rgb(255, 255, 255)' # black color
        d = ImageDraw.Draw(cropped)
        d.text((x, y), message, fill=color, font=font)

while(True):
    img = sys.stdin.readline()
    img_process(img,size,x_text,y_text,font)
