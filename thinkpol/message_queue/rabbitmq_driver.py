import pika
import sys

def create_server_publisher(host, port):
	def server_publish(snapshot):
		'''
		Receives a snapshot in json form, and publishes it to all parsers in the message queue.
		'''
		print(f"host is {host}, port is {port}")
		connection = pika.BlockingConnection(
			pika.ConnectionParameters(host=host, port=int(port)))
		channel = connection.channel()
		channel.exchange_declare(exchange='server_exchange', exchange_type='fanout')
		channel.basic_publish(exchange='server_exchange', routing_key='', body=snapshot)
		print("Server published a snapshot.")
		connection.close()
	return server_publish

def create_parser_consumer(host, port):
	def parser_consume(parser):
		'''
		Consumes a snapshot published by the server from the message queue,
		using the given parser.
		'''
		print("Parser started consuming a snapshot.")
		connection = pika.BlockingConnection(
		    pika.ConnectionParameters(host=host, port=int(port)))
		channel = connection.channel()
		channel.exchange_declare(exchange='server_exchange', exchange_type='fanout')
		result = channel.queue_declare(queue='', durable=True)
		queue_name = result.method.queue
		channel.queue_bind(exchange='server_exchange', queue=queue_name)
		callback_parser = make_callback_function(parser, host, port)
		print("Parser about to consume")
		channel.basic_consume(
		    queue=queue_name, on_message_callback=callback_parser, auto_ack=True)
		channel.start_consuming()
	return parser_consume

"""
def make_callback_from_parser(parser):
	'''
	Gets a parser and returns a callback function, which functions
	exactly like the parser except it gets 4 arguments instead of 1
	and only uses the last one.
	'''
	def callback_parser(ch, method, properties, body):
		print(parser(body))
		return parser(body)
	return callback_parser
"""

def make_callback_function(parser, host, port):
	'''
	Gets a parser and an address and creates a callback function
	that receives messages from the message queue, parses them
	and publishes them to the saver.
	'''
	def callback_parser(ch, method, properties, body):
		connection = pika.BlockingConnection()
		connection = pika.BlockingConnection(
			pika.ConnectionParameters(host=host, port=int(port)))
		channel = connection.channel()
		channel.queue_declare(queue=parser.field, durable=True)	# queue is named after the parser
		message = parser(body)
		print(message)
		channel.basic_publish(exchange='', routing_key=parser.field, body=message)
		connection.close()
	return callback_parser
