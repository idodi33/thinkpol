from ..utils.snapshot import Snapshot
import gzip
import os


def binary_snap_iterator(file_name, offset=0):
	"""
	Recieves a binary file name and reads snapshots from it iteratively.
	offset marks the length of the user info in the file.

	:param file_name: name of the file
	:type file_name: str
	:param offset: place we start reading from in file
	:type offset: int
	"""
	with open(file_name, 'rb') as f:
		f.read(offset)
		file_position = f.tell()
		f.seek(0, os.SEEK_END)
		file_end = f.tell()
		f.seek(file_position, os.SEEK_SET)
		while f.tell() != file_end:
			yield Snapshot.from_stream(f)

def protobuf_snap_iterator(file_name, offset=0):
	"""
	Recieves a gzipped protobuf file name and reads snapshots from it iteratively.
	offset marks the length of the user info in the file.

	:param file_name: name of the file
	:type file_name: str
	:param offset: place we start reading from in file
	:type offset: int
	"""
	with gzip.open(file_name, 'rb') as f:
		f.read(offset)
		file_position = f.tell()
		f.seek(0, os.SEEK_END)
		file_end = f.tell()
		f.seek(file_position, os.SEEK_SET)
		while f.tell != file_end:
			yield Snapshot.from_proto_stream(f)



snap_readers = {
	'binary': binary_snap_iterator, 
	'protobuf': protobuf_snap_iterator
	}