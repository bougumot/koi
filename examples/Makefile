# A simple make to cereate a app or .S

FILES = ls.c foo.c
APP = tst_app

include $(KOI_ROOT)/toolbox/Makefile.koi 

SPECIAL_CFLAGS = -g
#PLATFORM_CFLAGS = -m32

all: $(FILES)
	gcc $^ -o $(APP)

all_oc: instrument
	gcc $(TOOLBOX) $(FILES:.c=.ins.o) $(PLATFORM_CFLAGS) -o $(APP)

clobber: koi_clobber
	@rm -f $(APP)
