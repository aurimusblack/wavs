with open("xsspayloads.txt") as f:
	for line in f:
		li = line.strip()
		lin = "\"\"\"" + li + "\"\"\","
		print lin


