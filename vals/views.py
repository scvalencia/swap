from django.shortcuts import render
from django.db import connection
import val

def search(request):
	pass
	#TODO

def get_all_vals(request):
	# TODO scvalencia
	# Necesito que retorne una lista de objetos de clase val
	# con todos los valores de la tabla val.
	ans = []
	cursor = connection.cursor()
	query = "SELECT * FROM val"
	cursor.execute(query)
	values = [itm for itm in cursor.fetchall()]
	for itm in values:
		pk = itm[0]
		name = itm[1]
		price = itm[2]
		quantity = itm[3]
		offerant = itm[4]
		to_Add = val.Val(pk_id, name, price, quantity, offerant)
		ans.append(to_Add)
	return ans



