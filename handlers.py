#!/usr/bin/env python


import logging
import sys
import re

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# define Python user-defined exceptions
class Error(Exception):
	
	"""
	Base class for other exceptions
	"""

class ConflictException(Error):
	"""Raised when glance return a 409 Error"""
	pass

class ForbiddenException(Error):
	
	"""
	Raised when glance return a 403 Error
	"""
	pass

class ImageDoesNotExistException(Error):
	pass
