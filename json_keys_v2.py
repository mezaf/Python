import json
def flat_json(obj,json_list=[]):
	print(obj)
	def flat_json_a(obj,newObj={},keys=[]):
		for k,v in obj.items():
			if isinstance(v,dict):
				flat_json_a(obj[k],newObj,keys+[k])
			else:
				newObj['_'.join(keys+[k])] = v
		return newObj
	return flat_json_a(obj)
json_list = []
with open('data.json', 'r') as file:
	raw_data = file.read()
	flat_file = None
	try:
		data = json.loads(raw_data)
		if isinstance(data,list):
			for obj in data:
				if isinstance(obj,dict):
					json_list.append(flat_json(obj))

		else:
			json_list.append(flat_json(json.loads(data)))
	except:
		if isinstance(json.loads(raw_data),list):
			for i in raw_data:
				flat_file = 'nada'
	print(json_list)
