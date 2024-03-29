# vi: set ts=4
# The code block abstraction

import html
import re
import platform.platform as platform

cov_report_line = re.compile(r'^([0-9]*)::([0-9]*):([0-9]*);\[([0-9]*)\].*')

def lines_that_contain(string, fp):
	if fp is None:
		return None
	fp.seek(0)
	arr = [line for line in fp if string in line]
	if len(arr) == 0:
		return None
	else:
		return arr

class CodeBlock:
	def __init__(self, index, label, first_line_number):
		self.lines = list()
		self.lines.append("state"+str(index))
		self.label = label
		self.index = index
		self.first_number = first_line_number
		self.last_number = 0
		self.covered = False
		self.meaningful = False
		self.jtransition = None
		self.stransition = None
		self.ftransition = False
		self.fallthru = False
		self.jumped = False
		self.skiped = False
		self.transitions_count = 0

	def addLine(self, line, count):
		match = platform.meaningles.search(line)
		if not match:
			self.meaningful = True
		self.lines.append(str(count)+line)

	def closeBlock(self, line_number):
		self.last_number = line_number			

	def instrumentBlock(self, tid):
		base_tid = tid
		if "__koi_covdump" in self.label: # do not instrument the instrumenter
			return tid
		if not self.meaningful:
			return tid
		if len(self.lines) == 1:
			return tid

		if self.jtransition: # A conditional block case of jump
			if len(self.lines) == 2: # a special case of single jump
				self.lines[1:1] = platform.asm.instrument(self.jtransition[0], self.jtransition[1], tid)
				tid += 1
			else:
				self.ftransition = False
				self.lines[2:2] = platform.asm.instrument(self.first_number, 0, tid)
				tid += 1
				self.lines[-1:-1] = platform.asm.instrument(self.jtransition[0], self.jtransition[1], tid)
				tid += 1

		if self.stransition: # A conditional block case of skip, head is already set by jump case
			if self.ftransition:
				self.lines[2:2] = platform.asm.instrument(self.first_number, 0, tid)
				tid += 1

			self.lines.extend(platform.asm.instrument(self.stransition[0], self.stransition[1], tid))
			tid += 1

		elif not self.jtransition: # A closed block, (function ?)
			self.lines[2:2] = platform.asm.instrument(self.first_number, 0, tid)
			tid += 1
			self.lines[-1:-1] = platform.asm.instrument(self.last_number, -1, tid)
			tid += 1
		self.transitions_count = tid - base_tid
		return tid

	def transitionsCount(self):
		return self.transitions_count

	def emitBlock(self, cov_file):
		if len(self.lines) == 1:
			return
		if self.meaningful == False:
			return

		fp = None
		if cov_file is not None:
			fp = open(cov_file)

		if lines_that_contain("::"+str(self.first_number)+":0", fp) is not None or lines_that_contain(":"+str(self.first_number)+";", fp) is not None:
			color = "green"
			self.covered = True
		else:
			color = "gray"

		block_t = 0
		lines = lines_that_contain("::"+str(self.first_number)+":0", fp)
		if lines is not None:
			# Get temperature value
			matchobj = cov_report_line.search(lines[0])
			if matchobj is not None:
				block_t = matchobj.group(4)

		if lines_that_contain("::"+str(self.last_number)+":", fp) is None and color != "gray":
			color = "brown"

		print("\"state"+str(self.index)+"\"","[ style = \"filled\" penwidth = 1 fillcolor = \"white\" fontname = \"Courier New\" shape = \"Mrecord\" label =<<table border=\"0\" cellborder=\"0\" cellpadding=\"3\" bgcolor=\"white\"><tr><td bgcolor=\"black\" align=\"center\" colspan=\"2\"><font color=\"white\">", self.label + ", T = " + str(block_t), "</font></td></tr>", end = '')
		for line in self.lines[1:]:
			print("<tr><td align=\"left\" port=\"r5\">","<font color=\""+color+"\">", html.escape(line.strip().replace("}","\}").replace("{","\{").replace("\t","    ")),"</font></td></tr>", end = '')

		print("</table>> ];")

	def emitTransitions(self, cov_file):
		fp = None
		if cov_file is not None:
			fp = open(cov_file)

		if self.stransition:
			color = "gray"
			if lines_that_contain("::"+str(self.stransition[0])+":"+str(self.stransition[1]), fp) is not None:
				color = "black"
				self.skiped = True
			else:
				color = "red"
			print(self.lines[0], "->", self.skip_to_block, "[ penwidth = 5 fontsize = 28 fontcolor = \""+color+"\" label = ", end = '')
			if self.fallthru:
				print("\"SKIP " + str(self.stransition[0]) + " -> " + str(self.stransition[1]) + "\"]")
			else:
				print("\"FALL " + str(self.stransition[0]) + " -> " + str(self.stransition[1]) + "\"]")

		if self.jtransition:
			color = "gray"
			if lines_that_contain("::"+str(self.jtransition[0])+":"+str(self.jtransition[1]), fp) is not None:
				color = "black"
				self.jumped = True
			else:
				color = "red"
			print(self.lines[0], " -> ", self.jump_to_block ,"[ penwidth = 5 fontsize = 28 fontcolor = \"" + color + "\" label = \"JUMP " + str(self.jtransition[0]) + " -> "+ str(self.jtransition[1]) + "\"]")

	def renderBlock(self, show_lines):
		for line in self.lines[1:]:
			if show_lines:
				print(line, end = '')
			else:
				print(re.sub(r'^\d+ ?', '', line, re.MULTILINE), end = '')

# End of file
