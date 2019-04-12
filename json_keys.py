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

def check_json(obj,json_list=[], data=[]):
    try:
        data = json.loads(obj)
        if isinstance(data,dict):
            data = flat_json(data)
        else:
            data = multiple_json(data)
    except:
        for i in json_list:
            data = 'error'
    return data 

def multiple_json(obj,json_list=[]):
    for data in obj:
        print(json_list)
        json_list.append(upper_flat_json(data).copy())
        data = json.loads(json.dumps(json_list.pop()))
        print(json_list)
        print(data)
        for k,v in data.items():
            if isinstance(v, list):
                for i in v:
                    # print(i)
                    data[k] = i
                    # print(json_list)
                    json_list.append(data.copy())
                break
    # print (json_list)
    # print('pasada')
    return json_list

with open('data.json', 'r') as file:
    i = True
    data = (check_json(file.read()))
    # print(data)
    while i:
        i = False
        for data_set in data:
            for k,v in data_set.items():
                if isinstance(v, list):
                    data = check_json(json.dumps(data))
                    # print(data)
                    i = True
                elif isinstance(v, dict):
                    data.append(upper_flat_json(data.pop(data.index(data_set))))
                    i = True
        # print('pasada')
            # print('break')