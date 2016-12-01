#!/usr/bin/env python

from keystoneauth1.identity import v2
from keystoneauth1 import session
from keystoneauth1 import loading
from glanceclient import Client
from prettytable import PrettyTable
from handlers import Error, ConflictException, ForbiddenException
import json
import logging
import sys
import re


logging.basicConfig(stream=sys.stderr, level=logging.INFO)

class Wglance():

	# Just to make sure there is only one client
	__instance = None

	def __init__(self, u, mode):
		if Wglance.__instance:
			raise Exception("Just one client per session allowed!")
		Wglance.__instance = self
		self.user = u
		if(mode == "password"):
			loader = loading.get_plugin_loader('password')
			auth = loader.load_from_options(auth_url=u.endpoint, username=u.name, \
					password=u.password, tenant_name=u.tenant_name)
		else:
			auth = v2.Password(username=u.name, password=u.password, \
					tenant_name=u.tenant_name, auth_url=u.endpoint)
			
		self.s = session.Session(auth=auth)
		self.glance = Client('2', session=self.s)


	def __str__(self):
		print(self.glance)

	def saysomething(self):
		print "I exist"
	
	def exists(self, image_id):
		try:
			self.glance.images.get(image_id)
			return True
		except Exception, e:
			if(re.search('^404*', str(e))):
				logging.error("[404] IMAGE %s NOT FOUND" % image_id)
				return False
			return False


	def image_show(self, image_id):
		
		table = PrettyTable(['Property', 'Value'])
		
		for k, v in json.loads(json.dumps(self.glance.images.get(image_id))).items():
			table.add_row([k, v])
		
		print(table)

	def toggle_visibility(self, image_id, visibility):
		
		if visibility is "private":
			self.glance.images.update(image_id, visibility='private')
		
		elif visibility is "public":
			self.glance.images.update(image_id, visibility='public')
		
		logging.info("Visibility for image %s is now %s" % (image_id, visibility))
	
	# Add a share for the image provided;
	def add_share(self, image_id, tenant_id):
		'''
		>> image_id: the image provided
		>> tenant_id: an array of id who share the image
		'''
		try:
			logging.info("Adding member %s for image %s " % (tenant_id, image_id))
			self.glance.image_members.create(image_id, tenant_id)
		except Exception as e:
			if(re.search('^409*', str(e))):
				logging.error("[409] THIS MEMBERSHIP WAS ALREADY DEFINED")
			elif(re.search('^403*', str(self.error))):
				logging.error("[403] FORBIDDEN")

	# TODO: Delete the image
	def delete_image(self, image_id):
		pass
	
	def remove_share(self, image_id, tenant_id):
		'''
		>> image_id: the image provided
		>> tenant_id: an array of id who share the image
		'''
		try:
			logging.info("Remove member %s for image %s " % (tenant_id, image_id))
			m = self.glance.image_members.delete(image_id, tenant_id)
			if(re.search('^40{1}', m)):
				raise Exception("Something about Permissions went wrong: ch[mod|own] something")
		except:
			raise Exception("No idea what could go wrong..")

	# It cannot work for authentication reasons...hope for new better API
	def update_membership_status(self, image_id, tenant_id):
		self.glance.image_members.update(image_id, tenant_id)

	def image_list(self):
		table = PrettyTable(['ID', 'VISIBILITY', 'DEPRECATED'])
		for image in self.glance.images.list():
			img = json.loads(json.dumps(image))
			table.add_row([img.get('id'), img.get('visibility'), img.get('deprecated',\
				'no_deprecated')])
		print(table)
	
	
	def show_member_list(self, image_id):
		'''
		Show the member list for the given image
		'''
		table = PrettyTable(['Image ID', 'Member ID', 'Status [CAN SHARE]'])
		for member in self.glance.image_members.list(image_id):
			mbm = json.loads(json.dumps(member))
			table.add_row([mbm.get('image_id'), mbm.get('member_id'), mbm.get('status')])
		print(table)


	def member_list(self, image_id):
		'''
		Return a list containing all members for the given image
		'''
		member_list = []
		# table = PrettyTable(['Image ID', 'Member ID', 'Status [CAN SHARE]'])
		for member in self.glance.image_members.list(image_id):
			mbm = json.loads(json.dumps(member))
			# table.add_row([mbm.get('image_id'), mbm.get('member_id'), mbm.get('status')])
			member_list.append(mbm.get('member_id'))
		# print(table)
		return member_list


	def get_all_images(self):
		img_list = []
		for image in self.glance.images.list():
			img = json.loads(json.dumps(image))
			img_list.append(img.get('id'))
		return img_list
	
	def is_visible(self, image_id):
		for k, v in json.loads(json.dumps(self.glance.images.get(image_id))).items():
			if(k == "visibility" and v is "public"):
				return True
		return False
				
	
	def is_deprecated(self, image_id):
		for k, v in json.loads(json.dumps(self.glance.images.get(image_id))).items():
			if(k == "deprecated"):
				logging.info("[DEBUG] The image %s IS deprecated " % image_id)
				return v
		logging.info("[DEBUG] The image %s is NOT deprecated " % image_id)
		return False
		

	def toggle_deprecated(self, image_id, bool_value):
		if self.is_visible(image_id) is False:
			self.glance.images.update(image_id, deprecated=str(bool_value))
			return True
		logging.WARN("Cannot Deprecate the image %s : Make it private first!!" % image_id)
		return False
	
	

	def is_shared(self, image_id, tenant_id):
		if len(self.member_list(image_id)) > 0:
			return True
		else:
			return False
