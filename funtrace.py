#!/usr/bin/env python

import sys
import os
import string
import re

funcs = []

ignor_calls = '__stack_chk_fail,__strcat_chk,__strcpy_chk,__sprintf_chk,__strrchr_chk,__memcpy_chk'\
'strlen,__strlen_chk,printf,__errno,__strchr_chk,__strncpy_chk'

class funcNode:
	def __init__(self, name, aname):
		self.__mName = name
		self.__altName = aname
		self.__mCallee = set()
		self.mCallers = 0;

	def addCallee(self, callee):
		self.__mCallee.add(callee)

	def getCalleeList(self):
		return self.__mCallee.copy()

	def getName(self):
		return [self.__mName, self.__altName]

	def incCaller(self):
		self.mCallers += 1;

	def callers(self):
		return self.mCallers;

'''
example of function declaration
;; Function const uint8_t* getCharbitmap480(char, uint32_t*, uint32_t*) (_Z16getCharbitmap480cPjS_, funcdef_no=23, decl_uid=6855, cgraph_uid=23)
'''
def addFunc(line):
	'''''found a new funcation.'''
	fs = 12
	fe = line.index(')') + 1
	fun = line[fs:fe]

	ans = line.rindex('(') + 1
	ane = line.find(',', ans)
	altname = line[ans:ane]
	return [fun, altname]

def getNodeByName(nodeList, name):
	for node in nodeList:
		if cmp(name, node.getName()[0]) == 0:
			return node
	return 0

def getNodeByaltName(nodeList, name):
	for node in nodeList:
		if cmp(name, node.getName()[1]) == 0:
			return node
	return 0

def getFunList(files):
	filep = open(files)
	fundef = ';; Function'
	print 'Functions List at ' + files
	for line in filep:
		if line.find(fundef) == 0:
			name = addFunc(line)
			print '\t' + name[0] + '\t' + name[1]
			n = funcNode(name[0], name[1])
			funcs.append(n)
	filep.close()

'''
example format of call_insn
(call_insn 22 21 23 4 (parallel [
            (set (reg:SI 0 r0)
                (call (mem:SI (symbol_ref:SI ("uevent_kernel_multicast_recv") [flags 0x41]  <function_decl 0x2b003cf7d500 uevent_kernel_multicast_recv>) [0 uevent_kernel_multicast_recv S4 A32])
                    (const_int 0 [0])))
            (use (const_int 0 [0]))
            (clobber (reg:SI 14 lr))
        ]) frameworks/av/cmds/camerad/cameraserver.cpp:590 -1
     (nil)
    (expr_list:REG_CFA_WINDOW_SAVE (use (reg:SI 2 r2))
        (expr_list:REG_CFA_WINDOW_SAVE (use (reg:SI 1 r1))
            (expr_list:REG_CFA_WINDOW_SAVE (use (reg:SI 0 r0))
                (nil)))))
'''
def parafile(files):
	'''''paras input file.'''

	print '\nFunctions call map at ' + files
	insn='(call_insn'
	fundef = ';; Function'
	filep = open(files)
	incall = 0;
	parten1 = re.compile('.*\("(\S+)"\)')
	parten2 = re.compile('.*function_decl\s+\w+\s+(.+)>')
	iline=0
	funcnod=0
	for line in filep:
		iline+=1
		if line.find(fundef) == 0:
			name = addFunc(line)
			funcnod = getNodeByName(funcs, name[0])
			print '\t Function::' + name[0]

		incall = line.find(insn)

		if (line.find('function_decl') > 0) and (line.find('symbol_ref') > 0):
			m = parten1.match(line)
			fname = m.group(1)
			calleenod = getNodeByaltName(funcs, fname)
			if calleenod == 0:
#				m = parten2.match(line)
#				fname = m.group(1)
				if ignor_calls.find(fname) < 0:
					calleenod = funcNode(fname, fname)
					print  '\t\t --> ' + str(iline) + '::N::' + fname
					# funcnod.addCallee(calleenod)
			else:
				print  '\t\t --> ' + str(iline) + '::Y::' + calleenod.getName()[0]
				funcnod.addCallee(calleenod)
				calleenod.incCaller()

	filep.close()

def buildDotFile(func_list):
	header = 'digraph callgraph {\n'
	ender  = '}\n'
	color = '[style = "filled",color="red"]\n'

	output = open('./funtrace.dot', 'w')
	output.write(header)
	lines = 0;
	for node in func_list:
		if node.callers() == 0 and len(node.getCalleeList()) > 0:
			output.write('"' + node.getName()[0] + '"' + color)

		for callee in node.getCalleeList():
			print node.getName()[0] + '->' + callee.getName()[0]
			output.write('"' + node.getName()[0] + '" -> "' + callee.getName()[0] + '"\n')
			lines += 1
	print "have written (%d) lines" % (lines)
	output.write(ender)
	output.close()

def main(argv):
	for filename in sys.argv[1:]:
		getFunList(filename)

	print '\nFunctions found ' + str(len(funcs))

	for filename in sys.argv[1:]:
		parafile(filename);

	buildDotFile(funcs)

if __name__ == '__main__':
	main(sys.argv)


