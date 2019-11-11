from pingcheck import IPAddress
import random


class TestRecord:
	def __init__(self,):
		self.num_tests_completed = 0
		self.pass_count = 0
		self.fail_count = 0
	
	def passing(self, message = ""):
		self.pass_count += 1
		self.num_tests_completed +=1
		if message is not None:
			print(message + " pass")
			
	def fail(self, message = ""):
		self.fail_count += 0
		self.num_tests_completed +=1
		if message is not None:
			print(message + " FAIL")
	
	def dump(self):
		print("total tests: %s" % self.num_tests_completed)
		print("accuracy: %s" % (self.pass_count / self.num_tests_completed)  * 100)
		print("num pass: %s num fail %s " % (self.pass_count, self.num_tests_completed))

	

	
def build_ip_list():
	my_list = list()
	
	for o1 in range(192, 194):
		for o2 in range(168,170):
			for o3 in range(1, 3):
				for o4 in range(90,130):
					my_list.append(IPAddress("%s.%s.%s.%s" % (o1,o2,o3,o4) ))
					
	return my_list


def launch():
	main_list = build_ip_list()
	print("master list done")
	list_a = build_ip_list()
	print("list a done")
	list_b = build_ip_list()
	print('list b done')
	list_c = build_ip_list()
	print('list c done')
	
	print("begin randoms")
	random.shuffle(list_a)
	random.shuffle(list_b)
	random.shuffle(list_c)
	if list_a==list_b:
		print("WARNING: A==B")
	if list_a==list_c:
		print("WARNING: A==C")
	if list_c==list_b:
		print("WARNING: C==B")
	
	print('equivalency tests done')
	
	holder = TestRecord()
	list_a.sort()
	list_b.sort()
	list_c.sort()
	
	if main_list == list_a:
		holder.passing("A ==master")
	else:
		holder.fail("A !=master")
		
	if main_list == list_b:
		holder.passing("B ==master")
	else:
		holder.fail("B !=master")
		
	if main_list == list_c:
		holder.passing("c ==master")
	else:
		holder.fail("c !=master")
		
		
def launch2():
	a = IPAddress('192.168.1.1')
	b = IPAddress('192.168.1.2')
	c = IPAddress('192.168.0.1')
	print(a < b)
	print(a < c)
	print(b < c)
	print(b < a)
	print(c < a)
	print(c < b)
	
if __name__ == "__main__":
	launch2()
	launch()