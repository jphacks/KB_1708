from googleocr import GoogleOCR
from goolabs import  GoolabsAPI
import ocrparser
import question_generator
import json
import configparser
from os.path import exists

# config
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['googleAPI']['key']
app_id = api_key
goo = GoolabsAPI(app_id)

# OCR
img_paths = []
ocr = GoogleOCR(api_key=api_key)

res = ocr.recognize_image(img_paths)
ocr_strings = []
if res.status_code != 200 or res.json().get('error'):
    print('error happen!!!')
    print(res.text)

else:
    for idx, resp in enumerate(res.json().get('responses')):
        parser = ocrparser.Ocrparser(resp)
        ocr_strings.append(parser.get_ocr_string())

        # save JSON file
        f_out_name = './json/' + img_paths[idx] + '.json'
        if not exists(f_out_name):
            with open(f_out_name, 'w') as f_out:
                datatxt = json.dumps(resp, indent=2)
                print("saved", len(datatxt), "bytes to ", f_out_name)
                f_out.write(datatxt)

for ocr_string_ in ocr_strings:
    ret = goo.entity(sentence=ocr_string_)
