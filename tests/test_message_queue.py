import pytest
import pika
import os
import signal
import time
import json
from thinkpol.message_queue import rabbitmq_driver
import tester_utils as tu

def mock_parser(js):
	return js
mock_parser.field = 'mock'


def mock_callback_parser(ch, method, properties, body):
	print("hey it's callback parser")
	assert json.loads(body) == json.loads(tu._JSON)
	# kill child process if we succeeded
	os.kill(os.getpid(), signal.SIGKILL)


class MockSaver:
	def save(self, field, data):
		# check if saver received tu._JSON
		data_dict = json.loads(data)
		del data_dict['color_image']
		del data_dict['depth_image']
		orig_dict = json.loads(tu._JSON)
		del orig_dict['color_image']
		del orig_dict['depth_image']
		assert data_dict == orig_dict
		# kill child process if we succeeded
		os.kill(os.getpid(), signal.SIGKILL)
'''
@pytest.fixture
def mock_make_callback_parser(monkeypatch):
	
	Changes the function 'make callback parser' to return a generic
	callback function rather than an actual parser that would require
	using the parsers module.
	
	def mock_maker(parser, host, port):
		return mock_callback_parser
	monkeypatch.setattr(rabbitmq_driver, 'make_callback_parser', mock_maker)
'''


def test_server_publisher():
	# uses create_server_publisher to publish
	publish = rabbitmq_driver.create_server_publisher(tu._HOST, tu._MQ_PORT)
	# simulates parsers consuming; tests if correct result was published
	connection = pika.BlockingConnection(
	    pika.ConnectionParameters(host=tu._HOST, port=tu._MQ_PORT))
	channel = connection.channel()
	channel.exchange_declare(
		exchange='server_exchange', exchange_type='fanout')
	result = channel.queue_declare(queue='', durable=True)
	queue_name = result.method.queue
	channel.queue_bind(exchange='server_exchange', queue=queue_name)
	channel.basic_consume(
		queue=queue_name, on_message_callback=mock_callback_parser, 
		auto_ack=True)
	# use processing to close queue when done
	p = os.fork()
	if p:	# parent process
		print("parent here")
		child_pid = p
		time.sleep(1)
		publish(tu._JSON)
		os.wait()
	else:	# child process
		print("child here")
		channel.start_consuming() 


def test_parser_consumer():
	# simulates server publishing
	serv_connection = pika.BlockingConnection(
		pika.ConnectionParameters(host=tu._HOST, port=tu._MQ_PORT))
	serv_channel = serv_connection.channel()
	serv_channel.exchange_declare(
		exchange='server_exchange', exchange_type='fanout')
	serv_channel.basic_publish(
		exchange='server_exchange', routing_key='', body=tu._JSON)
	# uses create_parser_consumer
	consume = rabbitmq_driver.create_parser_consumer(tu._HOST, tu._MQ_PORT)
	# tests if correct result was published to queue
	save_connection = pika.BlockingConnection()
	save_connection = pika.BlockingConnection(
		pika.ConnectionParameters(host=tu._HOST, port=tu._MQ_PORT))
	save_channel = save_connection.channel()
	save_channel.queue_declare(
		queue=mock_parser.field, durable=True)
	save_channel.basic_consume(
		queue=mock_parser.field, 
		on_message_callback=mock_callback_parser)
	# use processing to close queue when done
	child = os.fork()
	if child:	# parent process
		print("parent here")
		time.sleep(6)
		os.kill(child, signal.SIGSTOP)
	else:	# child process
		grandchild = os.fork()
		if grandchild:	# child process
			consume(mock_parser)
			time.sleep(3)
			os.wait()
		else:	# grandchild process
			save_channel.start_consuming()


def test_saver_consumer():
	# simulates parser publishing
	connection = pika.BlockingConnection()
	connection = pika.BlockingConnection(
		pika.ConnectionParameters(host=tu._HOST, port=tu._MQ_PORT))
	channel = connection.channel()
	queue_name = "mock2_save_queue"
	channel.queue_declare(
		queue=queue_name, durable=True)	# queue is named after the parser
	# uses create_saver_consumer
	consume = rabbitmq_driver.create_saver_consumer(
		host=tu._HOST, port=tu._MQ_PORT)
	# use processing to close queue when done
	p = os.fork()
	if p:	# parent process
		print("parent here 2")
		time.sleep(1)
		print("publishing")
		#raise Exception(f"test_saver_consumer: tu._JSON['depth_image'] = {json.loads(tu._JSON)['depth_image']}")
		channel.basic_publish(
			exchange='', routing_key=queue_name, body=tu._JSON)
		os.wait()
	else:	# child process
		print("child here 2")
		saver = MockSaver()
		consume(["mock2"], saver)


