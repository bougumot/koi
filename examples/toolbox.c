#include <stdio.h>

const char*fmt = "%d:%d\n";

void __attribute__((used, noinline))
dump(int from, int to)
{
	printf(fmt, from, to);
}
