import os
import sys
import subprocess


class Invalid_IP_Address(Exception):
	def __init__(self, message='invalid number of octets', octets = 0):
		self.message = message
		self.octets = octets
		
	def __str__(self):
		return "%s octets was %s" % (self.message, self.octets)
		
	def __repr__(self):
		return self.__str__()
		
class IPAddress:

	def __init__(self,ip_address_string):
		#self.__class__.__name__ = "IPAddress"
		self.octets = ip_address_string.split('.')
		if len(self.octets) < 4:
			raise Invalid_IP_Address(octets = len(self.octets))
		elif len(self.octets) > 4:
			raise Invalid_IP_Address(octets= len(self.octets))
		elif len(self.octets) == 4:
			for _unused in range(0,4):
				self.octets[_unused] = int(self.octets[_unused])
		else:
			# should not be logically possible, but just in case
			raise Invalid_IP_Address(message="epic fail in IPAddress constructor",octets=len(self.octets))
		
		self.binary = (self.octets[0] << 24) + (self.octets[1] << 16) + (self.octets[2] << 8) + self.octets[3]
		
	def __str__(self):
		return "%s.%s.%s.%s" % (self.octets[0], self.octets[1], self.octets[2],self.octets[3])
		
	def __repr__(self):
		return self.__str__()
	
		
		
	# found LT GT here
	# https://stackoverflow.com/questions/15461574/python-overloading-operators
	
	def __lt__(self, other):
		return self.binary < other.binary

		
	def __le__(self, other):
		return self.binary <= other.binary
		
	def __gt__(self, other):
		return self.binary > other.binary
	
	def __ge__(self, other):
		return self.binary >= other.binary

	def __eq__(self, other):
		return self.binary == other.binary
		
	def __ne__(self, other):
		return self.binary != other.binary
	
	def __hash__(self):
		return hash(str(self.binary))
		
def launch(ip_address = None):
	if ip_address:
		print("not supported, proceeding with default")

	
	print('loading cached ip list')
	cached_ips, ip_file = ip_cache_load("ip_cache.txt")
	pre_check_ip(cached_ips)
	
	print("beginning sweep\n")
	valid_ip_list = ip_sweep('192.168.1.1')
			
	clear_line()
	print("found these IP's")
	for ip in valid_ip_list:
		print(ip)

	append_ip_cache(ip_file,cached_ips, valid_ip_list)
		
def ip_sweep(base_ip_string, octet_flag = 1, start = 0, stop = 255):
	"""
	@param - base	model IP to start with
	@param - octet_flag.  Bitwise flag to switch which IP octets to cycle start( 0) to stop (255)
	@param - start	number to begin cycling IP octet from
	@param - stop	number to limit cycling IP octect from
	
	@:return - List of found IP's of type <IPAddress>
	
	example if you use... 
	base_ip_string = 192.168.1.0
	start = 5
	stop = 200
	octet_flag = 5
	
	this script will ping
	192.005.001.005 - 192.005.001.200
	192.006.001.005 - 192.006.001.200
	...
	...
	192.199.001.005 - 192.199.001.200
	192.200.001.005 - 192.200.001.200
	
	(order may not be guaranteed)
	
	because 5 is 0101 in binary. so it flags
	OFF._ON.OFF._ON
	
	where 'on' are the octets that are cycled from @param start to @param stop.
	"""
	
	################ setup ###############
	base = IPAddress(base_ip_string)
	stop_ip = IPAddress( "%s.%s.%s.%s" % (base.octets[0], base.octets[1], base.octets[2], base.octets[3]))
	
	if octet_flag & 1 == 1:
		# iterate 4th octet
		base.octets[3] = start
		stop_ip.octets[3] = stop
	
	if octet_flag & 2 == 2:
		#iterate 3rd octet
		base.octets[2] = start
		stop_ip.octets[2] = stop
	
	if octet_flag & 4 == 4:
		#iterate 2nd octet
		base.octets[1] = start
		stop_ip.octets[1] = stop
		
	if octet_flag & 8 == 8:
		#iterate 1st octet
		base.octets[0] = start
		stop_ip.octets[0] = stop
		
	valid_ip = list()
	x = 0
	clear_line("Running")
	for oct_1 in range(base.octets[0], stop_ip.octets[0] + 1):
		
		for oct_2 in range(base.octets[1], stop_ip.octets[1] + 1):
			
			for oct_3 in range(base.octets[2], stop_ip.octets[2] + 1):
			
				for oct_4 in range (base.octets[3], stop_ip.octets[3] + 1):
					result = ping("%s.%s.%s.%s" % (oct_1, oct_2, oct_3, oct_4) )
					if result == 0:
						valid_ip.append(IPAddress("%s.%s.%s.%s" % (oct_1, oct_2, oct_3, oct_4)))
					
					# update screen while pinging
					x = x + 1
					sys.stdout.write('.')
					sys.stdout.flush()
					if x % 10 == 0:
						clear_line("Running")
	
	print('\n')
	return valid_ip
						

def append_ip_cache(file_obj,ip_list_a,ip_list_b):
	merged_list = list(set(ip_list_a + ip_list_b))
	merged_list.sort()
	
	for ip_address in merged_list:
		file_obj.write(str(ip_address) + '\n')
		
	file_obj.flush()
	file_obj.close()
	
def is_sorted(ip_list):
	_temp_len = len(ip_list) - 1
	for i in range(0,_temp_len):
		if ip_list[i] > ip_list[i + 1]:
			return False
		
	return True

def pre_check_ip(ip_list):
# see here
#https://www.python4networkengineers.com/posts/how_to_sort_ip_addresses_with_python/
	temp = sorted(ip_list)
	
	print("checking for cached IP's")
	for ip in temp:
		result = ping(ip)
		
		if result == 0:
			print ("%s \t OK" % ip)
		else:
			print ("%s \t down" % ip)
		

def ip_cache_load(filename):
	'''  
	returns a tuple of (cached IP list , file obj)
	'''
	file = None
	ip_list = []
	if os.path.exists(filename) and os.path.isfile(filename):
		print ("%s found" % filename)
		file = open(filename, "r")
		for line in file:
			line = line.strip()
			if line is not "":
				try:
					ip_list.append(IPAddress(line))
				except Invalid_IP_Address as e:
					print(e)
			else:
				print("warning, empty line in %s" % filename)
		
		file.close()
		
	else:
		print ("%s not found " % filename)
	
	# overwriting file, we merge both lists now
	file = open(filename, "w+")
		
	
	print ("len IPs: %s " % len(ip_list))
	return [ip_list, file]
		
	
	
		
	
	

def clear_line(message = None):
	if message is None:
		message = ""
	else:
		message = str(message) + " "
		
	cr = chr(13)
	sys.stdout.write(cr)
	sys.stdout.write('                                  ')
	sys.stdout.flush()
	sys.stdout.write(cr)
	sys.stdout.flush()
	sys.stdout.write("%s" % message)
	

def ping(host):

	if type(host).__name__ is "str" and host.strip is "":
		return 1
		
	if type(host).__name__ is "IPAddress":
		host = str(host)
		
	# taken from wellspokenman
	# https://stackoverflow.com/questions/2953462/pinging-servers-in-python#comment85724760_35625078
	#added wait time of 100 ms
	process = subprocess.Popen(["ping", "-n", "1", "-w", "100", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
	streamdata = process.communicate()[0]
	#print(str(streamdata))
	if 'unreachable' in str(streamdata): 
		return 1
	else:
		return process.returncode

if __name__ == "__main__":
	print("length of sys.argv: %s" % (len(sys.argv), ) )
	for count, elm in enumerate(sys.argv):
		print ("arg%s: %s" % (count, elm))
	
	if len(sys.argv) > 1:
		launch(sys.argv[1])
	else:
		launch()