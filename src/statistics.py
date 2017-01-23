import configparser
import pymysql.cursors
import collections
import plotly.plotly as py
import plotly.graph_objs as go

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
		d.append(row['class_code']) if row['class_code'] != None else d.append('Unknown')

	cnt = collections.Counter()

	for word in d:
		cnt[word] += 1

	trace = go.Pie(labels=list(cnt.keys()), values=list(cnt.values()))

	print(sum(cnt.values()))

	py.plot([trace])

if __name__ == '__main__':
	main()
