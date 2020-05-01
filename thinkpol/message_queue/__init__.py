"""
A driver containing functions the various parts of the project that need 
a message queue can use, using rabbitmq.
"""
from message_queue.rabbitmq_driver import create_server_publisher
from message_queue.rabbitmq_driver import create_parser_consumer
from message_queue.rabbitmq_driver import create_saver_consumer