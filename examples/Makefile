# A simple make to cereate a app or .S

FILES = ls.c foo.c
TOOLBOX = toolbox.c
APP = tst_app
CNT=0

#SPECIAL_CFLAGS = -m32

all: $(FILES)
	gcc $^ -o $(APP)

asm: $(FILES:.c=.asm)

%.asm:
	gcc $(@:.asm=.c) $(SPECIAL_CFLAGS) -S -DINSTRUMENTED -o $(@:.asm=.S)

clobber: 
	rm -f *.S 	
	rm -f *.o
	rm -f *.dot
	rm -f *.lst
	rm -f *.cov

graph: $(FILES:.c=.dot)

%.dot:
	@../make_instrument.py -i $(@:.dot=.S) -g -t coverage.log -o $@ > $(@:.dot=.cov)

toolbox:
	gcc $(TOOLBOX) $(SPECIAL_CFLAGS) -DTRANSITIONS=$(CNT) -c -o toolbox.o

instrument: clobber asm $(FILES:.c=.ins) toolbox
	gcc $(TOOLBOX:.c=.o) $(SPECIAL_CFLAGS) $(FILES:.c=.ins.o) -o $(APP)
	@echo "Total transitions: "$(CNT)

%.ins:
	@$(eval cnt= $(shell ../make_instrument.py -i $(@:.ins=.S) -o $(@:.ins=.ins.S) -s $(CNT)))
	@$(eval CNT=$(shell expr $(CNT) + $(cnt)))
	@gcc $(@:.ins=.ins.S) $(SPECIAL_CFLAGS) -c -o $(@:.ins=.ins.o)
	@nm --defined-only $(@).o | grep " [Tt] " | cut -d ' ' -f 3 > $(@).lst
