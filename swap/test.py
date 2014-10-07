<<<<<<< HEAD
from django.db import connection

def test_solicitudes_pk():
    cursor = connection.cursor()
    ans1 = "INSERT INTO solicitude VALUES (%s, %s, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
    p1 = [5476, '1', 2, 10, '1', 'wer', '0', '0']
    ans2 = "INSERT INTO solicitude VALUES (%s, %s, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
    p2 = p1
    try:
        cursor.execute(ans1, p1)
        print 'Insercion 1 exitosa'
    except Exception, e:
        print 'PK repetida'
    finally:
        connection.close()
    try:
        cursor.execute(ans2, p2)
        print 'Insercion 2 exitosa'
    except Exception, e:
        print 'PK repetida ' + str(5476)
    finally:
        connection.close()

def test_solicitudes_fk():
    cursor = connection.cursor()
    ans1 = "INSERT INTO solicitude VALUES (%s, %s, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
    p1 = [5276, '1', 2, 10, '1', 'wer', '0', '0']
    ans2 = "INSERT INTO solicitude VALUES (%s, %s, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
    p2 = p1
    p2[0] = 5270
    p2[5] = 'lalalalala'
    ans3 = "SELECT * FROM solicitude"
    ans4 = "DELETE FROM active WHERE login='wer'"
    ans5 = "SELECT * FROM solicitude"
    try:
        cursor.execute(ans1, p1)
        print 'Insercion 1 exitosa'
    except Exception, e:
        print 'FK no existe'
    finally:
        connection.close()
    try:
        cursor.execute(ans2, p2)
        print 'Insercion 2 exitosa'
    except Exception, e:
        print 'FK no existe ' + 'lalalalala'
    finally:
        connection.close()
    try:
        cursor.execute(ans3)
        all = cursor.fetchall()
        for a in all: print a
    except Exception, e:
        print 'error'
    finally:
        connection.close()
    try:
        cursor.execute(ans4)
        print 'Tupla removida'
    except Exception, e:
        print 'error'
    finally:
        connection.close()
    try:
        cursor.execute(ans3)
        all = cursor.fetchall()
        for a in all: print a
    except Exception, e:
        print 'error'
    finally:
        connection.close()

def test_solicitudes_constraints():
    ans1 = "INSERT INTO solicitude VALUES (%s, %s, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
    p1 = [8888, 2, 10, '1', 'wer', '0', '0']
    ans2 = "INSERT INTO solicitude VALUES (%s, NULL, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
    p2 = p1
    ans3 = "DELETE FROM solicitude WHERE (pk_id = 8888)"
    try:
        cursor.execute(ans1, p1)
        print 'INSERCION 1 exitosa'
    except Exception, e:
        print 'CONSTRAINT VIOLATED'
    finally:
        connection.close()
    try:
        cursor.execute(ans2, p2)
        print 'Insercion 2 exitosa'
    except Exception, e:
        print 'CONSTRAINT VIOLATED'
    finally:
        connection.close()
    try:
        cursor.execute(ans3)
        print 'Tupla removida'
    except Exception, e:
        print 'error'
    finally:
        connection.close()

test_solicitudes_pk()
test_solicitudes_fk()
test_solicitudes_constraints()
=======
from django.db import connection

def test_solicitudes_pk():
    cursor = connection.cursor()
    ans1 = "INSERT INTO solicitude VALUES (%s, %s, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
    p1 = [5476, '1', 2, 10, '1', 'wer', '0', '0']
    ans2 = "INSERT INTO solicitude VALUES (%s, %s, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
    p2 = p1
    try:
        cursor.execute(ans1, p1)
        print 'Insercion 1 exitosa'
    except Exception, e:
        print 'PK repetida'
    finally:
        connection.close()
    try:
        cursor.execute(ans2, p2)
        print 'Insercion 2 exitosa'
    except Exception, e:
        print 'PK repetida ' + str(5476)
    finally:
        connection.close()

def test_solicitudes_fk():
    cursor = connection.cursor()
    ans1 = "INSERT INTO solicitude VALUES (%s, %s, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
    p1 = [5276, '1', 2, 10, '1', 'wer', '0', '0']
    ans2 = "INSERT INTO solicitude VALUES (%s, %s, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
    p2 = p1
    p2[0] = 5270
    p2[5] = 'lalalalala'
    ans3 = "SELECT * FROM solicitude"
    ans4 = "DELETE FROM active WHERE login='wer'"
    ans5 = "SELECT * FROM solicitude"
    try:
        cursor.execute(ans1, p1)
        print 'Insercion 1 exitosa'
    except Exception, e:
        print 'FK no existe'
    finally:
        connection.close()
    try:
        cursor.execute(ans2, p2)
        print 'Insercion 2 exitosa'
    except Exception, e:
        print 'FK no existe ' + 'lalalalala'
    finally:
        connection.close()
    try:
        cursor.execute(ans3)
        all = cursor.fetchall()
        for a in all: print a
    except Exception, e:
        print 'error'
    finally:
        connection.close()
    try:
        cursor.execute(ans4)
        print 'Tupla removida'
    except Exception, e:
        print 'error'
    finally:
        connection.close()
    try:
        cursor.execute(ans3)
        all = cursor.fetchall()
        for a in all: print a
    except Exception, e:
        print 'error'
    finally:
        connection.close()

def test_solicitudes_constraints():
    ans1 = "INSERT INTO solicitude VALUES (%s, %s, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
    p1 = [8888, 2, 10, '1', 'wer', '0', '0']
    ans2 = "INSERT INTO solicitude VALUES (%s, NULL, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
    p2 = p1
    ans3 = "DELETE FROM solicitude WHERE (pk_id = 8888)"
    try:
        cursor.execute(ans1, p1)
        print 'INSERCION 1 exitosa'
    except Exception, e:
        print 'CONSTRAINT VIOLATED'
    finally:
        connection.close()
    try:
        cursor.execute(ans2, p2)
        print 'Insercion 2 exitosa'
    except Exception, e:
        print 'CONSTRAINT VIOLATED'
    finally:
        connection.close()
    try:
        cursor.execute(ans3)
        print 'Tupla removida'
    except Exception, e:
        print 'error'
    finally:
        connection.close()

test_solicitudes_pk()
test_solicitudes_fk()
test_solicitudes_constraints()
>>>>>>> f9d74e37f7eb3af2a531388a362d848560f9a3a9
