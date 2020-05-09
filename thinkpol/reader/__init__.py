"""
Reads information (about users and their snapshots) from a formatted binary file.
Contains the 'reader' module that has a Reader object, and the 'reader_drivers' 
folder, which contains drivers for handling different file formats.
"""
from .reader import Reader