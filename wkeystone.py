#!/bin/python2.7

from keystoneauth1.identity import v2
from keystoneauth1 import session
from keystoneclient.v2_0 import client
from prettytable import PrettyTable
from user import User

class Wkeystone():

	# Just to make sure there is only one client
	__instance = None

	def __init__(self, u):
		
		if Wkeystone.__instance:
			raise Exception("Just one client per session allowed!")
		
		Wkeystone.__instance = self
		
		self.user = u
		
		auth = v2.Password(username=u.name, password=u.password, \
				tenant_name=u.tenant_name, auth_url=u.endpoint)

		self.s = session.Session(auth=auth)
		self.keystone = client.Client(session=self.s)


	def __str__(self):
		print(self.keystone)


	def saysomething(self):
		print "I exist"


	def print_tenant_list(self):
		print(self.keystone.tenants.list())
