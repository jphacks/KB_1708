
class Ocrparser():
    '''
    googleocrで画像から文字列を取得して,その文字列情報(resp)をパースして返す

    :return ocr_strings:
    '''
    def __init__(self, resp: dict):
        self.resp = resp

    def get_ocr_strings(self, resp: dict) -> [str]:
        raw_ocr_string = resp['textAnnotations'][0]['description']
        ocr_string = raw_ocr_string.replace('/n', '')

        return ocr_string


