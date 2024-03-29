#!/usr/bin/python3
	
import sys, getopt
import os.path
import re
import platform.platform as platform
	
from ins_blocks import CodeBlock
from ins_graphs import *

doGraph = None
total_transitions = 0;

if __name__ == "__main__":
	inputfile = 'input.S'
	outputfile = None
	trans_name = None
	tid = 0

	try:
		opts, args = getopt.getopt(sys.argv[1:],"hi:o:gvs:t:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('USAGE: -i <inputfile> -o <outputfile> -s <starting transition ID>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('USAGE: -i <inputfile> -o <outputfile> -s <starting transition ID>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
			lstfile = arg.replace(".S", ".ins.lst")
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in '-s':
			tid = int(arg)
		elif opt == '-g':
			doGraph = True
		elif opt == '-t':
			if os.path.exists(arg):
				trans_name = arg
		elif opt == '-v':
			print('Input file is ', inputfile)
			if outputfile is not None:
				print('Output file is ', outputfile)
			else:
				print('Using stdout')
	
	tid += 1
	
	# Get function body
	lines = []
	with open(inputfile) as f:
		lines = f.readlines()
	f.close()
	
	line_count = 0
	block_count = 0;
	
	fragments = [] # An empty list for code fragments
	new_frag = CodeBlock(block_count, "__FIRST_BLOCK", line_count);

	functions_dict = {} # An empty dictionary of functions:fragments
	if os.path.exists(lstfile):
		with open(lstfile) as f:
			for line in f:
				functions_dict[line.strip()] = [] # Add list
		f.close()
	current_func = None

	# First pass - collect the boxes
	for line in lines:
		line_count += 1
	
		matchlabel = platform.label_mark.search(line)
		matchjump = platform.jump_cmd.search(line)
		if matchlabel:
			# Some labels are just labels... ignore them
			ignored_label = platform.ignored_labels.search(line)
			if ignored_label is None:
				new_frag.closeBlock(line_count - 1)
				fragments.append(new_frag)
				block_count += 1
				new_frag = CodeBlock(block_count, line, line_count)
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

		# Create a func:frags dictionary
		this_label = re.sub(':.*','', frag.label).strip()	
		if functions_dict.get(this_label) is not None:
			current_func = functions_dict.get(this_label)
		if current_func is not None:
			current_func.append(frag) 

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
			
		if (index+1 < len(fragments) and not platform.uncond_jump(subline)):
			lfrom = frag.last_number
			lto = frag.last_number + 1
			frag.stransition = (lfrom, lto)
			if fragments[index + 1].meaningful:
				frag.skip_to_block = fragments[index + 1].lines[0]
			else:
				k = 2
				while (index + k < len(fragments)) and (not fragments[index + k].meaningful):
					k += 1
				if index + k < len(fragments):
					frag.skip_to_block = fragments[index + k].lines[0]
				else:
					frag.stransition = None
	
			matchobj = platform.cond_jump_cmd.search(subline)
			if matchobj:
				frag.fallthru = True
			else:
				fragments[index + 1].ftransition = True

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
			frag.emitBlock(trans_name)
		for frag in fragments:
			frag.emitTransitions(trans_name)
		graphEND()
	else:
		for frag in fragments:
			tid = frag.instrumentBlock(tid)
			frag.renderBlock(False)
			total_transitions += frag.transitionsCount()

	# restore	
	sys.stdout = original_stdout 
	if f != None and f != original_stdout:
		f.close()

if not doGraph:
	print(total_transitions)
else:
	print ("\tFUNCTION COVERAGE AND TRANSITIONS")
	for func in functions_dict:
		print("="*79)
		print(func+" :", end = '')
		covered_lines = 0
		total_lines = 0
		for frag in functions_dict[func]:
			if not frag.meaningful:
       	                 continue
			if frag.covered:
				covered_lines += frag.last_number - frag.first_number
			total_lines += frag.last_number - frag.first_number

		print(str(covered_lines)+"/"+str(total_lines), end = '')
		print("({:.2f})".format(float(covered_lines)/float(total_lines) * 100))
		print("-" * 79)
		print("Type\tFrom\tTo\tStatus")
		has_conditionals = False
		for frag in functions_dict[func]:
			if frag.stransition is not None:
				has_conditionals = True
				print("S\t"+str(frag.stransition[0])+'\t'+str(frag.stransition[1]), end = '')
				if frag.skiped:
					print("\tCOVERED")
				else:
					print("\t---")

			if frag.jtransition is not None:
				has_conditionals = True
				print("J\t"+str(frag.jtransition[0])+'\t'+str(frag.jtransition[1]), end = '')
				if frag.jumped:
					print("\tCOVERED")
				else:
					print("\t---")
		if has_conditionals is False:
			print("\tNO TRANSTIONS")
