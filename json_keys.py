import json
def upper_flat_json(obj,json_list):
    def flat_json(obj, new_obj={}, keys=[]):
        for key, value in obj.items():
            if isinstance(value, dict):
                new_obj = flat_json(obj[key], new_obj, keys + [key])
            else:
                new_obj['_'.join(keys + [key])] = value
        return new_obj
    return flat_json(obj)

def check_json(obj,keys=[],json_list=[]):
    try:
        data = json.loads(obj)
        if isinstance(data,dict):
            data = flat_json(data)
        else:
            data = multiple_json(data,keys)
    except:
        print('error grave')
        # for i in json_list:
        #     print(i)
    return data 

def multiple_json(obj,keys,json_list=[]):
    for data in obj:
        # json_list[obj.index(data)] = flat_json(data)
        json_list.append(upper_flat_json(data,json_list,keys))
    return json_list

def list_atts(obj, key,json_list=[]):
    print (obj)
    # for att in obj[key]:
    #     obj[key] = att
    #     json_list.append(obj)
    # return json_list
with open('data.json', 'r') as file:
    
    print (asd_list)