"""
Receives data about users and snapshots of their cognition
from clients and sends it to parsing functions that parse 
that data and use it in various ways.
"""
from .server import run_server