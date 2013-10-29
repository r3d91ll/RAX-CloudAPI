import os
import pyrax

#def make_choice(item_list, prompt):
#	
#	for index, item in enumerate(item_list):
#		print index, item
#	selection = -1
#	while selection < 0 or selection > len(item_list) - 1:
#		selection = int(raw_input(prompt))
#	return item_list[selection]


def main():

	pyrax.set_setting("identity_type", "rackspace")
	creds_file = os.path.expanduser('~/.rackspace_cloud_credentials')
	pyrax.set_credential_file(creds_file)
	available_regions = pyrax.regions

	print "Regions Available:", " ".join(list(available_regions))
	region = ""
	while region not in pyrax.regions:
		region = raw_input("Select region: ")
	cs = pyrax.connect_to_cloudservers(region)
	servers = cs.servers.list()
	srv_dict = {}

	print "Select a server from which an image will be created."
	for pos, srv in enumerate(servers):
	    print "%s: %s" % (pos, srv.name)
	    srv_dict[str(pos)] = srv.id
	selection = None
	while selection not in srv_dict:
	    if selection is not None:
	        print " -- Invalid choice"
	    selection = raw_input("Enter the number for your choice: ")

	server_id = srv_dict[selection]
	print
	nm = raw_input("Enter a name for the image: ")

	img_id = cs.servers.create_image(server_id, nm)

	print "Image '%s' is being created. Its ID is: %s" % (nm, img_id)



if __name__ == '__main__':
	main()