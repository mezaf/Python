import bisect
import calendar
import datetime as dt
import java.io
import json
import subprocess
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback

def read_json_attributes(file,tag=None):
    data = json.loads(json.dumps(file))
    for key, value in data.items():
        if type(value) != dict and tag:
            atts[tag+'.'+key] = value
        elif type(value) == dict and tag:
            read_json_attributes(value,tag + '.' + key)
        elif type(value) != dict:
            atts[key] = value
        elif type(value) == dict:
            read_json_attributes(value,key)
    tag = str()
    return atts

cat = subprocess.Popen(['hdfs','dfs','-cat','/user/FernandM/Metadata/tester.json'], stdout=subprocess.PIPE)
data = json.loads(cat.stdout.read())
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