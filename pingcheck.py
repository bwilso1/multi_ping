import os
import sys
import subprocess


class Invalid_IP_Address(Exception):
	def __init__(self, message='not enough octets', octets = 0):
		self.message = message
		self.octets = octets
		
	def __str__(self):
		return "%s octets was %s" % (self.message, self.octets)
		
	def __repr__(self):
		return self.__str__()
		
class IPAddress():

	def __init__(self,ip_address_string):
		self.octets = ip_address_string.split('.')
		if len(self.octets) < 4:
			raise Invalid_IP_Address(octets = len(self.octets))
		else:
			for _unused in range(0,4):
				self.octets[_unused] = int(self.octets[_unused])
			
	def __str__(self):
		return "%s.%s.%s.%s" % (self.octets[0], self.octets[1], self.octets[2],self.octets[3])
		
	def __repr__(self):
		return self.__str__()
		
	# found LT GT here
	# https://stackoverflow.com/questions/15461574/python-overloading-operators
	
	def __lt__(self, other):
		if self.octets[0] <= other.octets[0]:
			if self.octets[1] <= other.octets[1]:
				if self.octets[2] <= other.octets[2]:
					if self.octets[3] < other.octets[3]:
						return True
		return False
		
	def __le__(self, other):
		if self.octets[0] <= other.octets[0]:
			if self.octets[1] <= other.octets[1]:
				if self.octets[2] <= other.octets[2]:
					if self.octets[3] <= other.octets[3]:
						return True
		return False
		
	def __eq__(self, other):
		if self.octets[0] == other.octets[0]:
			if self.octets[1] == other.octets[1]:
				if self.octets[2] == other.octets[2]:
					if self.octets[3] == other.octets[3]:
						return True
		return False
		
	def __gt__(self, other):
		if self.octets[0] >= other.octets[0]:
			if self.octets[1] >= other.octets[1]:
				if self.octets[2] >= other.octets[2]:
					if self.octets[3] > other.octets[3]:
						return True
		return False
	
	def __ge__(self, other):
		if self.octets[0] >= other.octets[0]:
			if self.octets[1] >= other.octets[1]:
				if self.octets[2] >= other.octets[2]:
					if self.octets[3] >= other.octets[3]:
						return True
		return False
		
	def __ne__(self, other):
		if self.octets[0] != other.octets[0]:
			if self.octets[1] != other.octets[1]:
				if self.octets[2] != other.octets[2]:
					if self.octets[3] != other.octets[3]:
						return True
		return False
	
		
		
def launch(ip_address = None):
	if ip_address:
		print("not supported, proceeding with default")

	
	print('loading cached ip list')
	temp_ips, ip_file = ip_cache_load("ip_cache.txt")
	pre_check_ip(temp_ips)
	
	print("beginning sweep\n")
	valid_ip = ip_sweep('192.168.1.1')
			
	clear_line()
	print("found these IP's")
	for ip in valid_ip:
		print(ip)
		append_ip_cache(ip_file, ip, valid_ip)
		
	ip_file.flush()
	ip_file.close()
		
def ip_sweep(base_ip_string, octet_flag = 1, start = 0, stop = 255):
	"""
	@param - base	model IP to start with
	@param - octet_flag.  Bitwise flag to switch which IP octets to cycle start( 0) to stop (255)
	@param - start	number to begin cycling IP octet from
	@param - stop	number to limit cycling IP octect from
	
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
						valid_ip.append("%s.%s.%s.%s" % (oct_1, oct_2, oct_3, oct_4))
					
					# update screen while pinging
					x = x + 1
					sys.stdout.write('.')
					sys.stdout.flush()
					if x % 10 == 0:
						clear_line("Running")
	
	print('\n')
	return valid_ip
						

def append_ip_cache(file_obj, ip_address, ip_list):
	# would like to sort by IP octets, but that will come later
	# doing wrapper for now
	file_obj.write(str(ip_address) + '\n')
	file_obj.flush()

def pre_check_ip(ip_list):
# see here
#https://www.python4networkengineers.com/posts/how_to_sort_ip_addresses_with_python/
	temp = sorted(ip_list)
	
	print("checking for cached IP's")
	for ip in temp:
		ip = ip.rstrip()
		result = ping(ip)
		
		if result == 0:
			print ("%s \t OK" % ip)
		else:
			print ("%s \t down" % ip)
		

def ip_cache_load(filename):
	'''  
	returns a tuple of (prev IP list , file obj)
	'''
	file = None
	ip_list = []
	if os.path.exists(filename) and os.path.isfile(filename):
		print ("%s found" % filename)
		file = open(filename, "r")
		for line in file:
			ip_list.append(line)
		
		file.close()
		
	else:
		print ("%s not found " % filename)
	
	#right now we blow away file. may change later to aggregate past IP's
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
	# taken from wellspokenman
	# https://stackoverflow.com/questions/2953462/pinging-servers-in-python#comment85724760_35625078
	
	#added wait time of 100 ms
	process = subprocess.Popen(["ping", "-n", "1", "-w", "100", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
	streamdata = process.communicate()[0] 
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