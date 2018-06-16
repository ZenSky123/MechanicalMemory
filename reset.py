import json
import codecs

data = json.load(codecs.open('data.json', 'r', 'utf-8'))
for d in data:
    d["count"]=0

json.dump(data, codecs.open('data.json', 'w', 'utf-8'), ensure_ascii=False, indent=4)
