# vi: set ts=4
# The code block abstraction

import sys
import html
from ins_definitions import *

class CodeBlock:
	def __init__(self, index, label, first_line_number):
		self.lines = list()
		self.lines.append("state"+str(index))
		self.label = label
		self.index = index
		self.first_number = first_line_number
		self.last_number = 0
		self.meaningful = False
		self.jtransition = None
		self.stransition = None
		self.fallthru = False

	def addLine(self, line, count):
		match = meaningles.search(line)
		if not match:
			self.meaningful = True
		self.lines.append(str(count)+line)

	def closeBlock(self, line_number):
		self.last_number = line_number			

	def instrumentBlock(self):
		if "dump" in self.label: # do not instrument the instrumenter
			return
		if not self.meaningful:
			return
		if len(self.lines) == 1:
			return

		if self.jtransition: # A conditional block case of jump
			if len(self.lines) == 2: # a special case of single jump
				self.lines[1:1] = self.addInstrumentation(self.jtransition[0], self.jtransition[1])
			else:
				self.lines[2:2] = self.addInstrumentation(self.first_number, 0)
				self.lines[-1:-1] = self.addInstrumentation(self.jtransition[0], self.jtransition[1])
		if self.stransition: # A conditional block case of skip, head is already set by jump case
			self.lines.extend(self.addInstrumentation(self.stransition[0], self.stransition[1]))

		elif not self.jtransition: # A closed block, (function ?)
			self.lines[2:2] = self.addInstrumentation(self.first_number, 0)
			self.lines[-1:-1] = self.addInstrumentation(self.last_number, -1)

	def emitBlock(self):
		if len(self.lines) == 1:
			return
		if self.meaningful == False:
			return
		print "\"state"+str(self.index)+"\"","[ style = \"filled\" penwidth = 1 fillcolor = \"white\" fontname = \"Courier New\" shape = \"Mrecord\" label =<<table border=\"0\" cellborder=\"0\" cellpadding=\"3\" bgcolor=\"white\"><tr><td bgcolor=\"black\" align=\"center\" colspan=\"2\"><font color=\"white\">", self.label, "</font></td></tr>",# no NL
		for line in self.lines[1:]:
			print "<tr><td align=\"left\" port=\"r5\">", html.escape(line.strip().replace("}","\}").replace("{","\{").replace("\t","    ")),"</td></tr>",

		print "</table>> ];"

	def emitTransitions(self):
		if self.stransition:
			print self.lines[0], "->", self.skip_to_block, "[ penwidth = 5 fontsize = 28 fontcolor = \"black\" label = ",
			if self.fallthru:
				print "\"SKIP " + str(self.stransition[0]) + " -> " + str(self.stransition[1]) + "\"]"
			else:
				print "\"FALL " + str(self.stransition[0]) + " -> " + str(self.stransition[1]) + "\"]"

		if self.jtransition:
	                print self.lines[0], " -> ", self.jump_to_block ,"[ penwidth = 5 fontsize = 28 fontcolor = \"black\" label = \"JUMP " + str(self.jtransition[0]) + " -> "+ str(self.jtransition[1]) + "\"]";
     
	def addInstrumentation(self, line_from, line_to):
		insBlock = list();

		#insBlock.append("\tpushq\t%rsp ## INS\n")
		insBlock.append("\tpushq\t%rbp ## INS\n")
		insBlock.append("\tpushq\t%rdi ## INS\n")
		insBlock.append("\tpushq\t%rsi ## INS\n")

		insBlock.append("\tpushq\t%rax ## INS\n")
		insBlock.append("\tpushq\t%rdx ## INS\n")
		insBlock.append("\tpushq\t%rcx ## INS\n")
	
		insBlock.append("\tpushfq\t ## INS\n")
		insBlock.append("\tmovl\t$"+str(line_from)+", %edi ## INS\n")
		insBlock.append("\tmovl\t$"+str(line_to)+", %esi ## INS\n")
		insBlock.append("\tcallq\t_dump ## INS\n")
		insBlock.append("\tpopfq\t ## INS\n")
		
		insBlock.append("\tpopq\t%rcx ## INS\n")
		insBlock.append("\tpopq\t%rdx ## INS\n")
		insBlock.append("\tpopq\t%rax ## INS\n")
	
		insBlock.append("\tpopq\t%rsi ## INS\n")
		insBlock.append("\tpopq\t%rdi ## INS\n")
		insBlock.append("\tpopq\t%rbp ## INS\n")
		#insBlock.append("\tpopq\t%rsp ## INS\n")

		return insBlock

	def renderBlock(self, show_lines, outfile):
		original_stdout = sys.stdout
		
		if outfile != None:
			f = open(outfile, 'a')
		else:
			outfile = original_stdout
		
    		sys.stdout = f # Change the standard output to the file we created.
		for line in self.lines[1:]:
			if show_lines:
				print line,
			else:
				print re.sub(r'^\d+ ?', '', line, re.MULTILINE),

		sys.stdout = original_stdout 
		if f != None:
			f.close()
# End of file
