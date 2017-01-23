import configparser
import pymysql.cursors
import collections

def transpose(twoDList):
	# Assume that 2dList is a square 2 dimensional list

	trans = []

	for c in range(len(twoDList[0])):
		trans.append([])
		for row in twoDList:
			trans[c].append(row[c]) if row[c] != None else trans[c].append('None')
	return trans

def uniqueList(oneDList):
	return sorted(list(set(oneDList)))

def count2Dict(set, list):
	temp = {}
	for val in set:
		count = 0
		for row in list:
			if row == val:
				count = count + 1
		temp[val] = count
	return temp

config = configparser.RawConfigParser()
config.read('secrets.cfg')

connection = pymysql.connect(host=config.get('_sql', 'hostname'),
				user=config.get('_sql', 'username'),
				password=config.get('_sql', 'password'),
				db=config.get('_sql', 'database')
				)

try:
	with connection.cursor() as cursor:
		# Read ALL the records!1
		sql = """SELECT * FROM `makerspace`.`signin`"""
		cursor.execute(sql)
		res = cursor.fetchall()

finally:
	connection.close()

zipped = transpose(res)

finalDict = count2Dict(uniqueList(zipped[6]), zipped[6])

sDict = collections.OrderedDict(sorted(finalDict.items(), key=lambda t: t[0]))

print(sDict)

