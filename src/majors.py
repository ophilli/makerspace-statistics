import configparser
import pymysql.cursors
import collections
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
from datetime import datetime
from datetime import timedelta
from datetime import time
from datetime import date

def downloadData(startDate):
	config = configparser.RawConfigParser()
	config.read('secrets.cfg')
	
	connection = pymysql.connect(host=config.get('_login', 'host'),
					user=config.get('_login', 'user'),
					password=config.get('_login', 'pass'),
					db=config.get('_login', 'data'),
					cursorclass=pymysql.cursors.DictCursor
				)

	try:
		with connection.cursor() as cursor:
			# Read ALL the records!1
			sql = """SELECT * FROM `makerspace`.`signin` WHERE `timestamp` BETWEEN %s AND %s"""
			sqlData = (startDate, startDate + timedelta(5)) #  WHERE `username` LIKE 'thorb'"""
			cursor.execute(sql, sqlData)
			res = cursor.fetchall()

	finally:
		connection.close()

	return res

def main():	
	startDate = date(2017, 2, 6)

	res = downloadData(startDate)

	d = []

	for row in res:
		d.append({'m' : row['major_code'], 't' : row['timestamp']}) if row['major_code'] !=  None else d.append({'m' : 'Unknown', 't' : row['timestamp']})

	cnt = collections.Counter()

	for word in d:
		cnt[word['m']] += 1

	trace = go.Pie(labels=list(cnt.keys()), values=list(cnt.values()))

	data = [trace]	
	layout = go.Layout(title='Makerspace Major Breakdown')

	fig = go.Figure(data=data, layout=layout)	

	py.plot(fig)

if __name__ == '__main__':
	main()
