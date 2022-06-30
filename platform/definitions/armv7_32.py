import re

#label_mark = re.compile(r'.*(\.L|LBB[0-9]*_)[0-9]+\:')
# A more generic label
label_mark = re.compile(r'^(?!//)[A-Za-z_0-9\.]+\:.*')

jump_cmd = re.compile(r'(beq|bne|bcs|bcc|bmi|bpl|bvs|bvc|bhi|bls|bge|blt|bgt|ble|bal|b[ \t]*).*((\.L|LBB[0-9]*_)[0-9]+)|(b[a-z]*[ \t]*lr)|(pop[ \t]*\{.*pc.*\})')

cond_jump_cmd = re.compile(r'(beq|bne|bcs|bcc|bmi|bpl|bvs|bvc|bhi|bls|bge|blt|bgt|ble|bal).*((\.L|LBB[0-9]*_)[0-9]+)')

cmp_or_jmp_cmd = re.compile(r'(b[ \t].*|b[a-z]*[ \t]*lr|pop[ \t]*\{.*pc.*\}|cmp[a-z]*[ \t]+.*)')

__unc_jump = re.compile(r'(b[ \t]*.*|b[a-z]*[ \t]*lr|pop[ \t]*\{.*pc.*\})')

line_address = re.compile(r'^[ ]*([0-9]+)[ ]*.*')

meaningles = re.compile(r'^[ \t]*(//.*|.*\..*|.*:.*|$)')

ignored_labels = re.compile(r'^.(LFB[0-9]*|LBB[0-9]*):.*')


def uncond_jump(subline):
	matchobj = __unc_jump.search(subline)
	if matchobj is not None:
		return True
	else:
		return False
