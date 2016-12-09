#!/usr/bin/env python

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#	 author: fmount <francesco.pantano@linux.com>


from fabric.api import env
from fabric.operations import run, put, local
from fabric.context_managers import lcd, cd


env.hosts = ['X.Y.Z.K']
env.user = 'root'
env.key_filename = '~/.ssh/opstack'
SOURCE = "~/git/openstack-aging"
TARGET = "/root/aging"


def copy():
	with lcd(SOURCE):
		# make sure the directory is there!
		local('tar cvf aging.tar --exclude .git --exclude "*.log" \
				--exclude "*.tar*" ./*')
		run('mkdir -p aging')
		put('aging.tar', TARGET)

def launch():
	with cd(TARGET):
		run('tar xvf aging.tar')
		run('source keystonerc_fpantano')
		run('chmod +x aging.py')
		run('./aging.py')

def uptime():
	run('uptime -p')
