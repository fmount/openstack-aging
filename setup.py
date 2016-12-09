from distutils.core import setup

setup(
	name='OpenstackAging',
	version='0.1.0',
	author='Francesco Pantano',
    author_email='francesco.pantano@linux.com',
    packages=['glance-aging', 'glance-aging.test'],
    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/OpenstackAging/',
    license='LICENSE',
    description='Useful openstack image management stuff.',
    long_description=open('README.md').read(),
    install_requires=[
        "Django >= 1.1.1",
        "caldav == 0.1.4",
    ],
)
