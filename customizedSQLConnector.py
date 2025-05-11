import mysql.connector

'''
this file is created just for connecting to my sql database and extrac tools according to mysql.connector
'''

def connect_sql():
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		database="classicmodels"
	)
	return mydb

def close(mydb):
	mydb.close()
