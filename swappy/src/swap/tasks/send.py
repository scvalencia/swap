#!/usr/bin/env python
import pika

PORT = 5672

local = True
queue_name = 'CF' if not local else 'SC'
connection = None

if not local:

	username = 'scvalencia'
	password = 'admin123'
	foreign_ip = '157.253.220.84' 

	credentials = pika.PlainCredentials(username, password)
	parameters = pika.ConnectionParameters(foreign_ip, PORT, '/', credentials)
	connection = pika.BlockingConnection(parameters)

else:

	connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()
channel.queue_declare(queue=queue_name)

def send_message(body):
	channel.basic_publish(exchange='', routing_key=queue_name, body=body)
	
connection.close()