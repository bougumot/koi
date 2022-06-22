#include <stdio.h>

const char*fmt = "%d:%d\n";

static int __attribute__((noinline))
foo(int b)
{
	printf("I am foo\n");
	return 1*b;
}

void __attribute__((used, noinline))
dump(int index, int label)
{
	printf(fmt, index, label);
}

int main(int argc, char ** argv)
{
	char a;
	int c = 0;

	if (foo(99) != 99) return 1;

	if (c * a > 0) {
		printf("here what we got: %d, %c, %d\n", c, a, foo(c));
	} else {
		foo(5);
		printf("QQ");
	}
	switch (foo(3)) {
		case 3:
			printf("ZZ\n");
			break;
		case 2:
			foo(7);
			break;
		default:
			printf("PID:%d\n", 11);
	}
	return 0;
}
