import configparser
import json
import codecs

cfg = configparser.ConfigParser()
cfg.read('config.ini')
data_filename = cfg.get('path', 'filename')

data = json.load(codecs.open(data_filename, 'r', 'utf-8'))

for d in data:
    d["count"] = 0

json.dump(data, codecs.open(data_filename, 'w', 'utf-8'), ensure_ascii=False, indent=4)
