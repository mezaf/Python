import bisect
import datetime as dt
import calendar
import java.io
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import bisect
import datetime as dt
import calendar

def today():
	today = dt.date.today()
	return(today.strftime('%Y%m%d'))

def yesterday():
	yesterday = dt.date.today()-dt.timedelta(days=1)
	return(yesterday.strftime('%Y%m%d'))

def first_day_current_month():
	now = dt.datetime.strptime(today(),'%Y%m%d')
	day = dt.date(now.year,now.month,1)
	return(day.strftime('%Y%m%d'))

def last_day_current_month():
	now = dt.datetime.today()
	last_day = calendar.monthrange(now.year,now.month)[1]
	day = dt.date(now.year,now.month,last_day)
	return(day.strftime('%Y%m%d'))

def last_day_current_quarter():
	today = dt.date.today()
	qends = [dt.date(today.year, month, 1) for month in (3,6,9,12)]
	idx = bisect.bisect(qends, today)
	return_q = [q.replace(day=calendar.monthrange(q.year,q.month)[1]).strftime('%Y%m%d') for q in qends]
	return str(return_q[idx])

def first_day_current_quarter():
	date = dt.datetime.strptime(last_day_current_quarter(),'%Y%m%d')
	return str(dt.date(date.year,date.month-2,1).strftime('%Y%m%d'))

def last_day_last_month():
	now = dt.datetime.strptime(first_day_current_month(),'%Y%m%d')
	day = now - dt.timedelta(days=1)
	return(day.strftime('%Y%m%d'))

def first_day_last_month():
	now = dt.datetime.strptime(last_day_last_month(),'%Y%m%d')
	day = dt.date(now.year,now.month,1)
	return(day.strftime('%Y%m%d'))

def last_day_last_quarter():
	today = dt.date.today()
	if today.month in [1,2,3]:
		year = today.year-1
	else:
		year = today.year
	qends = [dt.date(year, month, 1) for month in (3,6,9,12)]
	idx = bisect.bisect(qends, today)
	return_q = [q.replace(day=calendar.monthrange(q.year,q.month)[1]).strftime('%Y%m%d') for q in qends]
	return str(return_q[idx-1])

def first_day_last_quarter():
	date = dt.datetime.strptime(last_day_last_quarter(),'%Y%m%d')
	return str(dt.date(date.year,date.month-2,1).strftime('%Y%m%d'))

def year_last_quarter():
	return str(dt.datetime.strptime(last_day_last_quarter(),'%Y%m%d').year)

def last_quarter():
	date = dt.datetime.strptime(last_day_last_quarter(),'%Y%m%d')
	quarter = (date.month-1)//3 + 1
	return str(quarter)

dates = {
	'ppa.today':today()
	,'ppa.yesterday':yesterday()
	,'ppa.first_day_current_month':first_day_current_month()
	,'ppa.last_day_current_month':last_day_current_month()
	,'ppa.first_day_current_quarter':first_day_current_quarter()
	,'ppa.last_day_current_quarter':last_day_current_quarter()
	,'ppa.first_day_last_month':first_day_last_month()
	,'ppa.last_day_last_month':last_day_last_month()
	,'ppa.first_day_last_quarter':first_day_last_quarter()
	,'ppa.last_day_last_quarter':last_day_last_quarter()
	,'ppa.year_last_quarter':year_last_quarter()
	,'ppa.last_quarter':last_quarter()
}

flowFile = session.get() 
if (flowFile != None):
    flowFile = session.putAllAttributes(flowFile, dates)
    session.transfer(flowFile, REL_SUCCESS)