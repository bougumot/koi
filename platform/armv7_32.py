# Static instrumentation methods for ARMv7_32:
import config

def getHi(val):
	return int((int(val) >> 16) & 0xffff)

def getLo(val):
	return int(int(val) & 0xffff)
	

def instrument(line_from, line_to, tid):
		insBlock = list()
		# Start frame
		insBlock.append("\tpush\t{r0, r1, r2} // INS\n")

		insBlock.append("\tmovw\tr0,#"+str(getLo(tid))+" // INS\n")
		insBlock.append("\tmovt\tr0,#"+str(getHi(tid))+" // INS\n")

		insBlock.append("\tmovw\tr1,#"+str(getLo(line_to))+" // INS\n")
		insBlock.append("\tmovt\tr1,#"+str(getHi(line_to))+" // INS\n")

		insBlock.append("\tmovw\tr2,#"+str(getLo(line_from))+" // INS\n")
		insBlock.append("\tmovt\tr2,#"+str(getHi(line_from))+" // INS\n")

		insBlock.append("\tbl\ti"+config.koi_prefix+"__koi_covdump // INS\n")
	
		insBlock.append("\tpop\t{r0, r1, r2} // INS\n")

		return insBlock
