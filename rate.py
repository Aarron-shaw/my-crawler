full = 100
v = 25
j = (full - v) / 2
a = (full - v) / 2

prices = ["480","600","720","820"]

for i in prices:
	print("Jamie:	",j * int(i) / 100)
	print("Aarron:	",a * int(i) / 100)
	print("Victor:	",v * int(i) / 100)
	total = (j * int(i) / 100) + (a * int(i) / 100) + (v * int(i) / 100)
	print("Total:	", total)