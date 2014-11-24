#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
while True:
	body = raw_input("Message: ")
	channel.basic_publish(exchange='',
	                      routing_key='hello',
	                      body=body)
	print " [x] Sent ", body
connection.close()
