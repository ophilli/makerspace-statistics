import configparser
import pymysql.cursors
import collections
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
from datetime import datetime
from datetime import timedelta
from datetime import time

def downloadData():
	config = configparser.RawConfigParser()
	config.read('secrets.cfg')
	
	connection = pymysql.connect(host=config.get('_sql', 'hostname'),
					user=config.get('_sql', 'username'),
					password=config.get('_sql', 'password'),
					db=config.get('_sql', 'database'),
					cursorclass=pymysql.cursors.DictCursor
				)

	try:
		with connection.cursor() as cursor:
			# Read ALL the records!1
			sql = """SELECT * FROM `makerspace`.`signin`"""
			cursor.execute(sql)
			res = cursor.fetchall()

	finally:
		connection.close()

	return res

def main():
	res = downloadData()

	d = []

	for row in res:
		d.append(row['timestamp']) if row['timestamp'] != None else d.append('Unknown')
			
	l = []

	for row in d:
		l.append(timedelta(days=row.isoweekday(), hours=row.time().hour, minutes=row.time().minute,
			seconds=row.time().second, microseconds=row.time().microsecond))

	l.sort()
	
	wDay = []
	time = []

	for row in d:
		wDay.append(row.isoweekday())
		time.append(row.time())

	time, wDay = (list(t) for t in zip(*sorted(zip(time, wDay))))

	print(len(time), len(wDay))
	data = [
		go.Histogram2d(x=time, y=wDay, #histnorm='probability',
			autobinx=False,
			xbins=dict(start=0, end=1660, size=25),
			autobiny=False,
			ybins=dict(start=0, end=7, size=1),
			colorscale=[[0, 'rgb(12,51,131)'], [0.25, 'rgb(10,136,186)'], 
				[0.5, 'rgb(242,211,56)'], [0.75, 'rgb(242,143,56)'],
				[1, 'rgb(217,30,30)']]
			)
		]
	
	layout = go.Layout(
		title='Makerspace Utilization Heatmap',
		xaxis = dict(
				title='Military Time',
				#type="date"
			),
		yaxis = dict(
				title='Days of the Week',
				ticktext=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 
					'Thursday', 'Friday', 'Saturday'],
				tickvals=[0.5,1.5,2.5,3.5,4.5,5.5,6.5]
			)
	)
			
	#data = [go.Scatter(x=timestamp, y=weekday, mode='markers')]
	fig = go.Figure(data=data, layout=layout)	

	offline.plot(fig, image='png')

if __name__ == '__main__':
	main()
