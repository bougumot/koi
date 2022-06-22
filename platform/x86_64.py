# Static instrumentatin methods for x86_64:

def instrument_x86_64(line_from, line_to):
		insBlock = list()
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
		return insBlock
