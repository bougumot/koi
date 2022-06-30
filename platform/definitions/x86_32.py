import re

#label_mark = re.compile(r'.*(\.L|LBB[0-9]*_)[0-9]+\:')
# A more generic label
label_mark = re.compile(r'^(?!#)[A-Za-z_0-9\.]+\:.*')

jump_cmd = re.compile(r'(jo|jno|js|jns|je|jz|jne|jnz|jb|jnae|jc|jnb|jae|jnc|jbe|jna|ja|jnbe|jl|jnge|jge|jnl|jle|jng|jg|jnle|jp|jpe|jnp|jpo|jcxz|jecxz|jmp).*((\.L|LBB[0-9]*_)[0-9]+)|(ret.*)')

cond_jump_cmd = re.compile(r'(jo|jno|js|jns|je|jz|jne|jnz|jb|jnae|jc|jnb|jae|jnc|jbe|jna|ja|jnbe|jl|jnge|jge|jnl|jle|jng|jg|jnle|jp|jpe|jnp|jpo|jcxz|jecxz).*((\.L|LBB[0-9]*_)[0-9]+)')

cmp_or_jmp_cmd = re.compile(r'(jmp|ret[a-z]*|cmp[a-z]*[ \t]+.*|test[a-z]*[ \t]+.*)')

line_address = re.compile(r'^[ ]*([0-9]+)[ ]*.*')

meaningles = re.compile(r'^[ \t]*(#.*|.*\..*|.*:.*|$)')

ignored_labels = re.compile(r'^.(LFB[0-9]*|LBB[0-9]*):.*')

def uncond_jump(subline):
	if "jmp" in subline or "ret" in subline:
		return True
	else:
		return False
