#!/usr/bin/env python
import pika

PORT = 5672

local = True
queue_name = 'CF' if not local else 'SC'
connection = None

if not local:

	username = 'valencia'
	password = 'admin123'
	foreign_ip = '157.253.220.130' 

	credentials = pika.PlainCredentials(username, password)
	parameters = pika.ConnectionParameters(foreign_ip, PORT, '/', credentials)
	connection = pika.BlockingConnection(parameters)

else:

	print queue_name
	connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()
channel.queue_declare(queue=queue_name)

def send_message(body):
	channel.basic_publish(exchange='', routing_key=queue_name, body=body)

while True:
	body = raw_input("Message: ")
	send_message(body)
	
connection.close()
