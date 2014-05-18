# Andrew Duryea
# March 2014
# docGen.py
#
# This program generates documentation from comments.
# For instance:
# 	/* foo - a function
#		@param {number} param1 - a parameter
#		@param {string} param2 - another parameter
#		@returns {boolean} whatever this function returns
#	*/
#
# Would produce:
#	public foo(param1, param2)
#		Description: a function
#		Parameters:
#			param1
#				Type {number}
#				a parameter
#			param2
#				Type {string}
#				another parameter
#		Returns a boolean
#			whetever this function returns
#	
#	@returns is optional
#	Any string can be put inside the brackets for a parameter/return type.
#	
#	The file to process is passed as a command line argument to the program

import re
import sys

#the function class	
class Function:
	#the constructor
	def __init__(self, public, name, desc, params, returns):
		self.public = public
		self.name = name
		self.desc = desc
		self.params = params
		
		#set up the parameter arrays
		#@param {DOM object} cell - the initial cell
		#@param {object} values - an array of object
		self.paramNames = []
		self.paramTypes = []
		self.paramDescs = []
		self.noParams = False
		if params != 'none':
			for p in self.params:
				halves = p.split('-')
				self.paramNames.append(halves[0].split('}')[1].strip())
				typeMatch = re.compile('\{.*\}').search(halves[0])
				self.paramTypes.append(typeMatch.group())
				self.paramDescs.append(halves[1].strip())
		else:
			self.noParams = True
		
		#@returns {string} the string representation of the row
		self.returnType = ''
		self.returnDesc = ''
		if returns != 'nothing':
			returnHalves = returns.split('}')
			self.returnType = returnHalves[0].split()[1].strip('{')
			self.returnDesc = returnHalves[1].strip()
		else:
			self.returnType = 'nothing'
	
	#returns a string describing the function
	def toString(self):
		if public:
			returnStr = 'public '
		else:
			returnStr = 'private '
		
		returnStr += self.name + '('
		#add all the params after the function name
		if not self.noParams:
			for i in range(0,len(self.paramNames)-1):
				returnStr += self.paramNames[i] + ", "
			returnStr += self.paramNames[len(self.paramNames)-1] + ')\n'
		else:
			returnStr += ')\n'
		
		returnStr += '\tDescription: ' + self.desc + '\n'
		
		#add the params and descriptions
		if not self.noParams:
			returnStr += '\tParameters:\n'
			for i in range(0,len(self.paramNames)):
				returnStr += '\t\t' + self.paramNames[i] + '\n'
				returnStr += '\t\t\tType: ' + self.paramTypes[i] + '\n'
				returnStr += '\t\t\t' + self.paramDescs[i]+'\n'
		else:
			returnStr += '\ttakes no Parameters\n'
		
		if self.returnType != 'nothing':
			returnStr += '\tReturns a ' + self.returnType + '\n'
			returnStr += '\t\t' + self.returnDesc + '\n'
		else:
			returnStr += '\tReturns nothing\n'
		
		return returnStr

filename = ''

if len(sys.argv) <= 1:
	print("Please specify a file to process as a command line argument.")
	exit()
elif len(sys.argv) <=2:
	filename = sys.argv[1]
else:
	print("Please only specify a single file to process.")
	exit()

#open the file
F = open(filename)
#put the file into a string?
str = F.read()

#get a list of public functions
publicRE = re.compile('this\..*;')
publicFuncs = [x.split('=')[1].strip(' ;') for x in publicRE.findall(str)]

#match this: "/*...*/"
regex = re.compile('[\t]*/\* .*? - .*?\*/',re.DOTALL)
matches = regex.findall(str)
#print('Raw text: ', end='')
#print(matches)

#print the number of matches (ie the number of functions)
print('Number of funcitons: ', end='')
print(len(matches))

nameRE = re.compile('^/\* .*? -')
descRE = re.compile(' - .*')
paramsRE = re.compile('@param.*')
returnsRE = re.compile('@returns .*')

for m in matches:
	nameMatch = nameRE.search(m.strip('\t'))
	funcName = ''
	if nameMatch:
		funcName = nameMatch.group().split()[1]
	else:
		funcName = "N/A"
	
	public = False
	if funcName in publicFuncs or m.find('\t') != 0:
		public = True

	descMatch = descRE.search(m)
	funcDesc = ''
	if descMatch:
		funcDesc = descMatch.group().split('-')[1].strip()
	else:
		funcDesc = "N/A"

	paramsMatch = paramsRE.findall(m)
	funcParams = []
	if len(paramsMatch) > 0:
		funcParams = paramsMatch
	else:
		funcParams = "none"

	returnsMatch = returnsRE.search(m)
	funcReturns = ''
	if returnsMatch:
		funcReturns = returnsMatch.group()
	else:
		funcReturns = "nothing"

	func = Function(public, funcName, funcDesc, funcParams, funcReturns)
	print(func.toString())
