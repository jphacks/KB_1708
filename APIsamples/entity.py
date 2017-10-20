from goolabs import GoolabsAPI
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

app_id = config['gooAPI']['id']
api = GoolabsAPI(app_id)

ret = api.entity(sentence=u"鈴木さんがきょうの9時30分に横浜に行きます。")

print(ret)
