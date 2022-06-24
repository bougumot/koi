# A simple make to cereate a app or .S

FILES = ls.c foo.c
APP = tst_app

include Makefile.inc 

#SPECIAL_CFLAGS = -m32

all: $(FILES)
	gcc $^ -o $(APP)

all_oc: instrument
	gcc $(TOOLBOX) $(FILES:.c=.ins.o) -o $(APP)
