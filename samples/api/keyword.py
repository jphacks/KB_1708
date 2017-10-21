from goolabs import GoolabsAPI
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

app_id = config['gooAPI']['id']
api = GoolabsAPI(app_id)

ret = api.keyword(
    request_id="keyword-req001",
    title="「和」をコンセプトとする 匿名性コミュニケーションサービス「MURA」",
    body="NTTレゾナント株式会社（本社：東京都港区、代表取締役社長：若井 昌宏",
    max_num=10,
    forcus="ORG",
)

print(ret)
