#include <stdio.h>

#define FROM	0
#define TO	1
#define FLAGS	2

#define TF_PENDING	1
#define TF_JUMPED	2

static int __transitions[TRANSITIONS+1][3];

const char*fmt = "%d::%d:%d;\n";

void __attribute__((used, noinline))
dump(int from, int to, int id)
{
	static int prev_from;
	static int prev_id = -1;	

#if DEBUG
	printf("\t");printf("%d::%d:%d [%08x::%08x];\n", id, from, to,
		__transitions[prev_id][FLAGS], __transitions[id][FLAGS]);
#endif

	if (prev_from == from){
		// We are in a skip mark, so it was not a jump
		if (__transitions[id - 1][FLAGS] & TF_PENDING) {
			__transitions[id - 1][FROM] = 0;
			__transitions[id - 1][TO] = 0;
			__transitions[id - 1][FLAGS] = 0;
		}
	} else {
		// This was a jump, remove pending flag
		if (prev_id != -1) {
			__transitions[prev_id][FLAGS] &= ~TF_PENDING;
		}
	}

	__transitions[id][FROM] = from;
	__transitions[id][TO] = to;
	
	// It has a destination, so mark it a jump
	if (to > 0) {
		// If not already jumped
		if (!(__transitions[id][FLAGS] & TF_JUMPED)) {
			__transitions[id][FLAGS] = TF_PENDING | TF_JUMPED;
		}
	}
	prev_from = from;
	prev_id = id;
}

void __attribute__((used, noinline))
render_dump()
{
	int i;
	for (i = 0; i < TRANSITIONS; i++) {
		if (__transitions[i][0] || __transitions[i][1]) {
			printf(fmt, i, __transitions[i][0], __transitions[i][1]);
		}
	}
}
