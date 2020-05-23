import pika
import sys


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
	connection = pika.BlockingConnection(
		pika.ConnectionParameters(host=host, port=int(port)))
	channel = connection.channel()
	channel.exchange_declare(
		exchange='server_exchange', 
		exchange_type='fanout'
		)
	def server_publish(snapshot):
		'''
		Receives a snapshot in json form, 
		and publishes it to all parsers in the message queue.
		'''
		print(f"host is {host}, port is {port}")
		channel.basic_publish(
			exchange='server_exchange', 
			routing_key='', 
			body=snapshot
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
	connection = pika.BlockingConnection(
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
		)
	def parser_consume(parser):
		'''
		Consumes a snapshot published by the server from the message queue,
		using the given parser.
		'''
		print("Parser started consuming a snapshot.")
		callback_parser = make_callback_parser(parser, host, port)
		print("Parser about to consume")
		channel.basic_consume(
		    queue=queue_name, 
		    on_message_callback=callback_parser, 
		    auto_ack=True
		    )
		channel.start_consuming()
	return parser_consume


def make_callback_parser(parser, host, port):
	'''
	Gets a parser and an address and creates a callback function
	that receives messages from the message queue, parses them
	and publishes them to the saver.
	'''
	connection = pika.BlockingConnection(
		pika.ConnectionParameters(host=host, port=int(port)))
	channel = connection.channel()
	def callback_parser(ch, method, properties, body):
		channel.queue_declare(
			queue=parser.field, durable=True)	# queue is named after the parser
		message = parser(body)
		print(f"publishing this in queue {parser.field}")
		print(message)
		channel.basic_publish(
			exchange='', 
			routing_key=parser.field, 
			body=message
			)
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
	connection = pika.BlockingConnection(
		pika.ConnectionParameters(host=host, port=port))
	channel = connection.channel()
	def saver_consume(fields, saver):
		'''
		Consumes data as published by a parser, 
		using the given saver and fields.
		'''
		for field in fields:
			channel.queue_declare(queue=field, durable=True)
			callback_saver = make_callback_saver(field, saver)
			channel.basic_consume(
				queue=field, 
				on_message_callback=callback_saver
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
		print(f"make_callback_saver: body to be saved is {body}")
		return saver.save(field, body)
	return callback_saver


