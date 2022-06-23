#include <stdio.h>

static int __transitions[TRANSITIONS+1][2];

const char*fmt = "%d::%d:%d;\n";

void __attribute__((used, noinline))
dump(int from, int to, int id)
{
//	printf(fmt, id, from, to);
	static int prev_from;
	
	if (prev_from == from) {
		__transitions[id - 1][0] = 0;
		__transitions[id - 1][1] = 0;
	}

	__transitions[id][0] = from;
	__transitions[id][1] = to;
	prev_from = from;
}

void __attribute__((used, noinline))
render_dump()
{
	for (int i = 0; i < TRANSITIONS; i++) {
		if (__transitions[i][0] || __transitions[i][1]) {
			printf(fmt, i, __transitions[i][0], __transitions[i][1]);
		}
	}
}
