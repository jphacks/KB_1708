
class ocrparser():
    def __init__(self, resp: dict):
        self.resp = resp

    def get_ocr_strings(self, resp) -> [str]:
        ocred_string = resp['textAnnotations'][0]['description']
        splitted_strings = ocred_string.split('/n')

        return splitted_strings

