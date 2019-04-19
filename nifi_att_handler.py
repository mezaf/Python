import bisect
import calendar
import datetime as dt
import java.io
import json
import subprocess
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback

import json
from copy import deepcopy


def upper_flat_json(obj,keys=[]):
    def flat_json(obj, new_obj={}, keys=[]):
        for key, value in obj.items():
            if isinstance(value, dict):
                new_obj = flat_json(obj[key], new_obj, keys + [key])
            else:
                new_obj['.'.join(keys + [key])] = value
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

cat = subprocess.Popen(['hdfs','dfs','-cat','/user/FernandM/Metadata/tester.json'], stdout=subprocess.PIPE)
data = read_json(cat.stdout.read())
flowFile = session.get()
flowFiles = []
if flowFile:
    NiFi_Attributes = {}
    for k,v in flowFile.getAttributes().iteritems():
        NiFi_Attributes[k] = v
    for d in data:
        newFlowFile = session.create()
        atts = {}
        for k,v in read_json_attributes(d).items():
            NiFi_Attributes[k] = str(v)
        newFlowFile = session.putAllAttributes(newFlowFile,NiFi_Attributes)
        flowFiles.append(newFlowFile)
    session.transfer(flowFiles, REL_SUCCESS)
    session.transfer(flowFile,REL_FAILURE)