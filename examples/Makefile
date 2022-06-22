# A simple make to cereate a app or .S

FILES = ls.c
TOOLBOX = toolbox.c
APP = tst_app
CNT=0

all: $(FILES)
	gcc $^ -o $(APP)

asm: $(FILES:.c=.asm)

%.asm:
	gcc $(@:.asm=.c) -S -DINSTRUMENTED -o $(@:.asm=.S)

clobber: 
	rm -f *.S 	
	rm -f *.o

instrument: clobber asm $(FILES:.c=.ins)
	gcc $(TOOLBOX) -DTRANSITIONS=$(CNT) $(FILES:.c=.ins.o) -o $(APP)
	@echo "Total transitions: "$(CNT)

%.ins:
	$(eval cnt= $(shell ../make_instrument.py -i $(@:.ins=.S) -o $(@:.ins=.ins.S) -s $(CNT)))
	$(eval CNT=$(shell expr $(CNT) + $(cnt)))
	gcc $(@:.ins=.ins.S) -c -o $(@:.ins=.ins.o)
