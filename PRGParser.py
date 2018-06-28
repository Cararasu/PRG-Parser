#!/usr/bin/python3

import binascii
import sys

decode_char = [
    u'\uFFFD',u'\uFFFD',u'\uFFFD',u'\uFFFD',u'\uFFFD',u'\uF100',u'\uFFFD',u'\uFFFD',u'\uF118',u'\uF119',u'\uFFFD',u'\uFFFD',u'\uFFFD',u'\u000D',u'\u000E',u'\uFFFD',
    u'\uFFFD',u'\uF11C',u'\uF11A',u'\uF120',u'\u007F',u'\uFFFD',u'\uFFFD',u'\uFFFD',u'\uFFFD',u'\uFFFD',u'\uFFFD',u'\uFFFD',u'\uF101',u'\uF11D',u'\uF102',u'\uF103',
    u'\u0020',u'\u0021',u'\u0022',u'\u0023',u'\u0024',u'\u0025',u'\u0026',u'\u0027',u'\u0028',u'\u0029',u'\u002A',u'\u002B',u'\u002C',u'\u002D',u'\u002E',u'\u002F',
    u'\u0030',u'\u0031',u'\u0032',u'\u0033',u'\u0034',u'\u0035',u'\u0036',u'\u0037',u'\u0038',u'\u0039',u'\u003A',u'\u003B',u'\u003C',u'\u003D',u'\u003E',u'\u003F',
    u'\u0040',u'\u0061',u'\u0062',u'\u0063',u'\u0064',u'\u0065',u'\u0066',u'\u0067',u'\u0068',u'\u0069',u'\u006A',u'\u006B',u'\u006C',u'\u006D',u'\u006E',u'\u006F',
    u'\u0070',u'\u0071',u'\u0072',u'\u0073',u'\u0074',u'\u0075',u'\u0076',u'\u0077',u'\u0078',u'\u0079',u'\u007A',u'\u005B',u'\u00A3',u'\u005D',u'\u2191',u'\u2190',
    u'\u2501',u'\u0041',u'\u0042',u'\u0043',u'\u0044',u'\u0045',u'\u0046',u'\u0047',u'\u0048',u'\u0049',u'\u004A',u'\u004B',u'\u004C',u'\u004D',u'\u004E',u'\u004F',
    u'\u0050',u'\u0051',u'\u0052',u'\u0053',u'\u0054',u'\u0055',u'\u0056',u'\u0057',u'\u0058',u'\u0059',u'\u005A',u'\u253C',u'\uF12E',u'\u2502',u'\u2592',u'\uF139',
	"END", "FOR", "NEXT", "DATA", "INPUT#", "INPUT", "DIM", "READ", 
	"LET", "GOTO", "RUN", "IF", "RESTORE", "GOSUB", "RETURN", "REM",
	"STOP", "ON", "WAIT", "LOAD", "SAVE", "VERIFY", "DEF", "POKE",
	"PRINT#", "PRINT", "CONT", "LIST", "CLR", "CMD", "SYS", "OPEN",
	"CLOSE", "GET", "NEW", "TAB(", "TO", "FN", "SPC(", "THEN",
	"NOT", "STEP", "+", "-", "*", "/", "power", "AND",
	"OR", ">", "=", "<", "SGN", "INT", "ABS", "USR",
	"FRE", "POS", "SQR", "RND", "LOG", "EXP", "COS", "SIN",
	"TAN", "ATN", "PEEK", "LEN", "STR$", "VAL", "ASC", "CHR$",
	"LEFT$", "RIGHT$", "MID$", "GO", u'\u004C',u'\u004D',u'\u004E',u'\u004F',
    u'\u0050',u'\u0051',u'\u0052',u'\u0053',u'\u0054',u'\u0055',u'\u0056',u'\u0057',u'\u0058',u'\u0059',u'\u005A',u'\u253C',u'\uF12E',u'\u2502',u'\u2592',u'\uF139',
    u'\u00A0',u'\u258C',u'\u2584',u'\u2594',u'\u2581',u'\u258F',u'\u2592',u'\u2595',u'\uF12F',u'\uF13A',u'\uF130',u'\u251C',u'\uF134',u'\u2514',u'\u2510',u'\u2582',
    u'\u250C',u'\u2534',u'\u252C',u'\u2524',u'\u258E',u'\u258D',u'\uF131',u'\uF132',u'\uF133',u'\u2583',u'\u2713',u'\uF135',u'\uF136',u'\u2518',u'\uF137',u'\u2592'
    ]

class BasicCommand:
	def __init__(self, label, string, offset=-1, next_offset=-1):
		self.label = label
		self.string = string
		self.offset = offset
		self.next_offset = next_offset
	def __repr__(self):
		return str(self.label) + " " + self.string
	def __str__(self):
		return self.__repr__()

def bytes_to_int(bytes):
	i = 0
	for b in bytes[::-1]:
		i = (i << 8) + b
	return i
def parse_command(line, command_offset = 0x801):
	if len(line) < 4:
		return None
	next_offset = bytes_to_int(line[:2])
	label = bytes_to_int(line[2:4])
	ptr = 4
	string = ""
	while ptr < len(line):
		byte = line[ptr]
		ptr += 1
		if byte == 0x00:
			break
		else:
			string = string + decode_char[byte]
	return (BasicCommand(label, string, command_offset, next_offset), ptr)
	
def parse_all_commands(data, mapped_position = 0x801):
	commands = []
	
	ptr = 0
	while True:
		res = parse_command(data[ptr:], mapped_position + ptr)
		if res == None:
			break
		else:
			ptr += res[1]
			commands.append(res[0])
	return commands
def parse_file(file):
	with open(file, "rb") as f:
		mapped_position_bytes = f.read(2)
		if len(mapped_position_bytes) < 2:
			print("File needs to be at least 2 bytes long")
		mapped_position = bytes_to_int(mapped_position_bytes)
		return (mapped_position, parse_all_commands(f.read(), mapped_position))

if __name__ == "__main__":
	for file in sys.argv[1:]:
		res = parse_file(file)
		print("Program mapped at position 0x%x" % res[0])
		for line in res[1]:
			print(line)
