#!/usr/bin/env python

from fabric.api import env
from fabric.operations import run, put, local
from fabric.context_managers import lcd, cd


env.hosts = ['10.3.40.17']
env.user = 'root'
env.key_filename = '~/.ssh/opstack'
SOURCE = "/home/fmount/git/openstack-aging"
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
