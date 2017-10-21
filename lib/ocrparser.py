
class Ocrparser():
    '''
    googleocrで画像から文字列を取得して,その文字列情報(resp)をパースする。
    パースした文字列はリストで返す

    :return spllited_strings:
    '''
    def __init__(self, resp: dict):
        self.resp = resp

    def get_ocr_strings(self, resp: dict) -> [str]:
        ocred_string = resp['textAnnotations'][0]['description']
        splitted_strings = ocred_string.split('/n')

        return splitted_strings


