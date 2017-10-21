from googleocr import GoogleOCR
from goolabs import  GoolabsAPI
import ocrparser
import question_generator
import json
import configparser
from os.path import exists
import random

# config

class OcrWrapper():
    def __init__(self, api_key):
        self.ocr = GoogleOCR(api_key=api_key)

    def get_ocr_result(self, img_paths: [str]):
        ocr_strings = []
        res = self.ocr.recognize_image(img_paths)
        if res.status_code != 200 or res.json().get('error'):
            print('error happen!!!')
            print(res.text)

        else:
            json_list = []
            for idx, resp in enumerate(res.json().get('responses')):
                json_list.append(json.dumps(resp))

                # save JSON file
                f_out_name = './json/' + img_paths[idx] + '.json'
                if not exists(f_out_name):
                    with open(f_out_name, 'w') as f_out:
                        datatxt = json.dumps(resp, indent=2)
                        print("saved", len(datatxt), "bytes to ", f_out_name)
                        f_out.write(datatxt)
            return json_list

    def get_ocr_string(self, json):
        raw_string_data = json.dumps(json)['textAnnotations'[0][0]]
        ocr_string = raw_string_data.replace('/n', '')
        return ocr_string


class GoolabWrapper():
    def __init__(self, api_id):
        self.goolab = GoolabsAPI(api_id)

    def get_keywords_from_ocr_string(self, ocr_string):
        keywords = []
        ret = self.goolab.entity(sentence=ocr_string)
        for idx in range(len(ret['ne_list'])):
            keywords.append(ret['ne_list'][idx][0])

        return keywords

    def generate_selected_num_of_questions(self, keyword, num):
        all_questions = question_generator.QuestionGeneratorOfKeywords.create_questions_with(keyword)
        for i in range(len(all_questions) - num):
            del all_questions[random.randint(0, len(all_questions)-i)]


def generate_questions_from_images():
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


    keywords_list = []
    # atributes_list = []  #keywordの属性が必要な場合
    for ocr_string_ in ocr_strings:
        ret = goo.entity(sentence=ocr_string_)
        for item in range(len(ret['ne_list'])):
            keywords = []
            atributes = []
            keywords.append(ret['ne_list'][item][0])
            # atributes.append(ret['ne_list'][item

    list_of_question_list = []
    for keywords_ in keywords_list:
        question_generator.QuestionGeneratorOfKeywords.convert_keywords_to_qustions_list(keywords_)

    return list_of_question_list