import re
import html

from ins_blocks import CodeBlock
from ins_definitions import *
from ins_graphs import *

# Get function body
lines = []
with open('input.S') as f:
    lines = f.readlines()
f.close()

line_count = 0
block_count = 0;

fragments = [] # An empty list for code fragments
new_frag = CodeBlock(block_count, "__FIRST_BLOCK", line_count);

for line in lines:
    line_count += 1

    matchlabel = label_mark.search(line)
    matchjump = jump_cmd.search(line)
    if matchlabel:
	new_frag.closeBlock(line_count - 1)
	fragments.append(new_frag)
        #new_frag.emitBlock()

        block_count += 1
        new_frag = CodeBlock(block_count, line, line_count);
        new_frag.addLine(line, line_count)
    elif matchjump:
	new_frag.addLine(line, line_count)
	new_frag.closeBlock(line_count)
        fragments.append(new_frag)
	#new_frag.emitBlock()
        block_count += 1
        new_frag = CodeBlock(block_count, line, line_count + 1)
    else:
        if new_frag is not None:
            new_frag.addLine(line, line_count);
# The last one
fragments.append(new_frag)
new_frag.closeBlock(line_count)
#new_frag.emitBlock()

# Remove empty boxes
fragments[:] = [x for x in fragments if not (len(x.lines) == 1)]

# Build transitions	
for index, frag in enumerate(fragments):
    # only for meaningful boxes
    if not frag.meaningful:
        continue
    # for every code fragment except the empy ones
    for subline in frag.lines:
    #for every line in a fragment
        matchobj = jump_cmd.search(subline)
	if matchobj:
            # search for a match:
            for sfrag in fragments:
                if not matchobj.group(2):
                    continue
                if matchobj.group(2)+":" in sfrag.label:
                    trans_loc = line_address.search(subline)
                    if trans_loc:
                        lfrom = trans_loc.group(1)
                        trans_loc = line_address.search(sfrag.lines[1])
                        lto = trans_loc.group(1)
                    frag.jtransition = (lfrom, lto)
                    frag.jump_to_block = sfrag.lines[0]
           
    if (index+1 < len(fragments) and "jmp" not in subline and "ret" not in subline):
         lfrom = frag.last_number
         lto = frag.last_number + 1
         frag.stransition = (lfrom, lto)
         frag.skip_to_block = fragments[index + 1].lines[0]

         matchobj = cond_jump_cmd.search(subline)
         if matchobj:
             frag.fallthru = True

#graphBEGIN()
#for frag in fragments:
#	frag.emitBlock()
#for frag in fragments:
#	frag.emitTransitions()
#graphEND()

for frag in fragments:
    frag.instrumentBlock()
    frag.renderBlock(False)

