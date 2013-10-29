#!/bin/bash

import os
import pyrax
import sys
import time

def make_choice(item_list, prompt):
	
	for index, item in enumerate(item_list):
		print index, item
	selection = -1
	while selection < 0 or selection > len(item_list) - 1:
		selection = int(raw_input(prompt))
	return item_list[selection]

def main():

	pyrax.set_setting("identity_type", "rackspace")
	creds_file = os.path.expanduser('~/.rackspace_cloud_credentials')
	pyrax.set_credential_file(creds_file)

	available_regions = pyrax.regions

	print "Regions Available:", " ".join(list(available_regions))
	region = ""
	while region not in available_regions:
		region = raw_input("Select Region: ")

	cs = pyrax.connect_to_cloudservers(region)
	
#find a way to use string to format this output into tow or three collums
	available_images = cs.images.list()
	available_flavors = cs.flavors.list()

	image = make_choice(available_images, "Select an image: ")
	flavor = make_choice(available_flavors, " select a flavor:")

	base_name = raw_input("Base Server name: ")
	server_count = int(raw_input("Number of servers to build: "))

	print "building {} servers with base name '{}', flavor '{}, and image '{}'.".format(server_count, base_name, flavor.name, image.name)
	choice = raw_input('Proceed? Y/[N]: ')
	if not choice == 'Y':
		print "Exiting..."
		sys.exit(0)

	new_servers = []
	completed_servers = []

#create servers and add them to the new_servers list	
	for i in range(1, server_count + 1):
		server_name = base_name + str(i)
		print "Creating {}...".format(server_name)
		try:
			server = cs.servers.create(server_name, image, flavor)
		except Exception, e:
			print "Error in creating {}: {}".format(server_name, e)
		else:
				new_servers.append((server,server.adminPass))

	while new_servers:
		time.sleep(10)
		new_servers_copy = list(new_servers)
		for server, admin_pass in new_servers_copy:
			server = cs.servers.get(server.id)
			if server.status == 'ERROR':
				print "{} - Error in build".format(server.name)
				new_servers.remove((server, admin_pass))
				continue
			print "{} - {}% complete".format(server.name, server.progress)
			if server.status == 'ACTIVE':
				completed_servers.append((server, admin_pass))
				new_servers.remove((server, admin_pass))
	print
	print "completed Server Info:"
	print
	for server, admin_pass in completed_servers:
			print "Name: ", server.name
			print "ID: ", server.id
			print "Status: ", server.status
			print "Admin Password: ", admin_pass
			print "Server Network Addresses: ", server.networks
if __name__ == '__main__':
		main()

