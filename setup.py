from distutils.core import setup

setup(
	name='OpenstackAging',
	version='0.1.0',
	author='Francesco Pantano',
	author_email='francesco.pantano@linux.com',
	packages=['glance-aging', 'glance-aging.test'],
	url='http://pypi.python.org/pypi/OpenstackAging/',
	license='APACHE',
	description='Useful openstack image management stuff.',
	long_description=open('README').read(),
	install_requires=[
		"prettytable",
		"pprint",
	],
)
