from pingcheck import IPAddress
a1 = IPAddress('192.168.1.1')
a2 = IPAddress('192.168.1.1')
b1 = IPAddress("192.168.1.2")
b2 = IPAddress("192.168.1.2")

tests = 0
pass_count = 0
fail_count = 0

def passing(string):
	pass_count +=1
	tests += 1
	print(string + " pass")
	
	
def fail(string):
	fail_count += 1
	tests += 1
	print(string + " FAIL")
	
def result(string, objA, comparitor_string, objB):
	if comparitor_string == "<":
		if objA < objB:
			passing(string)
		else:
			fail(string)
	elif comparitor_string == ">":
		if objA > objB:
			passing(string)
		else:
			fail(string)
	elif comparitor_string == "==":
		if objA == objB:
			passing(string)
		else:
			fail(string)	
	elif comparitor_string == "<=":
		if objA <= objB:
			passing(string)
		else:
			fail(string)	
	elif comparitor_string == ">=":
		if objA >= objB:
			passing(string)
		else:
			fail(string)	
	elif comparitor_string == "!=":
		if objA != objB:
			passing(string)
		else:
			fail(string)	
	
def lt_tests():
	if a1 < b1:
		print("a1 < b2"
		passing()
	else:
		fail()
	
	if 
	

ip_list = [IPAddress('192.168.1.1'), IPAddress('127.0.0.1'), IPAddress('192.169.1.1'), IPAddress("192.168.2.1"), IPAddress("192.168.0.1"), IPAddress("127.1.0.1")]

print(ip_list.sort())