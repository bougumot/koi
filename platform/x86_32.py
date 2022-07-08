# Static instrumentatin methods for x86_64:

def instrument(line_from, line_to, tid):
		insBlock = list()
		insBlock.append("\tpushl\t%esp ## INS\n")
		insBlock.append("\tpushl\t%ebp ## INS\n")

		#caller-saved
		insBlock.append("\tpushl\t%eax ## INS\n")
		insBlock.append("\tpushl\t%edx ## INS\n")
		insBlock.append("\tpushl\t%ecx ## INS\n")
		insBlock.append("\tpushl\t%ebx ## INS\n")

		insBlock.append("\tpushf\t ## INS\n")	

		# Start frame
		insBlock.append("\tmovl\t%esp, %ebp ## INS\n")

		insBlock.append("\tmovl\t$"+str(tid)+", __koi_id ## INS\n")
		insBlock.append("\tmovl\t$"+str(line_to)+", __koi_to ## INS\n")
		insBlock.append("\tmovl\t$"+str(line_from)+" __koi_from ## INS\n")
		insBlock.append("\tcall\t__koi_covdump ## INS\n")
	
		insBlock.append("\tmovl\t%ebp, %esp ## INS\n")

		insBlock.append("\tpopf\t ## INS\n")

		insBlock.append("\tpopl\t%ebx ## INS\n")
		insBlock.append("\tpopl\t%ecx ## INS\n")
		insBlock.append("\tpopl\t%edx ## INS\n")
		insBlock.append("\tpopl\t%eax ## INS\n")

		insBlock.append("\tpopl\t%ebp ## INS\n")
		insBlock.append("\tpopl\t%esp ## INS\n")
		return insBlock
