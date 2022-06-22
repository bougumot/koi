# A simple make to cereate a app or .S

FILES = ls.c
TOOLBOX = toolbox.c
APP = tst_app

all: $(FILES) $(TOOLBOX)
	gcc $^ -o $(APP)

asm: $(FILES:.c=.asm)

%.asm:
	gcc $(@:.asm=.c) -S -o $(@:.asm=.S)

clobber: 
	rm -f *.S 	
	rm -f *.o

instrument: clobber asm $(FILES:.c=.ins)
	gcc $(TOOLBOX) $(FILES:.c=.ins.o) -o $(APP)
%.ins:
	../make_instrument.py -i $(@:.ins=.S) -o $(@:.ins=.ins.S)
	gcc $(@:.ins=.ins.S) -c -o $(@:.ins=.ins.o)
