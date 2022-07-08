# Static instrumentatin methods for x86_64:

def instrument(line_from, line_to, tid):
		insBlock = list()
		insBlock.append("\tpushq\t%rbp ## INS\n")
		insBlock.append("\tpushq\t%rdi ## INS\n")
		insBlock.append("\tpushq\t%rsi ## INS\n")

		insBlock.append("\tpushq\t%rax ## INS\n")
		insBlock.append("\tpushq\t%rdx ## INS\n")
		insBlock.append("\tpushq\t%rcx ## INS\n")
	
		insBlock.append("\tpushfq\t ## INS\n")

		insBlock.append("\tmovq	___koi_from@GOTPCREL(%rip), %rcx\n")
		insBlock.append("\tmovl\t$"+str(line_from)+",(%rcx)  ## INS\n")
		
		insBlock.append("\tmovq	___koi_to@GOTPCREL(%rip), %rcx\n")
		insBlock.append("\tmovl\t$"+str(line_to)+", (%rcx) ## INS\n")
		
		insBlock.append("\tmovq	___koi_id@GOTPCREL(%rip), %rcx\n")
		insBlock.append("\tmovl\t$"+str(tid)+", (%rcx)## INS\n")
		
		insBlock.append("\tcallq\t___koi_covdump ## INS\n")
		insBlock.append("\tpopfq\t ## INS\n")
		
		insBlock.append("\tpopq\t%rcx ## INS\n")
		insBlock.append("\tpopq\t%rdx ## INS\n")
		insBlock.append("\tpopq\t%rax ## INS\n")
	
		insBlock.append("\tpopq\t%rsi ## INS\n")
		insBlock.append("\tpopq\t%rdi ## INS\n")
		insBlock.append("\tpopq\t%rbp ## INS\n")
		return insBlock
