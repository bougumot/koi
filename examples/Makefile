# A simple make to cereate a app or .S

FILES = ls.c

all: $(FILES)
	gcc $^ -o tst_app
asm: $(FILES)
	gcc $^ -S -o ../input.S
