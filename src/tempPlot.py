import configparser
import pymysql.cursors
import datetime
import plotly.plotly as py
import plotly.graph_objs as go

def downloadData():
	config = configparser.RawConfigParser()
	config.read('secrets.cfg')
	
	connection = pymysql.connect(host=config.get('_temp', 'host'),
					user=config.get('_temp', 'user'),
					password=config.get('_temp', 'pass'),
					db=config.get('_temp', 'data'),
					cursorclass=pymysql.cursors.DictCursor
				)

	try:
		with connection.cursor() as cursor:
			# Read ALL the records!1
			sql = """SELECT * FROM `ext_Temp`"""
			cursor.execute(sql)
			res = cursor.fetchall()

	finally:
		connection.close()

	return res

def main():
	res = downloadData()

	d = [{ 'Mach_Key' : '0',  'Ext' : {'t_a' : [], 't_t' : [], 'tim' : []} },
		{ 'Mach_Key' : '1',  'Ext' : {'t_a' : [], 't_t' : [], 'tim' : []} },
		{ 'Mach_Key' : '2',  'Ext' : {'t_a' : [], 't_t' : [], 'tim' : []} },
		{ 'Mach_Key' : '3',  'Ext' : {'t_a' : [], 't_t' : [], 'tim' : []} },
		{ 'Mach_Key' : '4',  'Ext' : {'t_a' : [], 't_t' : [], 'tim' : []} },
		{ 'Mach_Key' : '5',  'Ext' : {'t_a' : [], 't_t' : [], 'tim' : []} },
		{ 'Mach_Key' : '6',  'Ext' : {'t_a' : [], 't_t' : [], 'tim' : []} }
	]

	for row in res:
		d[row['Mach_Key']]['Ext']['t_a'].append(row['Temp_Actual'])
		d[row['Mach_Key']]['Ext']['t_t'].append(row['Temp_Target'])
		d[row['Mach_Key']]['Ext']['tim'].append(row['Time'])

	data = [go.Scatter(x=d[0]['Ext']['tim'], y=d[0]['Ext']['t_a'], name='0 Act'), 
		go.Scatter(x=d[0]['Ext']['tim'], y=d[0]['Ext']['t_t'], name='0 Tar'),
		go.Scatter(x=d[1]['Ext']['tim'], y=d[1]['Ext']['t_a'], name='1 Act'),
		go.Scatter(x=d[1]['Ext']['tim'], y=d[1]['Ext']['t_t'], name='1 Tar'),
		go.Scatter(x=d[2]['Ext']['tim'], y=d[2]['Ext']['t_a'], name='2 Act'),
		go.Scatter(x=d[2]['Ext']['tim'], y=d[2]['Ext']['t_t'], name='2 Tar'),
		go.Scatter(x=d[3]['Ext']['tim'], y=d[3]['Ext']['t_a'], name='3 Act'),
		go.Scatter(x=d[3]['Ext']['tim'], y=d[3]['Ext']['t_t'], name='3 Tar'),
		go.Scatter(x=d[4]['Ext']['tim'], y=d[4]['Ext']['t_a'], name='4 Act'),
		go.Scatter(x=d[4]['Ext']['tim'], y=d[4]['Ext']['t_t'], name='4 Tar'),
		go.Scatter(x=d[5]['Ext']['tim'], y=d[5]['Ext']['t_a'], name='5 Act'),
		go.Scatter(x=d[5]['Ext']['tim'], y=d[5]['Ext']['t_t'], name='5 Tar'),
		#go.Scatter(x=d[6]['Ext']['tim'], y=d[6]['Ext']['t_a'], name='6 Act'),
		#go.Scatter(x=d[6]['Ext']['tim'], y=d[6]['Ext']['t_t'], name='6 Tar')
	]

	layout=go.Layout(
		title='Clemson Makerspace Temperatures',
		showlegend=True,
		xaxis=dict(title='Date and Time'),
		yaxis=dict(title='Degrees Celsius')
	)

	fig = go.Figure(data=data, layout=layout)

	py.plot(fig)

if __name__ == '__main__':
	main()
