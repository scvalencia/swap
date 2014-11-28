#!/usr/bin/env python
import pika

queue_name = 'SC'

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()
channel.queue_declare(queue=queue_name)

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

while True:
	channel.basic_consume(callback1, queue=queue_name, no_ack=True)

channel.start_consuming()