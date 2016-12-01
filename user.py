#!/usr/bin/env python

from prettytable import PrettyTable
from collections import defaultdict
import re
import os


class User():


	def __init__(self, params):
		
		for key in params.keys():
			if params[key] == "None":
				raise Exception("[ERROR] Error Loading Parameters: check your keystonerc")
				return -1
	
		self.name = params.get('OS_USERNAME', 'None')
		self.password = params.get('OS_PASSWORD', 'None')
		self.tenant_name = params.get('OS_TENANT_NAME', 'None')
		self.endpoint = params.get('OS_AUTH_URL', 'None')
		self.api_version = "v2.0"


	def __str__(self):
		
		x = PrettyTable()
		x = PrettyTable(["Name", "Password", "Tenant", "Endpoint", "API"])
		x.add_row([self.name, ''.join(['*' for _ in self.password]),\
			self.tenant_name, self.endpoint, self.api_version])

		return str(x)


def read_env():
	
	if(os.getenv('OS_USERNAME', 'None') is None):
		return None
	if(os.getenv('OS_PASSWORD', 'None') is None):
		return None
	if(os.getenv('OS_TENANT_NAME', 'None') is None):
		return None
	if(os.getenv('OS_AUTH_URL', 'None') is None):
		return None

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



def test():
	
	d = read_keystonerc("~/keystonerc")
	print(User(d))
	
	d = read_env()
	print(User(d))

# MAIN TEST FOR THE CLASS

if __name__ == '__main__':
	test()
