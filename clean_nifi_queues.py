import json
import urllib.request as req

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
            ,'Content-Type':'application/json'
            ,'Accept':'application/json'
            ,'Connection':'keep-alive'
            ,'Accept-Encoding': 'gzip, deflate'
            ,'Referer':'http://phoenix.paraport.com:1055/swagger/ui/index'
            }
get_groups = 'http://localhost:8080/nifi-api/flow/process-groups/96649e4d-016c-1000-4c04-297507e11e44'

group_request = req.Request(get_groups,method='GET')
groups = json.loads(req.urlopen(group_request).read())

ids = [i['id'] for i in groups['processGroupFlow']['flow']['processGroups']]

get_connections = 'http://localhost:8080/nifi-api/process-groups/{id}/connections'
connections = []
for i in ids:
    connection_request = req.Request(get_connections.format(id=i),method='GET')
    request_connections = json.loads(req.urlopen(connection_request).read())
    for j in request_connections['connections']:
        connections.append(j['id'])

delete_queues = 'http://localhost:8080/nifi-api/flowfile-queues/{id}/drop-requests'
[req.urlopen(req.Request(url=delete_queues.format(id=i),method='POST')).read() for i in connections]