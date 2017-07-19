import math, functools, operator
from common import args

class memoize:
	def __init__(self, function):
		self.function = function
		self.cache = {}
	def __call__(self, *args, **kwargs):
		key = tuple(args) + (undict(kwargs),)
		try:
			if key in self.cache:
				return self.cache[key]
		except:
			pass # probably unhashable
		result = self.function(*args, **kwargs)
		try:
			self.cache[key] = result
		except:
			pass # probably unhashable... again
		return result

def undict(m):
	return tuple(sorted([(a, m[a]) for a in m], key = lambda e: e[0]))

def constant(value):
	return lambda stack: stack.push(value)

def _(function):
	return lambda stack: stack.push(function(stack.pop()))

@memoize
def toInt(x):
	return int(abs(x) * (1 if x > 0 else -1))

@memoize
def sign(x):
	return 1 if x > 0 else -1 if x < 0 else 0

@memoize
def digits(x, base = 10):
	x = toInt(x)
	d = []
	while x >= 1:
		d.insert(0, x % base)
		x //= base
	return d

@memoize
def digitify(base):
	return lambda x: digits(x, base)

def vrange(x):
	return x if type(x) == list else list(range(sign(x), toInt(x), sign(x) or 1)) + [toInt(x)]

def vdigit(x):
	return x if type(x) == list else digits(x)

def vrange_(function):
	return _(lambda x: function(vrange(x)))

def vdigit_(function):
	return _(lambda x: function(vdigit(x)))

def __(function):
	return lambda stack: stack.push(function(stack.pop(), stack.pop()))

def ___(function):
	return lambda stack: stack.push(function(stack.pop(), stack.pop(), stack.pop()))

def v_(function):
	return _(vectorize(function))

def v__(function):
	return __(vectorize(function))

def v___(function):
	return ___(vectorize(function))

def all_(function):
	return lambda stack: stack.push(function(stack.popall()))

def vectorize(function):
	return lambda x: list(map(function), x) if type(x) == list else function(x)

def vectorizeLeft(function):
	return lambda x, y: [function(k, y) for k in x] if type(x) == list else function(x, y)

def vectorizeRight(function):
	return lambda x, y: [function(x, k) for k in y] if type(y) == list else function(x, y)

def vectorizeBoth(function):
	return vectorizeLeft(vectorizeRight(function))

@memoize
def Pi(number):
	return math.gamma(number + 1)

@memoize
def flatten(value):
	if type(value) == list and any(type(v) == list for v in value):
		res = []
		for v in value:
			if type(v) == list:
				for k in flatten(v):
					res.append(k)
			else:
				res.append(v)
		return flatten(res)
	else:
		return value

@memoize
def increments(array):
	return [array[i] - array[i - 1] for i in range(1, len(array))]

functions = {
	'!': v_(Pi),
	'B': v_(digitify(2)),
	'D': v_(digitify(10)),
	'F': _(flatten),
	'L': _(len),
	'H': v_(lambda x: x / 2),
	'R': v_(lambda x: list(range(sign(x), toInt(x), sign(x) or 1)) + [toInt(x)]),
	'W': _(lambda x: [x]),
	'f': __(lambda x, y: [k for k in vdigit(x) if k not in vdigit(y)]),
	'ḟ': __(lambda x, y: [k for k in vdigit(x) if k in vdigit(y)]),
	'w': all_(lambda x: x),
	'⊹': lambda stack: stack.push(*stack.pop()),
	'‥': __(lambda x, y: list(range(toInt(x), toInt(y), sign(toInt(y) - toInt(x)) or 1)) + [toInt(y)]),
	'…': ___(lambda x, y, z: list(range(toInt(x), toInt(y), toInt(z))) + [toInt(y)]),
	'¹': lambda stack: stack.push(stack.pop()), # TODO this is useless in stack-based languages
	'²': _(lambda x: vectorizeBoth(operator.mul)(x, x)),
	'³': constant(args[0]),
	'⁴': constant(args[1]),
	'⁵': constant(args[2]),
	'⁶': constant(args[3]),
	'⁷': constant(args[4]),
	'⁸': constant(args[5]),
	'⁹': constant(args[6]),
	'₁': vdigit_(lambda x: x[0]),
	'₂': vdigit_(lambda x: x[1]),
	'₃': vdigit_(lambda x: x[2]),
	'₄': vdigit_(lambda x: x[3]),
	'₅': vdigit_(lambda x: x[4]),
	'₆': vdigit_(lambda x: x[5]),
	'₇': vdigit_(lambda x: x[6]),
	'₈': vdigit_(lambda x: x[7]),
	'₉': vdigit_(lambda x: x[-1]),
	'π': constant(math.pi),
	'τ': constant(math.pi * 2),
	'ϕ': constant(.5+5**.5*.5),
	'+': v__(operator.add),
	'_': v__(operator.sub),
	'⨉': v__(operator.mul),
	'*': v__(operator.pow),
	'∏': _(lambda x: functools.reduce(operator.mul, vrange(x))),
	'Σ': _(lambda x: functools.reduce(operator.add, vrange(x))),
	'Δ': vdigit_(increments)
}
