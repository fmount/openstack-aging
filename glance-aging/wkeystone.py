#!/bin/python2.7

#	 Licensed under the Apache License, Version 2.0 (the "License");
#	 you may not use this file except in compliance with the License.
#	 You may obtain a copy of the License at
#
#		 http://www.apache.org/licenses/LICENSE-2.0
#
#	 Unless required by applicable law or agreed to in writing, software
#	 distributed under the License is distributed on an "AS IS" BASIS,
#	 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#	 See the License for the specific language governing permissions and
#	 limitations under the License.
#
#	 author: fmount <francesco.pantano@linux.com>


from keystoneauth1.identity import v2
from keystoneauth1 import session
from keystoneclient.v2_0 import client
from prettytable import PrettyTable
from user import User

class Wkeystone():

	# Just to make sure there is only one client
	__instance = None

	def __init__(self, u, debug):
		
		if Wkeystone.__instance:
			raise Exception("Just one client per session allowed!")
		
		Wkeystone.__instance = self
		
		self.user = u
		self.debug = debug

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
