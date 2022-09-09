import config

if config.platform == "x86_64": 
	from . import x86_64 as asm
	from .definitions.x86_64 import *
elif config.platform == "x86_32":
	from . import x86_32 as asm
	from .definitions.x86_32 import *
elif config.platform == "armv7_32":
	from . import armv7_32 as asm
	from .definitions.armv7_32 import *
else:
	print("UNSUPPORTED PLATFORM")
	exit(1)
