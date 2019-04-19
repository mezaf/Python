import json
from copy import deepcopy


def upper_flat_json(obj,keys=[]):
	def flat_json(obj, new_obj={}, keys=[]):
		for key, value in obj.items():
			if isinstance(value, dict):
				new_obj = flat_json(obj[key], new_obj, keys + [key])
			else:
				new_obj['_'.join(keys + [key])] = value
		return new_obj
	return flat_json(obj)

def read_json(file=None,json_new_obj=[]):
	if file:
		try:
			obj = json.loads(file.read())
		except:
			obj = json.loads(json.dumps(file.read()))
		data = validation(obj)
	else:
		return 'No JSON provided'
	return data

def handle_list(list_obj,list_new_obj=[]):
	for key, value in list_obj.items():
		if isinstance(value, list):
			for idx,val in enumerate(value):
				list_obj[key] = val
				list_new_obj.append(list_obj.copy())
			break
		elif isinstance(value, dict):
			list_new_obj.append(list_obj)
	return list_new_obj

def validation(val_obj,final_obj=[],types=[]):
	i = True
	while i:
		i = False
		alpha=0
		data = val_obj.pop(0)
		for key, value in data.items():
			if isinstance(value, dict):
				val_obj.append(upper_flat_json(data).copy())
				data = val_obj.pop(-1)
				i=True
				break
		for key, value in data.items():
			alpha += 1
			if isinstance(value,list):
				val_obj.extend(handle_list(data,[]))
				i = True
				break
			elif alpha == len(data):
				val_obj.append(data.copy())
	return(val_obj)

with open('data.json', 'r') as file:
	print(read_json(file))