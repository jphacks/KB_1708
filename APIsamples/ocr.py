from lib.googleocr import GoogleOCR
import json
import configparser
from os.path import basename

# config
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['googleAPI']['key']

# OCR
ocr = GoogleOCR(api_key=api_key)
img_paths = [
    './img/ocr_test1.jpg',
    './img/ocr_test2.jpg'
]
res = ocr.recognize_image(img_paths)
if res.status_code != 200 or res.json().get('error'):
    print('error happen!!!')
    print(res.text)

else:
    for idx, resp in enumerate(res.json().get('responses')):
        # save JSON file
        f_out_name = './json/' + basename(img_paths[idx]) + '.json'
        with open(f_out_name, 'w') as f_out:
            datatxt = json.dumps(resp, indent=2)
            print("saved", len(datatxt), "bytes to ", f_out_name)
            f_out.write(datatxt)

        # print the plaintext to screen for convenience
        print("---------------------------------------------")
        t = resp['textAnnotations'][0]
        print("    Bounding Polygon:")
        print(t['boundingPoly'])
        print("    Text:")
        print(t['description'])

print('ocr program finish')