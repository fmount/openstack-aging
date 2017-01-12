#!/usr/bin/env python

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


from novaclient import client
from prettytable import PrettyTable
from collections import defaultdict
from keystoneauth1.identity import v2
from keystoneauth1 import session
import simplejson as json


class Wnova():

	# Just to make sure there is only one client
	__instance = None


	def __init__(self, u, debug):

		if Wnova.__instance:
			raise Exception("Just one client per session allowed!")
		
		Wnova.__instance = self
		auth = v2.Password(username=u.name, password=u.password, \
				tenant_name=u.tenant_name, auth_url=u.endpoint)

		self.s = session.Session(auth=auth)
		self.nova = client.Client('2', session=self.s)

		self.debug = debug

	def __str__(self):
		print(self.nova)


	def print_server_list(self):
		
		'''
		It creates a table representing the list of nodes (vms deployed) for
		all tenants.
		'''
		
		x = PrettyTable(['Server ID', 'Server Name', 'Tenant ID', 'Image ID'])
		for server in self.nova.servers.list(search_opts={'all_tenants': 1}):
				simg = json.loads(json.dumps(server.image))

				x.add_row([server.id, server.name, server.tenant_id, \
					(lambda simg: "noid" if str(simg) == "" else simg['id'])(simg)])
		print(x)


	def build_compute(self):
		
		'''
		It creates a dict in which the serverID is the key (it is the nova-id), the other
		elements (server_name,tenant_id,image_id) are the array value.
		
		{server_id: [server_name, tenant_id, image_id]}
		
		'''
		compute_set = defaultdict()
		for server in self.nova.servers.list(search_opts={'all_tenants': 1}):
			simg = json.loads(json.dumps(server.image))
			
			compute_set[server.id] = ([server.name, server.tenant_id, \
					(lambda simg: "noid" if str(simg) == "" else simg['id'])(simg)])

		return compute_set
