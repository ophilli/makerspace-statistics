import configparser
import pymysql.cursors
import collections

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

majors = []

for row in res:
	majors.append(row['major_code']) if row['major_code'] != None else majors.append('None')

print(uniqueList(majors))

print(count2Dict(uniqueList(majors), majors))
