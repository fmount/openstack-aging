OPENSTACK IMAGE AGING PLUGIN
=======

The Glance plugin implements an aging algorithm for images stored in the Openstack Infrastructure.
This plugin also allow to interactively deprecate openstack images tenant by tenant and manage shared member
according to your own policy.
It also will help sysadmin to process their glance images inside the openstack infrastructure according to an aging
algorithm  that allows them to keep the system up to date and more clean. 
You can also instruct the  script to be executed periodically.

##Usage

aging.py --image [image\_id, image\_id, ..] -z image\_file -f  tenant\_file --debug

Options:
	 -h, --help   		show this help message and exit
     -z IMAGE_FILE     	a file that contains an image list
     -f TENANT_FILE    	tenant file to authenticate on keystone
     -i IMAGE     		specify the image id to analyze
     -d  DEPRECATE 		deprecate  the images read from file or  given as argument
     --debug=DEBUG		activate DEBUG MODE to print all  critical  statement during the algorithm execution

You can import the library inside your py package and use the exposed methods in this way:

TODO:::::::::::
	#!/usr/bin/env python
	
	from towelstuff import location
	from towelstuff import utils

	if utils.has_towel():
		print "Your towel is located:", location.where_is_my_towel()
:::::::::::::::


##FILES

+ keystonerc


##EXAMPLE
       ./aging.py   -f   keystonerc_admin   -i   [IMAGE_ID_1,  IMAGE_ID_2  .., IMAGE_ID_N] -v



##SEE ALSO
+ python requirements


