with open('keywords.txt', 'r') as f, open('output.txt', 'w') as o:
	for line in f:
		o.write(f'\t\'{line.rstrip()}\': \'TK_{line.rstrip().upper()}\',\n')