This script is for automating the process of cropping, resizing, adding author's information, compressing, and uploading an image.

- The compressing service I use [tinypng](https://tinypng.com)
- The storage for image I user [sm.ms](https://sm.ms/)
- This script works only for the image download from [unsplash.com](https://unsplash.com/), since I use regular expression operations to get the author's name from file name.

## Usage

To use correctly, you need to create an ```api.txt``` file that contains only the API key for  [tinypng](https://tinypng.com). To generate an API key, you can check [https://tinypng.com/developers](https://tinypng.com/developers).

```main.py``` can be easily run in the terminal with the command:
```bash
python main.py
```
Once it launched, you can drag and drop any image on it.


```automator.py``` can be used in Mac's Automator. By building a server with Automator, I can right click on any image and run the script, or use a shortcut to run the script.
