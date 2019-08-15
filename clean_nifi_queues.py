import json, requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
            ,'Content-Type':'application/json'
            ,'Accept':'application/json'
            ,'Connection':'keep-alive'
            ,'Accept-Encoding': 'gzip, deflate'
            ,'Referer':'http://phoenix.paraport.com:1055/swagger/ui/index'
            }
get_groups = 'http://localhost:8080/nifi-api/flow/process-groups/96649e4d-016c-1000-4c04-297507e11e44'
data = {
    "listingRequest": {"id":"9678fe1d-016c-1000-aac2-7eec798158d1"}
}
r = requests.get(url=get_groups)
groups = json.loads(r.text)  
ids = [i['id'] for i in groups['processGroupFlow']['flow']['processGroups']]

get_connections = 'http://localhost:8080/nifi-api/process-groups/{id}/connections'
connections = []
for i in ids:
    request_connections = json.loads(requests.get(url=get_connections.format(id=i)).text)
    for j in request_connections['connections']:
        connections.append(j['id'])

delete_queues = 'http://localhost:8080/nifi-api/flowfile-queues/{id}/drop-requests'
[requests.post(url=delete_queues.format(id=i)) for i in connections]