connection = cx_Oracle.connect("uid/pwd@database")
cursor = connection.cursor()
cursor.execute("INSERT INTO User_Tables(login,first_name,last_name,age,date_of_birth) 
                VALUES (:login,:first,:last,:age,to_date(:dob,'YYYY-MM-DD HH24:MI:SS'))",
               {
                'login' : 'some_user_login',
                'first' : 'some_first_name',
                'last' : 'some_last_name',
                'age' : 42,
                'dob' : '1970-01-01 23:52:00',
               }
              )
count = cursor.fetchall()[0][0]
cursor.close()
connection.commit()
connection.close()
