from .googleocr import GoogleOCR
from goolabs import GoolabsAPI
from . import question_generator
import json
import random


class OcrWrapper(object):
    def __init__(self, api_key):
        self.ocr = GoogleOCR(api_key=api_key)

    def get_ocr_result(self, img_paths: [str]):
        json_list = []
        res = self.ocr.recognize_image(img_paths)
        if res.status_code != 200 or res.json().get('error'):
            pass
        else:
            for idx, resp in enumerate(res.json().get('responses')):
                json_list.append(json.dumps(resp))
        return json_list

    def get_ocr_string(self, j):
        raw_string_data = json.loads(j)['textAnnotations'][0]['description']
        ocr_string = raw_string_data.replace('/n', '')
        return ocr_string


class GoolabWrapper(object):
    def __init__(self, api_id):
        self.goolab = GoolabsAPI(api_id)

    def get_keywords_from_ocr_string(self, ocr_string):
        keywords = []
        ret = self.goolab.entity(sentence=ocr_string)
        for idx in range(len(ret['ne_list'])):
            keywords.append(ret['ne_list'][idx][0])
        return keywords

    def generate_selected_num_of_questions(self, keyword, num):
        q_gen = question_generator.QuestionGeneratorOfKeywords(keyword)
        all_questions = q_gen.create_questions_with()
        for i in range(len(all_questions) - num):
            del all_questions[random.randint(0, len(all_questions)-i)]
        return all_questions
