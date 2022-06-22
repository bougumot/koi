#include <stdio.h>

const char*fmt = "%d:%d\n";

void __attribute__((used, noinline))
dump(int index, int label)
{
	printf(fmt, index, label);
}
