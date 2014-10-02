######################## DJANGO IMPORTS ########################
from django.shortcuts import render
from django.db import connection

######################## CUSTOM IMPORTS ########################
import val


################################################################
######################## VIEW FUNCTIONS ########################
################################################################


def search(request):
	pass
	#TODO


################################################################
################## HIGH LEVEL AUX FUNCTIONS ####################
################################################################



################################################################
################### LOW LEVEL AUX FUNCTIONS ####################
################################################################


def get_all_vals():
	ans = []
	cursor = connection.cursor()
	query = "SELECT * FROM val"
	cursor.execute(query)
	values = [itm for itm in cursor.fetchall()]
	for itm in values:
		pk_id = itm[0]
		name = itm[1]
		price = itm[2]
		quantity = itm[3]
		offerant = itm[4]
		to_Add = val.Val(pk_id, name, price, quantity, offerant)
		ans.append(to_Add)
	return ans