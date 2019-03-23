import urllib.request, json, pandas, datetime

site= "http://whattomine.com/asic.json"
hdr = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	}

req = urllib.request.Request(site, headers=hdr)

date_tag = datetime.datetime.now().strftime('_%Y%m%d')

page = urllib.request.urlopen(req)

string_response = page.read().decode('utf-8')

coins_json = json.loads(string_response)

coins_data =pandas.DataFrame()
coins_data = pandas.DataFrame.from_dict(coins_json['coins'],orient='index')
coins_data.to_csv('coins_data'+date_tag,sep=',') 