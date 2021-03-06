# O2I.g v1.0, 2021-07-03
# Creat Gaussian input file from output file, powered by Python 3.9
# Written by Zhe Wang, Hiroshima university
# Catch me with wongzit@yahoo.co.jp
# Personal webpage: https://www.wangzhe95.net

# Program information section
print("*******************************************************************************")
print("*                                                                             *")
print("*                                   O 2 I . g                                 *")
print("*                                                                             *")
print("*     =================== Version 1.0 for Source Code ===================     *")
# Choose platform (for packaging)
#print("*     ====================== Version 1.0 for macOS ======================     *")
#print("*     ====================== Version 1.0 for Linux ======================     *")
#print("*     ================ Version 1.0 for Microsoft Windows ================     *")
print("*                           Last update: 2021-07-03                           *")
print("*                                                                             *")
print("*     Create Gaussian input file from output file, developed by Zhe Wang,     *")
print("*     Online document is available from GitHub.                               *")
print("*                                     (https://github.com/wongzit/O2Ig)       *")
print("*                                                                             *")
print("*                             -- Catch me with --                             *")
print("*                         E-mail  wongzit@yahoo.co.jp                         *")
print("*                       Homepage  https://www.wangzhe95.net                   *")
print("*                                                                             *")
print("*******************************************************************************")
print("\nPRESS Ctrl+c to exit the program.\n")

def elementNo (eleNumber):
	element = 'H'
	periodTable = ['Bq', 'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', \
					'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', \
					'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', \
					'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Ym', 'Yb', 'Lu', 'Ha', 'Ta', \
					'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', \
					'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', \
					'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
	element = periodTable[eleNumber]
	return element

# ========================== Read original output file ==========================
print("Please specify the Gaussian output file path:")

# For Unix/Linux OS
fileName = input("(e.g.: /O2I.g/example/DR3b_CS2021.log)\n")
if fileName.strip()[0] == '\'' and fileName.strip()[-1] == '\'':
    fileName = fileName.strip()[1:-1]

# For Microsoft Windows
#fileName = input("(e.g.: C:\\O2I.g\\example\\DR3b_CS2021.log)\n")
#if fileName.strip()[0] == '\"' and fileName.strip()[-1] == '\"':
#    fileName = fileName.strip()[1:-1]

with open(fileName.strip(), 'r',) as output:
	outputFile = output.readlines()

geoFlagStart = 0

for i in range(len(outputFile)):
	if '------' in outputFile[i] and '#' in outputFile[i + 1]:
		routeLine = outputFile[i + 1].strip().lower()
		break

for j in range(len(outputFile)):
	if 'Will use up to ' in outputFile[j]:
		CPUcore = 	outputFile[j].split()[4]
	if '%mem=' in outputFile[j]:
		memory = outputFile[j]
	if '%chk=' in outputFile[j]:
		chkFile = outputFile[j]
	if 'Charge =' in outputFile[j] and 'Multiplicity =' in outputFile[j]:
		charge = int(outputFile[j].split()[2])
		multiplicity = int(outputFile[j].split()[5])
	if 'Standard orientation:' in outputFile[j]:
		geoFlagStart = j
if geoFlagStart == 0:
	for k in range(len(outputFile)):
		if 'Input orientation:' in outputFile[k]:
			geoFlagStart = k

for m in range(geoFlagStart + 5, len(outputFile)):
	if '------' in outputFile[m]:
		geoFlagEnd = m
		break

coorLines = []

for coorLine in outputFile[geoFlagStart + 5 : geoFlagEnd]:
	coorLines.append(coorLine.strip())

newFileType = 1

print('\n------- Please choose the new input file type -------')
print('   1 - Coordinates only (default)')
print('   2 - Read routine lines from output file')
print('   3 - Leave routine lines section blank')
print('   4 - Read routine lines from additional input')

while True:
	try:
		userInput = input('Please input style number: ')
		userInputInt = int(userInput)
		break
	except ValueError:
		print('Input error, use default (1).')
		userInputInt = 1

if userInputInt > 4:
	print('Input error, use default (1).')
	userInputInt = 1

newGjf = open(f'{fileName.strip()[:-4]}_new.gjf', 'w')

if userInputInt == 4:
	ginpFileName = input("\nPlease specify the path to O2I input file:\n")
	if ginpFileName.strip()[0] == '\'' and ginpFileName.strip()[-1] == '\'':
		ginpFileName = ginpFileName.strip()[1:-1]
#	ginpFileName = input("\nPlease specify the path to O2I input file:\n")
#	if ginpFileName.strip()[0] == '\"' and ginpFileName.strip()[-1] == '\"':
#	    ginpFileName = ginpFileName.strip()[1:-1]
	with open(ginpFileName.strip(), 'r',) as o2iInp:
		o2iInpFile = o2iInp.readlines()
	newGjf.write(f'%nprocshared={o2iInpFile[1].strip()}\n')
	newGjf.write(f'%mem={o2iInpFile[4].strip()}\n')
	newGjf.write(f'%chk={o2iInpFile[7].strip()}\n')
	newGjf.write(f'{o2iInpFile[10].strip()}\n')
	newGjf.write(f'\n{fileName.strip()[:-4]}_new.gjf\n\n')
	newGjf.write(f'{o2iInpFile[13].strip()} {o2iInpFile[16].strip()}\n')

elif userInputInt == 3:
	newGjf.write('%nprocshared=\n')
	newGjf.write('%mem=\n')
	newGjf.write('%chk=\n')
	newGjf.write('# \n')
	newGjf.write(f'\n{fileName.strip()[:-4]}_new.gjf\n\n')
	newGjf.write('charge multiplicity\n')

elif userInputInt == 2:
	newGjf.write(f'%nprocshared={CPUcore}\n')
	newGjf.write(f'{memory.strip()}\n')
	newGjf.write(f'{chkFile.strip()[:-4]}_new.chk\n')
	newGjf.write(f'{routeLine.strip()}\n')
	newGjf.write(f'\n{fileName.strip()[:-4]}_new.gjf\n\n')
	newGjf.write(f'{charge} {multiplicity}\n')

for line in coorLines:
	newGjf.write(f' {elementNo(int(line.split()[1]))}')
	newGjf.write(f'            {line.split()[3]}')
	newGjf.write(f'            {line.split()[4]}')
	newGjf.write(f'            {line.split()[5]}\n')

newGjf.write('\n\n')
newGjf.close()

# ========================== Result information ==========================
print("\n*******************************************************************************")
print("")
print("                          Normal termination of O2I.g")
print("")
print("*******************************************************************************\n")