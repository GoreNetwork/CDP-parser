import os
import re
import socket
import sys
import netmiko
import time
from getpass import getpass
from ciscoconfparse import CiscoConfParse
from pprint import pprint

def get_ip (input):
	return(re.findall(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', input))

	
def read_doc (file_name):
	doc = []
	for line in open(file_name, 'r').readlines():
		doc.append(line)
	return doc

def to_doc(file_name, varable):
	f=open(file_name, 'w')
	f.write(varable)
	f.close()		
	
def fix_for_ciscoconfparse(file_name):
	cdp = read_doc(file_name)
	cdp_str = ""
	for line in cdp:
		
		if "---" not in line:
			line = "     "+line
		cdp_str = cdp_str+line
		#print (cdp_str)
	to_doc(file_name, cdp_str)

def parse_cdp_out(file_name):
	cdp_parse = {}
	fix_for_ciscoconfparse(file_name)
	cdp_doc=CiscoConfParse(file_name)
	strip_these = ("[","]","'", "")
	cdp_entries = cdp_doc.find_objects("-----")
	all_cdp_entries = []
	for cdp_entrie in cdp_entries:
		next_line = False
		cdp_parse = {}
		for cdp_line in cdp_entrie.all_children:
			if "IP" in cdp_line.text:
				ip = str(get_ip (str(cdp_line.text)))
				for each in strip_these:
					ip = ip.strip(each)
				cdp_parse['remote_ip'] = ip
				
			if "Device ID: " in cdp_line.text:
				id_start = str(cdp_line.text).find(":")+2
				remote_id = str(cdp_line.text)[id_start:]
				cdp_parse['remote_id'] = remote_id
			if "Platform: " in cdp_line.text:
				platform_start = str(cdp_line.text).find(":")+2
				tmp = str(cdp_line.text)[platform_start:]
				platform_end = tmp.find(",")
				platform = tmp[:platform_end]
				cdp_parse['platform'] = platform
			if "Capabilities: " in cdp_line.text:
				capabilities_start = str(cdp_line.text).find("Capabilities:")+14
				capabilities = str(cdp_line.text)[capabilities_start:]
				cdp_parse['capabilities'] = capabilities
			if "Interface: " in cdp_line.text:
				interface_start = str(cdp_line.text).find(":")+2
				interface_end = str(cdp_line.text).find(",")
				local_int = str(cdp_line.text)[interface_start:interface_end]
				cdp_parse['local_int'] = local_int
			if "Port ID (outgoing port): " in cdp_line.text:
				interface_start = str(cdp_line.text).find("Port ID (outgoing port):")+25
				remote_int = str(cdp_line.text)[interface_start:]
				cdp_parse['remote_int'] = remote_int	
	
			if next_line == True:
				version = str(cdp_line.text).lstrip(' ')
				cdp_parse['version'] = version
				next_line = False
				
			if "Version :" in cdp_line.text:
				next_line = True
				
			
		all_cdp_entries.append(cdp_parse)
	return all_cdp_entries
		
pprint(parse_cdp_out("cdp_info.txt"))
			
			
	
	


