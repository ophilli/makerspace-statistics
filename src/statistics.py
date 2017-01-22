import configparser
import pymysql.cursors

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
		sql = """SELECT `id`, `username`, `timestamp`, `first`, `last`,
			`email`, `major_code`, `class_code`, `college_code`,
			`role`, `ip` FROM `makerspace`.`signin`"""
		cursor.execute(sql)
		bulkData = cursor.fetchall()
		
finally:
	connection.close()

