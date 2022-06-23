import config

if config.platform is "x86_64": 
	import x86_64 as asm
	from definitions.x86_64 import *
elif config.platform is "x86_32":
	import x86_32 as asm
	from definitions.x86_32 import *
else:
	print "UNSUPPORTED PLATFORM"
	exit(1)
