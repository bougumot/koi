# Generic part of a instrumentation make system

TOOLBOX_FILES = toolbox.c

#TBD: This gonna be a library
TOOLBOX = $(TOOLBOX_FILES:.c=.o)
CNT=0

clobber: 
	rm -f *.S 	
	rm -f *.o
	rm -f *.dot
	rm -f *.lst
	rm -f *.cov

asm: $(FILES:.c=.asm)

toolbox:
	gcc $(TOOLBOX_FILES) $(SPECIAL_CFLAGS) -DTRANSITIONS=$(CNT) -c -o toolbox.o

instrument: clobber asm $(FILES:.c=.ins) toolbox
	@echo "Total transitions: "$(CNT)

__app:
	gcc $(TOOLBOX_FILES:.c=.o) $(SPECIAL_CFLAGS) $(FILES:.c=.ins.o) -o $(APP)

graph: $(FILES:.c=.dot)

%.asm:
	gcc $(@:.asm=.c) $(SPECIAL_CFLAGS) -S -DINSTRUMENTED -o $(@:.asm=.S)

%.dot:
	@../make_instrument.py -i $(@:.dot=.S) -g -t coverage.log -o $@ > $(@:.dot=.cov)

%.ins:
	@$(eval cnt= $(shell ../make_instrument.py -i $(@:.ins=.S) -o $(@:.ins=.ins.S) -s $(CNT)))
	@$(eval CNT=$(shell expr $(CNT) + $(cnt)))
	@gcc $(@:.ins=.ins.S) $(SPECIAL_CFLAGS) -c -o $(@:.ins=.ins.o)
	@nm --defined-only $(@).o | grep " [Tt] " | cut -d ' ' -f 3 > $(@).lst


