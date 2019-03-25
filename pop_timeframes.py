import json

data = {
	"ymd":[20191210,20191211,20191215,20181204,20181213,20181214,20181220,20181223,20181221,20181222,20181130,20191129,20191130]
}

init_val = None
last_val = None
data_set = json.loads(json.dumps(data))
range_set = {}
for i in range(len(data_set['ymd'])):
	data_set['ymd'].sort()
	list_set = data_set['ymd']
	if init_val:
		if init_val == 20191115:
			print init_val, range_set
		if list_set[i] - list_set[i-1] > 1 and not last_val:
			last_val = list_set[i-1]
			range_set[init_val] = [init_val,init_val]
			init_val = list_set[i]
		elif list_set[i] - list_set[i-1] == 1:
			last_val = list_set[i]
			range_set[init_val] = [init_val,last_val]
		elif list_set[i] - list_set[i-1] > 1:
			last_val = list_set[i-1]
			range_set[init_val] = [init_val,last_val]
			init_val = list_set[i]
	else:
		init_val = list_set[i]
		continue
	try:
		aplpha = range_set[init_val]
	except:
		range_set[init_val] = [init_val,init_val]

for key,val in range_set.items():
	print val[0],val[1]