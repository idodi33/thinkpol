import pika
import sys
import time


RECONNECT_TRIES = 10


def create_server_publisher(host, port):
	"""
	Creates a publishing function a server can use
	to upload snapshots to be parsed by functions in
	the message queue.

	:param host: the host of the message queue connection
	:type host: str
	:param port: the port of the message queue connection
	:type port: str
	:returns: the publishing function
	:rtype: callable
	"""
	'''connection = pika.BlockingConnection(
		pika.ConnectionParameters(host=host, port=int(port)))
	channel = connection.channel()
	channel.exchange_declare(
		exchange='server_exchange', 
		exchange_type='fanout'
		)'''
	def server_publish(snapshot):
		'''
		Receives a snapshot in json form, 
		and publishes it to all parsers in the message queue.
		'''
		connection = pika.BlockingConnection(
		pika.ConnectionParameters(host=host, port=int(port)))
		channel = connection.channel()
		channel.exchange_declare(
			exchange='server_exchange', 
			exchange_type='fanout'
		)
		print(f"host is {host}, port is {port}")
		channel.basic_publish(
			exchange='server_exchange', 
			routing_key='', 
			body=snapshot,
			properties=pika.BasicProperties(
                delivery_mode = 2, # make message persistent
            )
			)
		print("Server published a snapshot.")
		#connection.close()
	return server_publish


def create_parser_consumer(host, port):
	"""
	Creates a function that consumes data from the server's
	message queue using a given parser, and sends that parsed
	data to another message queue where it's received by a saver.

	:param host: the host of the message queue connection
	:type host: str
	:param port: the port of the message queue connection
	:type port: str
	:returns: the consuming function
	:rtype: callable
	"""
	'''connection = pika.BlockingConnection(
	    pika.ConnectionParameters(host=host, port=int(port)))
	channel = connection.channel()
	channel.exchange_declare(
		exchange='server_exchange', 
		exchange_type='fanout'
		)
	result = channel.queue_declare(queue='', durable=True)
	queue_name = result.method.queue
	channel.queue_bind(
		exchange='server_exchange', 
		queue=queue_name
		)'''
	def parser_consume(parser):
		'''
		Consumes a snapshot published by the server from the message queue,
		using the given parser.
		'''
		connection = pika.BlockingConnection(
	    	pika.ConnectionParameters(host=host, port=int(port)))
		channel = connection.channel()
		channel.exchange_declare(
			exchange='server_exchange', 
			exchange_type='fanout'
		)
		queue_name = parser.field + "_parse_queue"
		result = channel.queue_declare(queue=queue_name, durable=True)
		#queue_name = result.method.queue
		channel.queue_bind(
			exchange='server_exchange', 
			queue=queue_name
		)
		print("Parser started consuming a snapshot.")
		callback_parser = make_callback_parser(parser, host, port)
		print("Parser about to consume")
		channel.basic_consume(
		    queue=queue_name, 
		    on_message_callback=callback_parser
		    #auto_ack=True
		    )
		channel.basic_qos(prefetch_count=100);
		channel.start_consuming()
	return parser_consume


def make_callback_parser(parser, host, port):
	'''
	Gets a parser and an address and creates a callback function
	that receives messages from the message queue, parses them
	and publishes them to the saver.
	'''
	'''connection = pika.BlockingConnection(
		pika.ConnectionParameters(host=host, port=int(port)))
	channel = connection.channel()'''
	def callback_parser(ch, method, properties, body):
		connection = pika.BlockingConnection(
			pika.ConnectionParameters(host=host, port=int(port)))
		channel = connection.channel()
		queue_name = parser.field + "_save_queue"
		channel.queue_declare(
			queue=queue_name, durable=True)	# queue is named after the parser
		message = parser(body)
		print(f"publishing this in queue {queue_name}")
		print(message)
		channel.basic_publish(
			exchange='', 
			routing_key=queue_name, 
			body=message,
			properties=pika.BasicProperties(
                delivery_mode = 2, # make message persistent
            )
			)
		ch.basic_ack(delivery_tag=method.delivery_tag)
		#connection.close()
	return callback_parser


def create_saver_consumer(host, port):
	"""
	Creates a consuming function a saver can use
	to receive parsed snapshots from parsers' message queues.
	
	:param host: the host of the message queue connection
	:type host: str
	:param port: the port of the message queue connection
	:type port: str
	:returns: the consuming function
	:rtype: callable
	"""
	print("Started creating saver consumer")
	'''connection = pika.BlockingConnection(
		pika.ConnectionParameters(host=host, port=port))
	channel = connection.channel()'''
	def saver_consume(fields, saver):
		'''
		Consumes data as published by a parser, 
		using the given saver and fields.
		'''
		connection = pika.BlockingConnection(
		pika.ConnectionParameters(host=host, port=port))
		channel = connection.channel()
		for field in fields:
			queue_name = field + "_save_queue"
			channel.queue_declare(queue=queue_name, durable=True)
			callback_saver = make_callback_saver(field, saver)
			channel.basic_consume(
				queue=queue_name, 
				on_message_callback=callback_saver
				#auto_ack=True
				)
			print(f"Started consuming from queue {field}")
		channel.start_consuming()
	return saver_consume


def make_callback_saver(field, saver):
	'''
	Gets a saver and a field and returns a callback function that 
	receives messages from the message queue and saves them
	to the database.
	'''
	print(f"making callback saver with saver {saver}")
	def callback_saver(ch, method, properties, body):
		try:
			print(f"make_callback_saver: body to be saved is {body}")
			return saver.save(field, body)
		finally:
			ch.basic_ack(delivery_tag=method.delivery_tag)
	return callback_saver


