import json
def upper_flat_json(obj):
    def flat_json(obj, new_obj={}, keys=[]):
        for key, value in obj.items():
            if isinstance(value, dict):
                new_obj = flat_json(obj[key], new_obj, keys + [key])
            else:
                new_obj['_'.join(keys + [key])] = value
        return new_obj
    return flat_json(obj)

def check_json(obj,json_list=[]):
    try:
        data = json.loads(obj)
        if isinstance(data,dict):
            data = flat_json(data)
        else:
            data = multiple_json(data)
    except:
        # print(json_list)
        for i in json_list:
            print(i)
    return data 

def multiple_json(obj,json_list=[]):
    for data in obj:
        # json_list[obj.index(data)] = flat_json(data)
        # print(obj)
        json_list.append(upper_flat_json(data).copy())
        data = json.loads(json.dumps(json_list.pop()))
        for k,v in data.items():
            try:
                multiple_json(json.loads(v),json_list)
            except:
                if isinstance(v,list):
                    for i in v:
                        data[k] = i
                        json_list.append(data.copy())
    return json_list

with open('data.json', 'r') as file:
    # print(flat_keys(file.read()))
    print(check_json(file.read()))