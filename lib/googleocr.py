from base64 import b64encode
import json
import requests


class GoogleOCR:
    def __init__(self, api_key):
        self.api_key = api_key
        self.end_point_url = 'https://vision.googleapis.com/v1/images:annotate'
        self.headers = {'Content-Type': 'application/json'}

    def create_image_data_list(self, img_paths: list, max_results=1):
        """
        それぞれの画像をエンコード，リスト化する
        :param img_paths: 判定する画像のパス（リスト）
        :return: エンコードされた各画像データ
        """
        img_requests = []
        for img_path in img_paths:
            with open(img_path, 'rb') as f:
                ctxt = b64encode(f.read()).decode()
                img_requests.append({
                    'image': {'content': ctxt},
                    'features': [{
                        'type': 'TEXT_DETECTION',
                        'maxResults': max_results
                    }]
                })
        return img_requests

    def convert_images(self, img_paths: list, max_results=1):
        """
        画像データをPOST用データに変換
        :param img_paths:
        :return:　POST用データ
        """
        dict = self.create_image_data_list(img_paths, max_results)
        return json.dumps(
            {
                "requests": dict
            }
        ).encode()

    def recognize_image(self, img_paths, max_results=1, timeout=None):
        response = requests.post(self.end_point_url,
                                 data=self.convert_images(img_paths, max_results),
                                 params={'key': self.api_key},
                                 headers=self.headers,
                                 timeout=timeout)
        return response
