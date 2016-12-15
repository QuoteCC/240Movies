import omdb
import math
import sys

file = open(sys.argv[1], "r")
data = file.read()
file.close

s = data.splitlines()
print("Lines found: " + str(len(s)))



for l in s[1:]:
	x = l.split(',')
	x = x[28]
	
	while len(x) < 7:
		x = "0" + x
	x = "tt"+x	
	
	res = omdb.request(i=x, tomatoes='true', r='JSON')
	xml_content = res.content
	
	print(xml_content)
	