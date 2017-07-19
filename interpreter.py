import sys, re, functions
from common import args

code_page  = '''¹²³⁴⁵⁶⁷⁸⁹₁₂₃₄₅₆₇₈₉∃∄∀..þÞÆæŒœıȷ !"#$%&\'()*+,-./0123456789:;<=>?'''
code_page += '''@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~‥'''
code_page += '''…⊹∏Σπτϕ⨉Δ¶∑√....................................................'''
code_page += '''.............................................................‷“”'''

escapes    = '''¹²³⁴⁵⁶⁷⁸⁹₁₂₃₄₅₆₇₈₉∃∄∀..þÞÆæŒœıȷ !"#$%&\'()*+,-./0123456789:;<=>?'''
escapes   += '''@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`a\bcdefghijklm\nopq\rs\tuvwxyz{|}~‥'''
escapes   += '''…⊹∏Σπτϕ⨉Δ¶∑.....................................................'''
escapes   += '''.............................................................‷“”'''

code = ''

if sys.argv[1:]:
	with open(sys.argv[1], 'r') as f:
		code = f.read().replace('\n', '¶')
	args[:len(sys.argv) - 2] = list(map(int, sys.argv[2:]))
else:
	code = input().replace('\n', '¶')

index = 0

def parseNumber(string, default = 0):
	if 'ȷ' in string:
		left, right = tuple(string.split('ȷ'))
		return parseNumber(left, 1) * 10 ** parseNumber(right, 3)
	elif 'ı' in string:
		left, right = tuple(string.split('ı'))
		return parseNumber(left, 0) + parseNumber(right, 1) * 1j
	elif string == '-':
		return -1
	elif string == '.':
		return 0.5
	elif string == '-.':
		return -0.5
	elif string.endswith('.'):
		return float(string) + 0.5
	elif string:
		return float(string)
	else:
		return default

def ORD(chr):
	if chr in code_page:
		return code_page.find(chr)
	else:
		return ord(chr)

def tokenize(code):
	index = 0
	tokens = []
	while index < len(code):
		if code[index] in '0123456789-.ıȷ':
			decimals = code[index] == '.'
			rcurrent = code[index]
			specials = code[index] in 'ıȷ'
			newliter = code[index] in 'ıȷ'
			index   += 1
			while index < len(code) and (code[index] in '0123456789' or code[index] == '.' and not decimals or code[index] in '-.' and newliter or code[index] in 'ıȷ' and not specials):
				specials |= code[index] in 'ıȷ'
				newliter = code[index] in 'ıȷ'
				decimals |= code[index] in '.ȷ'
				rcurrent += code[index]
				index += 1
			tokens.append(('literal', parseNumber(rcurrent)))
		elif code[index] == "”":
			index += 1
			tokens.append(('literal', ORD(code[index])))
			index += 1
		elif code[index] == '\\':
			index += 1
			tokens.append(('literal', ORD(escapes[code_page.find(code[index])])))
			index += 1
		elif code[index] == '"':
			index += 1
			tokens.append(('literal', [ORD(code[index]), ORD(code[index + 1])]))
			index += 2
		elif code[index] == '‷':
			index += 1
			tokens.append(('literal', [ORD(code[index]), ORD(code[index + 1]), ORD(code[index + 2])]))
			index += 3
		elif code[index] == '“':
			index += 1
			strings = []
			backslash = False
			hashmode = False
			while True:
				if code[index] == '“':
					if not strings or type(strings[0]) != list:
						strings = [strings, []]
					else:
						strings.append([])
				elif code[index] == '”':
					index += 1
					break
				elif backslash:
					(strings if not strings or type(strings[0]) != list else strings[-1]).append(ORD(escapes[code_page.find(code[index])]))
					backslash = False
				elif code[index] not in '\\':
					if code[index] == '#':
						decimals = code[index] == '.'
						rcurrent = code[index]
						specials = code[index] in 'ıȷ'
						index   += 1
						while index < len(code) and (code[index] in '0123456789' or code[index] == '.' and not decimals or code[index] in 'ıȷ' and not specials):
							specials |= code[index] in 'ıȷ'
							decimals |= code[index] in '.ȷ'
							rcurrent += code[index]
							index += 1
						(strings if not strings or type(strings[0]) != list else strings[-1]).append(parseNumber(rcurrent[1:]))
						index -= 1
					else:
						(strings if not strings or type(strings[0]) != list else strings[-1]).append(ORD(code[index]))
				else:
					backslash = True
				index += 1
			tokens.append(('literal', strings))
		elif code[index] == '‴':
			string = ''
			backslash = False
			for i in range(index):
				if backslash:
					string += escapes[code_page.find(code[i])]
					backslash = False
				elif code[i] == '\\':
					backslash = True
				else:
					string += code[i]
			tokens = [('literal', list(map(ORD, string)))]
			index += 1
		elif code[index] in '∑∃∄∀þÞ':
			tokentype = ['sum', 'exists', 'existsnot', 'map', 'sort', 'sortdyad']['∑∃∄∀þÞ'.find(code[index])]
			inner = ''
			index += 1
			brackets = 1
			while brackets and index < len(code):
				if code[index] in '∑∃∄∀þÞ':
					brackets += 1
				elif code[index] in '}':
					brackets -= 1
				if brackets:
					inner += code[index]
				index += 1
			tokens.append((tokentype, tokenize(inner)))
		elif code[index] in 'ÆæŒœ':
			tokens.append(('operator', code[index:index + 2]))
			index += 2
		else:
			tokens.append(('operator', code[index]))
			index += 1
	return tokens

class Stack:
	def __init__(self):
		self.stack = []
		self.argindex = 0
	def index(self):
		self.argindex += 1
		return self.argindex - 1
	def reset(self):
		self.argindex = 0
	def push(self, *values):
		for value in values:
			self.stack.append(value)
		return self
	def pushItem(self, value):
		self.stack.append(value)
		return value
	def pop(self):
		return self.stack.pop() if self.stack else args[self.index()]
	def rmtop(self):
		if self.stack: self.stack.pop()
		else: self.argindex += 1
		return self
	def clear(self):
		self.stack = []
		return self
	def popall(self):
		array = self.stack
		self.stack = []
		return array
	def peek(self):
		return self.stack[-1]
	def peekall(self):
		return self.stack[:]

def evaluate(tokens, stack = Stack()):
	for token in tokens:
		if token[0] == 'literal':
			stack.push(token[1])
		elif token[0] == 'operator' and token[1] not in ' ¶':
			functions.functions[token[1]](stack)
			stack.reset()
		elif token[0] == 'sum':
			values = []
			value = vrange(stack.pop())
			stack.reset()
			for val in value:
				values.append(evaluate(inner, Stack(stack.stack + [val])))
		elif token[0] == 'exists':
			value = vrange(stack.pop())
			stack.reset()
			for val in value:
				if evaluate(inner, Stack(stack.stack + [val])):
					stack.push(1)
					break
			stack.push(0)
		elif token[0] == 'existsnot':
			value = vrange(stack.pop())
			stack.reset()
			for val in value:
				if evaluate(inner, Stack(stack.stack + [val])):
					stack.push(0)
					break
			stack.push(1)
	return stack.stack.pop() if stack.stack else None

output = evaluate(tokenize(code))
print('' if output == None else output)
