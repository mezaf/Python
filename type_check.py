string = 'asd123AA'

for a in string:
	if a in ['a-z']:
		print(a)

import pytz
import datetime
date = 'Sun 10 May 2015 13:54:36 -0700'
da = 'Sun 10 May 2015 13:54:36 -0000'
real_date = datetime.datetime.strptime(date,'%a %d %b %Y %H:%M:%S %z')
real_date_ = datetime.datetime.strptime(da,'%a %d %b %Y %H:%M:%S %z')
diff = (real_date_ - real_date).total_seconds()
print(int(abs(diff)))
