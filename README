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

##API

	#!/usr/bin/env python
	
	import aging
    
    params = read_keystonerc('/path/to/tenant/file')
    clients = init(params)
    image = [id1,id2, id3]

    for image in set(image):
        aging_image(image, clients)

##FILES

The first file used by this plugin is the **keystonerc** that looks like:

    export OS_USERNAME=admin 
    export OS_TENANT_NAME=admin   
    export OS_PASSWORD=admin
    export OS_AUTH_URL=http://X.Y.Z.K:5000/v2.0/

You can also read these values from the ENV invoking the appropriate API, but remember to source
your keystonerc before:

	params = read_env()


##EXAMPLE
       ./aging.py   -f   keystonerc_admin   -i   [IMAGE_ID_1,  IMAGE_ID_2  .., IMAGE_ID_N] -v



##SEE ALSO
+ python requirements


