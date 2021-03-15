# Blog Image Processing Automation Script

This is the one of the functions for my personal FastAPI server. It automates the process of cropping, resizing, adding author's information, compressing, and uploading an image.

- The compressing service I use [tinypng](https://tinypng.com)
- The storage for image I use [sm.ms](https://doc.sm.ms/)
- The image resource I use [unsplash.com](https://unsplash.com/documentation)

## Usage

Please create `.env` file at the **Project** root folder and incldues:
```
SMMS_KEY= <sm.ms API key>
UNSPLASH_KEY= <Unsplash Access Key>
TINY_KEY= <tinypng.cpm API key>
```

Call Function `img_process(id,width,height,x_text,y_text)` and it will return a url string and Markdown string for the image.

Args:

- id (str): Image ID
- width (int, optional): The width after processing. 
- height (int, optional): The height after processing.
- x_text (int, optional): The x position for the artist's name on the image.
- y_text (int, optional): The y position for the artist's name on the image. 

Returns:
- Processed image url and Markdown string

### Example for FastAPI

You can also download this theme using Git, execute the following command under your FastAPI server folder:

```git clone https://github.com/iamjohnnyli/blog-image-processing-automation BlogImageProcessor```

If you are using Git to manage your server, add this function as a submodule.
```git submodule add https://github.com/iamjohnnyli/blog-image-processing-automation BlogImageProcessor```

In `main.py` file import processor
```python
from BlogImageProcessor import processor
```
Create server by calling img_process in BlogImageProcessor endpoint.
```python
@app.get("/BlogImageProcessor")
async def BlogImageProcessor(id: str, width: int=1600, height: int=800, x_text: int=40, y_text: int=760):   
    if id:
        return processor.img_process(id,width,height,x_text,y_text)
    else:
        return {"message": 'Missing id paramator in the request.'}
```

In command line run:

```shell
uvicorn main:app --reload --env-file .env
```