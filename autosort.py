import os
import time

source = os.path.abspath("tosort")
target = os.path.abspath("autosort")

stack = [source]
files = []
dirs = []

fh = open("log_" + time.strftime("%Y%m%d_%H%M%S") + ".txt","w")

while len(stack) > 0:
	f = stack.pop()
	if os.path.isdir(f):
		dirs.append(f)
		for t in os.listdir(f):
			stack.append(os.path.join(f,t))
	else:
		files.append(f)

for f in files:
	year = str(time.localtime(os.stat(f).st_mtime).tm_year)
	ext = os.path.splitext(f)[1][1:].lower()
	if len(ext) == 0:
		ext = "blank"
	parent = os.path.split(os.path.dirname(f))[1]
	name = os.path.split(f)[1]

	n = os.path.join(target, year, ext, parent, name)

	if os.path.exists(n):
		c = 0
		while(os.path.exists(n)):
			n = os.path.join(target, year, ext, "z%03d" % c, parent, name)
			c = c + 1

	if not os.path.exists(os.path.split(n)[0]):
		os.makedirs(os.path.split(n)[0])

	fh.write(f + " -> " + n + "\n")
	print(f + " -> " + n)

	os.rename(f,n);

dirs.reverse()

for d in dirs:
	if len(os.listdir(d)) == 0:
		fh.write("- " + d + "\n")
		print("- " + d)
		os.rmdir(d)

fh.close()
