import sqlite3
from sqlite3 import Error


def create_sql_connection():
	'''

	Creates database.
	return database connection
	
	'''
	try:
		con = sqlite3.connect('reports3d_database.db', check_same_thread=False)
		return con
	except Error:
		print(Error)


def check(con):
	'''

	Enables foreign key constaint in sqlite3
	
	'''
	cursor=con.cursor()
	cursor.execute("PRAGMA foreign_keys=on;")
	con.commit()


def create_sql_table(con):
	'''

	Creates tables in database
	args: database connection

	'''
	cursorObj = con.cursor()
	cursorObj.execute("CREATE TABLE IF NOT EXISTS doctor_table(doc_id integer PRIMARY KEY AUTOINCREMENT, username text NOT NULL, email varchar(30) NOT NULL UNIQUE, password varchar NOT NULL)")
	cursorObj.execute("CREATE TABLE IF NOT EXISTS patient_table(pat_id integer PRIMARY KEY, doc_id integer NOT NULL, name text NOT NULL, comments text, link varchar, FOREIGN KEY (doc_id) REFERENCES doctor_table(doc_id))")
	con.commit()


def doctor_register():
	'''
	
	populated from the webinterface directly
	Function to MANUALLY register new doctor details
	Pass details from the web form here
	(remove the manual inputs)

	'''
	# doc_id=int(input("Enter ID: "))
	username=input("Enter username: ")
	email=input("Enter email: ")
	password=input("Enter password: ")
	return (username, email, password)


def doctor_insert(con,values_to_insert):
	'''

	Populates the doctor table, post doctor registration
	args:
	con- database connection
	values_to_insert- registrattion details

	'''
	cursorObj=con.cursor()
	query="INSERT INTO doctor_table(username, email, password) VALUES(?,?,?)"
	cursorObj.execute(query,values_to_insert)
	con.commit()


def login(con, email, password):
	'''
	Log-in check
	
	Args:
	sql table connection

	'''
	cursor=con.cursor()
	cursor.execute("SELECT doc_id, email, password FROM doctor_table")
	rows=cursor.fetchall()
	for row in rows:
		if row[1]==email:
			if row[2]==password:
				return True, row[0]  #Return doctor ID in order to ensure only that doctors patients can be accessed.
	return False, -99
	con.commit()


def patient_insert(con, values_to_insert):
	'''

	Populates the patient table, post patient registration
	args:
	con- database connection
	values_to_insert- registrattion details

	'''
	cursorObj=con.cursor()
	query="INSERT INTO patient_table (pat_id, doc_id, name, comments, link) VALUES(?,?,?,?,?)"
	try:
		cursorObj.execute(query,values_to_insert)
	except Error:
		print(Error)
		print("Patient needs valid doctor_id")
	con.commit()


def find_patient(con, d_id):
	'''

	To retrieve the link for particular patient
	args:
	con- database connection
	doc_id- doctor whose patient files need to be accessed 

	'''
	cursor=con.cursor()
	cursor.execute("SELECT pat_id, name, comments, link FROM patient_table WHERE doc_id=?", (d_id,))
	rows=cursor.fetchall()
	return rows
	# print(rows)
	con.commit()

	
def doctor_select(con):
	'''

	pprint all rows of doctor table

	'''
	cursor=con.cursor()
	cursor.execute("SELECT * FROM doctor_table")
	rows=cursor.fetchall()
	for row in rows:
		print(row)
	con.commit()


def patient_select(con):
	'''

	pprint all rows of patient table

	'''
	cursor=con.cursor()
	cursor.execute("SELECT * FROM patient_table")
	rows=cursor.fetchall()
	for row in rows:
		print(row)
	con.commit()

def drop_tables(con):
	cursor=con.cursor()
	cursor.execute("DROP TABLE patient_table")
	cursor.execute("DROP TABLE doctor_table")
	con.commit()


if __name__=='__main__':
	'''Mandatory functions to run'''
	# con = create_sql_connection()
	# check(con)
	# create_sql_table(con)

	'''Inserting into doctor table'''
	# for i in range(4):
	# 	doctor_values_to_insert=doctor_register()
	# 	doctor_insert(con, doctor_values_to_insert)

	'''Inserting into patient table'''
	# (pat_id, doc_id, name, comments, link)
	# for i in range(1,5):
	# 	values=(100+i, i,"patient"+str(i),"None", "test")
	# 	patient_insert(con, values)
	
	''' Print doctor table'''
	# doctor_select(con)
		
	''' Print patient table'''
	# patient_select(con)

	'''drop tables'''
	# drop_tables(con)