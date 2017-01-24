import configparser
import pymysql.cursors
import collections
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime

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
	di = []

	for row in res:
		d.append(row['timestamp']) if row['timestamp'] != None else d.append('Unknown')
		di.append(row['id']) if row['id'] != None else di.append('Unknown')
		
	data = [go.Scatter(x=d, y=di)]
	py.plot(data)

if __name__ == '__main__':
	main()
