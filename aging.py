#!/usr/bin/env python

from __future__ import print_function
from prettytable import PrettyTable
from collections import defaultdict
from wnova import Wnova as nclient
from wkeystone import Wkeystone as kclient
from wglance import Wglance as gclient
from handlers import ImageDoesNotExistException
from user import User
import optparse
import re
import os
import pprint
import user
import logging
import sys
import json

SUPPORTED_VERSIONS = [1, 2]

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


def init(*args):
	# mode = args[0]
	dic = args[0]
	return build_openstack_clients(dic)


def build_openstack_clients(params):
	dic = defaultdict()
	dic.__setitem__('kclient', kclient(User(params)))
	dic.__setitem__('nclient', nclient(User(params)))
	dic.__setitem__('gclient', gclient(User(params), "password"))
	# return kclient(User(params)), nclient(User(params)), gclient(User(params))
	return dic


def read_env(parser):
	
	if(os.getenv('OS_USERNAME') is None) or \
		(os.getenv('OS_PASSWORD') is None) or \
		(os.getenv('OS_TENANT_NAME') is None) or \
		(os.getenv('OS_AUTH_URL') is None):
			print(parser.usage)
			exit(-1)

	
	prms = defaultdict()
	prms.__setitem__('OS_USERNAME', os.getenv('OS_USERNAME', 'None'))
	prms.__setitem__('OS_TENANT_NAME', os.getenv('OS_TENANT_NAME', 'None'))
	prms.__setitem__('OS_PASSWORD', os.getenv('OS_PASSWORD', 'None'))
	prms.__setitem__('OS_AUTH_URL', os.getenv('OS_AUTH_URL', 'None'))
	
	return prms


def read_keystonerc(ksrc):
	prms = defaultdict()
	with open(ksrc, 'r') as f:
		for line in f:
			l = re.sub('export ', '', line)
			prms.__setitem__(l.split("=")[0], l.split("=")[1].rstrip())
	
	return prms


def who_use_that_image(nclient, image_id):
	'''
	Return a dict in the form of { "tenant_id" : "image_id" }
	'''
	candidates = nclient.build_compute()
	marked = {}
	for k, v in candidates.items():
		
		using = (lambda image_id, _analyze: True if image_id == _analyze \
				else False)(image_id, candidates.get(k)[2])
		

		logging.info("%s using the %s image? %s" % (k, image_id, using))
		
		if(using):
			marked[candidates.get(k)[1]] = image_id
	
	return marked


def interactive_deprecation(nclient, gclient):
	images = gclient.get_image_list()
	for img in images:
		print("Deprecate %s [y/n]")
		c = input()
		if(str(c) is 'y'):
			mark_as_deprecated(img)


def mark_as_private(gclient, image_id):
	gclient.toggle_visibility(image_id, 'private')


def mark_as_deprecated(image_id):
	gclient.toggle_deprecated(image_id, True)


def mark_as_shared(image_id, **kwargs):
	'''
	First aging algorithm: mark the image as shared means making it private \
	and the sharing it just with tenants having active nodes that make use of \
	the image passed as argument.
	'''

	(gclient, nclient) = (kwargs['gclient'], kwargs['nclient'])

	logging.info("MAKING IMAGE %s PRIVATE" % image_id)
	mark_as_private(gclient, image_id)
	logging.debug(gclient.image_show(image_id))
	
	marked = who_use_that_image(nclient, image_id)
	logging.info("\nTARGET FOR SHARE DETECTED: %s" % marked)
	share_with_tenants(gclient, image_id, marked.keys())


def share_with_tenants(gclient, image_id, tenants):
	'''
	We share the image passed as argument with a list of tenants: this \
	method accept tenants as argument coming from the "who_use_that_image" method.
	'''
	# MAP IS DEAD
	# map(gclient.add_share, image_id, tenants)
	
	for tenant in tenants:
		gclient.add_share(image_id, tenant)

def autoglancing(**kwargs):
	for image_id in kwargs['gclient'].get_all_images():
		logging.info("Processing image %s" % image_id)
		if(kwargs['gclient'].is_deprecated(image_id)):
			mark_as_shared(image_id, **kwargs)


def aging_image(image, **kwargs):
	
	'''
	The aging algorithm is design to work on deprecation defined model.
	For each image it follows these steps:
	1. Deprecate the image adding a "Deprecated=True" property
	2. Make the image private toggling Visibility from Glance Client instance
	3. For each active node that use the image, add a member share
	4. Print the resulting member share
	'''
	
	gclient = kwargs['gclient']
	logging.info("STARTING AGING ALGO FOR IMAGE %s " % image)

	# Verify Image exists
	try:
		if(not gclient.exists(image)):
			raise ImageDoesNotExistException
		else:
			logging.info("IMAGE %s EXISTS " % image)

	except ImageDoesNotExistException:
		logging.error("IMAGE DOESN'T EXIST")
		yield_retry(image)
		return -1

	logging.info("DEPRECATING IMAGE %s " % image)
	gclient.toggle_deprecated(image, True)
	logging.debug(gclient.image_show(image))

	'''
	Marking image as shared works in two steps:
	1. Make it private (toggling visibility)
	2. Compute tenants who works with that image and share it with them
	'''
	mark_as_shared(image, **kwargs)
	gclient.show_member_list(image)


#  Utility #

def listing_images(gclient):
	print(gclient.get_all_images())


def yield_retry(msg):

	try:
		with open("hosts.retry", 'a') as f:
			f.write(msg)
	except Exception, e:
		logging.error(str(e))


def load_images_from_file(fpath):

	images = []

	try:
		with open(fpath, 'r') as f:
			for image in f:
				images.append(image.strip())
			return images
	except IOError, e:
		logging.error(str(e))
		exit(-1)


def cli():

	print("------------------------------")
	print("GLANCE AGING PLUGIN")
	print("------------------------------\n")

	parser = optparse.OptionParser('\nsource keystonerc* \nusage %prog --image [image_id, image_id, ..] -z image_file -f tenant_file')
	parser.add_option('-z', dest='image_file', type='string', help='a file that contains an image list')
	parser.add_option('-f', dest='tenant_file', type='string', help='tenant file to authenticate on keystone')
	parser.add_option('-i', dest='image', type='string', help='specify the image id to analyze')
	parser.add_option('-d', dest='deprecate', type='string', help='deprecate the images read from file or given as argument')
	

	(options, args) = parser.parse_args()
	
	tenant_file = options.tenant_file
	image_file = options.image_file
	image = options.image
	deprecate = options.deprecate

	'''
	First of all check the authentication method: give priority to keystonerc option
	to avoid any relation with the host/guest
	'''
	if tenant_file == None:
		logging.info("Try to read user info from ENV")
		params = read_env(parser)
	else:
		logging.info("Loading from keystonerc")
		params = read_keystonerc(tenant_file)
		
	c = init(params)
	
	if(image is None and image_file is None):
		print("No images provided: continue following deprecation model")
		autoglancing(**c)
		return 0
	if(image_file is not None):
		logging.info("Reading images from the file provided")
		for image in set(load_images_from_file(image_file)):
			aging_image(image, **c)
		return 0

	elif(image is not None):
		for image in set(list(image.split(','))):
			aging_image(image, **c)
		return 0
	
	# TODO: Add deprecation feature and interactive deprecation mode

if __name__ == '__main__':
	cli()
