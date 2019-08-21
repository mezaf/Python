import json
import urllib2
import urllib
import ssl
import sys
class CleanNiFiQueues(object):
   """
       No more manual delete of Queues
   """
   def __init__(self, server,port,username,password):
       super(CleanNiFiQueues, self).__init__()
       # Server Info
       self.server = server
       self.port = port
       # Turn On/Off SSL Auth
       self.ctx = ssl.create_default_context()
       self.ctx.check_hostname = False
       self.ctx.verify_mode = ssl.CERT_NONE
       # Auth
       data = urllib.urlencode({"username":username,"password":password})
       acces_token = 'https://sea-2673-01.paraport.com:9443/nifi-api/access/token'
       token_req = urllib2.Request(acces_token)
       token_req.add_header("Content-Type","application/x-www-form-urlencoded")
       self.token = urllib2.urlopen(token_req,data,context=self.ctx).read()
   def get_connections(self,group_ids,connection_ids=[]):
       get_connections = 'https://{server}:{port}/nifi-api/process-groups/{id}/connections'
       connections = []
       for i in group_ids:
           connection_request = urllib2.Request(get_connections.format(server=self.server,port=self.port,id=i))
           connection_request.add_header("Authorization", "Bearer %s" % self.token)
           request_connections = json.loads(urllib2.urlopen(connection_request,context=self.ctx).read())
           for j in request_connections['connections']:
               connections.append(j['id'])
       return connections
   def get_groups(self,id,group_ids=[]):
       group_ids.append(id)
       get_groups = 'https://{server}:{port}/nifi-api/flow/process-groups/{id}'
       group_request = urllib2.Request(get_groups.format(server=self.server,port=self.port,id=id))
       group_request.add_header("Authorization", "Bearer %s" % self.token)
       groups = json.loads(urllib2.urlopen(group_request,context=self.ctx).read())
       if  groups['processGroupFlow']['flow']['processGroups']:
           [self.get_groups(i['id']) for i in groups['processGroupFlow']['flow']['processGroups']]
       return group_ids
   def del_flowfiles(self,connection_ids):
       for i in connection_ids:
           delete_queue = 'https://{server}:{port}/nifi-api/flowfile-queues/{id}/drop-requests'
           try:
               del_request = urllib2.Request(url=delete_queue.format(server=self.server,port=self.port,id=i),data='asd')
               del_request.add_header("Authorization", "Bearer %s" % self.token)
               urllib2.urlopen(del_request,context=self.ctx).read()
           except:
               print('Id '+i+' not found, continue')
       print('Queues deleted')
username = sys.argv[1]
password = sys.argv[2]
server = sys.argv[3]
port = sys.argv[4]
process = sys.argv[5]
NiFi = CleanNiFiQueues(server,port,username,password)
print 'Getting sub groups'
groups = NiFi.get_groups(process)
print 'Getting connections'
connections = NiFi.get_connections(groups)
print 'Queue cleaning'
NiFi.del_flowfiles(connections)