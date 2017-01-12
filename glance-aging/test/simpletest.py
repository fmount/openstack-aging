#!/usb/bin/env python

import unittest
from user import User

__author__ = 'fmount'
__project__ = 'glance-aging'

# TODO: Write some tests

class TestUser(unittest.TestCase):
	
	def test_error_user(self):
		params = {}
		u = User(params)
		
	def create_user(self):
		self.fail()


class SimplisticTest(unittest.TestCase):

    def test(self):
        self.failUnless(True)

if __name__ == '__main__':
    unittest.main()
