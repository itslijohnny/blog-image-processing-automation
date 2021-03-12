from PIL import Image, ImageDraw, ImageFont
import tinify
import requests
import sys
import os
import os.path
import re
# import pyperclip
import json
import io

size = 1600, 728
x_text = 38
y_text = 682

def get_img(id):
    """Get information for image based on the image ID

    Args:
        id (str): Image ID

    Returns:
        img_url: image's URL
        user_name: artist's name
    """
    cwd = os.path.dirname(__file__)
    url = 'http://api.unsplash.com/photos/'+id
    with open('{}/ca.txt'.format(cwd)) as f:
        API_KEY = f.readline()
    params = dict(client_id=API_KEY)
    res = requests.get(url, params=params)
    img_url = res.json()['urls']['raw']
    name = res.json()['user']['name']
    return img_url, name 


def img_process(id,width,height,x_text,y_text):
    """Process image

    Args:
        id (str): Image ID
        width (int, optional): The width after processing. 
        height (int, optional): The height after processing. 
        x_text (int, optional): The x position for the artist's name on the image. 
        y_text (int, optional): The y position for the artist's name on the image . 
    Returns:
        str: Processed image url and MarkDown string.
    """
    cwd = os.path.dirname(__file__)
    url, name=get_img(id)
    original = Image.open(requests.get(url, stream=True).raw)
    size = width,height
    cropped = img_crop(original,size)
    cropped.thumbnail(size, Image.ANTIALIAS)
    truetype_url = 'https://github.com/ProgrammingFonts/ProgrammingFonts/raw/master/Droid-Sans-Mono/droid-sans-mono-1.00/Droid%20Sans%20Mono.ttf'
    r = requests.get(truetype_url, allow_redirects=True)
    font = ImageFont.truetype(io.BytesIO(r.content), size=24)

    img_addtext(cropped,name,x_text,y_text,font)
    cropped.save('{}/resizeimage.jpg'.format(cwd), "JPEG")
    keyFile = open('{}/tiny.txt'.format(cwd), 'r')
    consumer_key = keyFile.readline().rstrip()
    tinify.key = consumer_key
    source = tinify.from_file("{}/resizeimage.jpg".format(cwd))
    source.to_file("{}/{}.jpg".format(cwd,id))
    print('Compressed by tinypng')
    img2 = '{}/{}.jpg'.format(cwd,id)
    the_json = upload(img2)
    os.remove('{}/resizeimage.jpg'.format(cwd))
    os.remove('{}/{}.jpg'.format(cwd,id))
    print('Uploaded to sm.ms')
    
    if str(the_json['success'])=='False':
        print('Fail uploading')
        print(the_json['message'])
        processed_img_link = the_json['images']
        mk='![]()'.format(the_json['images'])
    else:
        processed_img_link = the_json['data']['url']  # 图片链接
        mk = '![{}]({})'.format(the_json['data']['filename'], the_json['data']['url'])

    # processed_img_link = the_json['data']
    # mk=''

    return processed_img_link, mk


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
    message = "Photo by {} on Unsplash".format(name)
    color = 'rgb(255, 255, 255)' # black color
    d = ImageDraw.Draw(cropped)
    d.text((x, y), message, fill=color, font=font)


def upload(path):
    with open('{}/smms.txt'.format(os.path.dirname(__file__))) as f:
        API_KEY = f.readline()
    headers = {'Authorization': API_KEY}
    files = {'smfile': open(path, 'rb')}
    url = 'https://sm.ms/api/v2/upload'
    result = requests.post(url, files=files, headers=headers).json()
    return result

