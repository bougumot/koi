#!/usr/bin/python
	
import sys, getopt
import re
import html
import platform.platform as platform
	
from ins_blocks import CodeBlock
from ins_graphs import *

if __name__ == "__main__":
	inputfile = 'input.S'
	outputfile = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hi:o:g",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'USAGE: -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'USAGE: -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt == '-g':
			doGraph = True
	print 'Input file is ', inputfile
	if outputfile is not None:
		print 'Output file is ', outputfile
	else:
		print 'Using stdout'
		
	# Get function body
	lines = []
	with open(inputfile) as f:
		lines = f.readlines()
	f.close()
	
	line_count = 0
	block_count = 0;
	
	fragments = [] # An empty list for code fragments
	new_frag = CodeBlock(block_count, "__FIRST_BLOCK", line_count);
	
	for line in lines:
		line_count += 1
	
		matchlabel = platform.label_mark.search(line)
		matchjump = platform.jump_cmd.search(line)
		if matchlabel:
			new_frag.closeBlock(line_count - 1)
			fragments.append(new_frag)
			block_count += 1
			new_frag = CodeBlock(block_count, line, line_count);
			new_frag.addLine(line, line_count)
		elif matchjump:
			new_frag.addLine(line, line_count)
			new_frag.closeBlock(line_count)
			fragments.append(new_frag)
			block_count += 1
			new_frag = CodeBlock(block_count, line, line_count + 1)
		else:
			if new_frag is not None:
				new_frag.addLine(line, line_count);
	# The last one
	fragments.append(new_frag)
	new_frag.closeBlock(line_count)
	
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
			matchobj = platform.jump_cmd.search(subline)
		if matchobj:
				# search for a match:
				for sfrag in fragments:
					if not matchobj.group(2):
						continue
					if matchobj.group(2)+":" in sfrag.label:
						trans_loc = platform.line_address.search(subline)
						if trans_loc:
							lfrom = trans_loc.group(1)
							trans_loc = platform.line_address.search(sfrag.lines[1])
							lto = trans_loc.group(1)
						frag.jtransition = (lfrom, lto)
						frag.jump_to_block = sfrag.lines[0]
			   
		if (index+1 < len(fragments) and "jmp" not in subline and "ret" not in subline):
			 lfrom = frag.last_number
			 lto = frag.last_number + 1
			 frag.stransition = (lfrom, lto)
			 frag.skip_to_block = fragments[index + 1].lines[0]
	
			 matchobj = platform.cond_jump_cmd.search(subline)
			 if matchobj:
				 frag.fallthru = True

	# Some block magic with output
	original_stdout = sys.stdout	
	if outputfile != None:
		f = open(outputfile, 'a')
	else:
		f = original_stdout
	sys.stdout = f

	if doGraph:	
		graphBEGIN()
		for frag in fragments:
			frag.emitBlock()
		for frag in fragments:
			frag.emitTransitions()
		graphEND()
	else:
		for frag in fragments:
			frag.instrumentBlock()
			frag.renderBlock(False)

	# restore	
	sys.stdout = original_stdout 
	if f != None:
		f.close()

