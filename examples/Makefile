# A simple make to cereate a app or .S

FILES = ls.c
TOOLBOX = toolbox.c
APP = tst_app
CNT=100

all: $(FILES) $(TOOLBOX)
	gcc $^ -o $(APP)

asm: $(FILES:.c=.asm)

%.asm:
	gcc $(@:.asm=.c) -S -o $(@:.asm=.S)

clobber: 
	rm -f *.S 	
	rm -f *.o

instrument: clobber asm $(FILES:.c=.ins)
	gcc $(TOOLBOX) -DTRANSITIONS=$(CNT) $(FILES:.c=.ins.o) -o $(APP)
	@echo "Total transitions: "$(CNT)

%.ins:
	$(eval cnt= $(shell ../make_instrument.py -i $(@:.ins=.S) -o $(@:.ins=.ins.S)))
	$(eval CNT=`expr $(CNT) + $(cnt)`)
	gcc $(@:.ins=.ins.S) -c -o $(@:.ins=.ins.o)
