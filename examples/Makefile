# A simple make to cereate a app or .S

FILES = ls.c foo.c
APP = tst_app

include $(KOI_ROOT)/toolbox/Makefile.koi 

SPECIAL_CFLAGS = -g -O2
#PLATFORM_CFLAGS = -m32

all: $(FILES)
	gcc $^ -o $(APP)

all_oc: koi_instrument koi_toolbox 
	gcc $(TOOLBOX) $(FILES:.c=.ins.o) $(PLATFORM_CFLAGS) -o $(APP)

clobber: koi_clobber koi_clean_toolbox
	@rm -f $(APP)
