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
	timeList = []

	midnight = time()

	for row in d:
		wDay.append(row.isoweekday())#row.isoweekday()))
		timeList.append(datetime(2017,1,24,row.time().hour, row.time().minute, row.time().second, row.time().microsecond))

	timeList, wDay = (list(t) for t in zip(*sorted(zip(timeList, wDay))))

	trace0 = go.Histogram2d(x=timeList, y=wDay, #histnorm='probability',
			autobinx=True,
			nbinsx=(72),
			#xbins=dict(start=datetime(2017,1,24), end=datetime(2017,1,25), size=24),
			autobiny=False,
			ybins=dict(start=0, end=7, size=1),
			colorscale=[[0, 'rgb(82,45,128)'],
				[1, 'rgb(234,106,32)']]
			)

	trace1 = go.Scatter(x=timeList, y=wDay,
			mode='markers',
			showlegend=False,
			marker=dict(
				symbol='x',
				opacity=0.7,
				color='white',
				size=8,
				line=dict(width=1)
			)
		)

	data = [trace0]#[trace0, trace1]	
	layout = go.Layout(
		title='Makerspace Utilization Heatmap',
		xaxis = dict(
				title='Military Time'
				
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

	py.plot(fig)

if __name__ == '__main__':
	main()
