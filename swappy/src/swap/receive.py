#!/usr/bin/env python
import pika
import random

queue_name = 'SC'

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()
channel.queue_declare(queue=queue_name)

QUESTION = 1
ANSWER = 2

def callback(ch, method, properties, body):

	if len(body) > 3:

		if ';' in body:

			parse = body.split(';')
			
			head = parse[0]
			args = parse[1]

			kind, number = None, '0'

			if head[0] == 'Q':
				kind = QUESTION
				number = head[1]

			elif head[0] == 'R':
				kind = ANSWER
				number = head[1]

			print process_query(kind, number, args)

def process_query(kind, number, args):
	number = int(number)

	if kind == QUESTION:
		if number == 1:

			args = [_ for _ in args.split(':')]

			email = args[0]
			id_portfolio = args[1]
			values = args[2]

			return process_Q1(email, id_portfolio, values)

		elif number == 2:
			return 'QUESTION 2'
		elif number == 3:
			return 'QUESTION 3'
		elif number == 4:
			return 'QUESTION 4'

	elif kind == ANSWER:
		if number == 1:
			return 'ANSWER 1'
		elif number == 2:
			return 'ANSWER 2'
		elif number == 3:
			return 'ANSWER 3'
		elif number == 4:
			return 'ANSWER 4'

def process_Q1(email, id_portfolio, args):
	ans = {'user_login' : None, 'risk' : None, 'pk_id' : None, 'values' : []}

	ans['user_login'] = email
	ans['risk'] = random.choice(['M', 'H', 'L'])
	ans['pk_id'] = id_portfolio

	values = [_.split(',')[1] for _ in args.split('|')]

	for value in values:
		ans['values'].append(value)
		
	return ans


while True:
	channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()

