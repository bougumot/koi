#include <stdio.h>

#define TF_PENDING	1
#define TF_JUMPED	2

typedef struct __attribute__((packed)) {
	void * from;
	void * to;
	unsigned int flags;
	size_t t;
} transition_t;

static transition_t  __transitions[TRANSITIONS+1];

const char*fmt = "%d::%d:%d;[%d]\n";

void __attribute__((used, noinline))
__koi_covdump(int from, int to, int id)
{
	static int prev_from;
	static int prev_id = -1;	

#if DEBUG
	printf("\t");printf("%d::%d:%d [%08x::%08x];\n", id, from, to,
		__transitions[prev_id].flags, __transitions[id].flags);
#endif

	if (prev_from == from){
		// We are in a skip mark, so it was not a jump
		if (__transitions[id - 1].flags & TF_PENDING) {
			__transitions[id - 1].from = 0;
			__transitions[id - 1].to = 0;
			__transitions[id - 1].flags = 0;
			__transitions[id - 1].t = 0;
		}
		if (__transitions[id].flags & TF_JUMPED) {
			// Decrement Jump temperature
			if (__transitions[id - 1].t > 0) {
				__transitions[id - 1].t -= 1;
			}
		}
	} else {
		// This was a jump, remove pending flag
		if (prev_id != -1) {
			__transitions[prev_id].flags &= ~TF_PENDING;
		}
	}

	__transitions[id].from = (void*)from;
	__transitions[id].to = (void*)to;
	__transitions[id].t += 1;
	
	// It has a destination, so mark it a jump
	if (to > 0) {
		// If not already jumped
		if (!(__transitions[id].flags & TF_JUMPED)) {
			__transitions[id].flags = TF_PENDING | TF_JUMPED;
		}
	}
	prev_from = from;
	prev_id = id;
}

void __attribute__((used, noinline))
__koi_covdump_render()
{
	int i;
	for (i = 0; i < TRANSITIONS; i++) {
		if (__transitions[i].from || __transitions[i].to) {
			printf(fmt, i, __transitions[i].from,
				__transitions[i].to, __transitions[i].t);
		}
	}
}

