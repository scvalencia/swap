import cx_Oracle

connection = cx_Oracle.connect('username/password@localhost')
connection.close()
cursor = connection.cursor()
 
cursor.execute('SELECT Firstname,Lastname FROM TB_NAME')
lastname = raw_input('Please type a lastname: ')
 
cursor.execute('''
SELECT Firstname
FROM TB_TABLE
WHERE Lastname = :last''', last=lastname)
 
#Dictionary
#Insert a new name
firstname = raw_input('Please type a firstname: ')
lastname = raw_input('Please type a lastname: ')
 
cursor.execute('''
INSERT INTO TB_NAME
VALUES(:first,:last)''', {'first':firstname,'last':lastname})

row = cursor.fetchone()
#or
rows = cursor.fetchall()

for row in rows:
	print row[0], row[1]
 
#or
 
for firstname, lastname in rows:
	print firstname, lastname

name_list = [('Joe','Blogs'),('Jim','Jones'),('Dan','Smith')]
 
for name in name_list:
	cursor.execute('''
	INSERT INTO TB_NAME(Firstname,Lastname) VALUES(:first,:last)
	''',
	{'first':name[0],'last':name[1]})