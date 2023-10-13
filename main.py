import json


bf = open('brain-data.json')
brain_data = json.load(bf)


print(json.dumps(brain_data['chunks'][0]['layers'][0]['dynamics']['a'][0], indent=1))







