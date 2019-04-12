import json

def upper_flat_json(obj,keys=[]):
    def flat_json(obj, new_obj={}, keys=[]):
        for key, value in obj.items():
            if isinstance(value, dict):
                new_obj = flat_json(obj[key], new_obj, keys + [key])
            else:
                new_obj['_'.join(keys + [key])] = value
        return new_obj
    return flat_json(obj)

def handle_list(obj,new_obj = []):
	for data in range(len(obj)):
		data = obj.pop()
		if isinstance(data,list):
			handle_list(data,new_obj)
		else:
			new_obj.append(data)
	return(new_obj)


with open('data.json', 'r') as file:
	new_obj = []
	obj = json.loads(file.read())
	i = True
	while i:
		i = False
		if isinstance(obj,list):
			for _ in range(len(obj)):
				data = obj.pop()
				for k,v in data.items():
					if isinstance(v,list):
						i = True
						for _ in range(len(v)):
							data[k] = v.pop()
							new_obj.append(data.copy())
							print(obj)
						break
					elif isinstance(v,dict):
						new_obj.append(upper_flat_json(data).copy())
		else: 
			new_obj.append(data.copy())
		obj = new_obj
		print(new_obj,obj)
	# obj = handle_list(obj)
	print(obj)