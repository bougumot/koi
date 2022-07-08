# Static instrumentation methods for ARMv7_32:

def getHi(val):
	return int((int(val) >> 16) & 0xffff)

def getLo(val):
	return int(int(val) & 0xffff)
	

def instrument(line_from, line_to, tid):
		insBlock = list()
		# Start frame
		insBlock.append("\tpush\t{r0, r1, r2} // INS\n")

		insBlock.append("\tldr r0, __koi_id")
		insBlock.append("\tmovw\t[r0],#"+str(getLo(tid))+" // INS\n")
		insBlock.append("\tmovt\t[r0],#"+str(getHi(tid))+" // INS\n")

		insBlock.append("\tldr r0, __koi_to")
		insBlock.append("\tmovw\t[r0],#"+str(getLo(line_to))+" // INS\n")
		insBlock.append("\tmovt\t[r0],#"+str(getHi(line_to))+" // INS\n")

		insBlock.append("\tldr r0, __koi_from")
		insBlock.append("\tmovw\[r0],#"+str(getLo(line_from))+" // INS\n")
		insBlock.append("\tmovt\t[r0],#"+str(getHi(line_from))+" // INS\n")

		insBlock.append("\tbl\t__koi_covdump // INS\n")
	
		insBlock.append("\tpop\t{r0, r1, r2} // INS\n")

		return insBlock
