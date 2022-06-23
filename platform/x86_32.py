# Static instrumentatin methods for x86_64:

def instrument(line_from, line_to, tid):
		insBlock = list()
		insBlock.append("\tpushl\t%esp ## INS\n")
		insBlock.append("\tpushl\t%ebp ## INS\n")

		#caller-saved
		insBlock.append("\tpushl\t%eax ## INS\n")
		insBlock.append("\tpushl\t%edx ## INS\n")
		insBlock.append("\tpushl\t%ecx ## INS\n")

		insBlock.append("\tpushf\t ## INS\n")	

		# Start frame
		insBlock.append("\tmovl\t%esp, %ebp ## INS\n")

		insBlock.append("\tpushl\t$"+str(tid)+" ## INS\n")
		insBlock.append("\tpushl\t$"+str(line_to)+" ## INS\n")
		insBlock.append("\tpushl\t$"+str(line_from)+" ## INS\n")
		insBlock.append("\tcall\tdump ## INS\n")
		insBlock.append("\taddl\t$12, %esp ## INS\n")	
	
		insBlock.append("\tmovl\t%ebp, %esp ## INS\n")

		insBlock.append("\tpopf\t ## INS\n")

		insBlock.append("\tpopl\t%ecx ## INS\n")
		insBlock.append("\tpopl\t%edx ## INS\n")
		insBlock.append("\tpopl\t%eax ## INS\n")

		insBlock.append("\tpopl\t%ebp ## INS\n")
		insBlock.append("\tpopl\t%esp ## INS\n")
		return insBlock
