from subprocess import call
import os
import numpy as np

# List of included variables:
# Common Variables
# X-Ray Wavelength
# Pseudo-Voigt U, V, W, and Gamma
# Background Polynomial
# Silver Ferrite
# Lattice parameter A
# Lattice parameter C
# Size
# Maghemite
# Lattice parameter A
# Size
def calcDiff(params):
	# Write Silver Ferrite Fault Params
	out = open('test.dat', 'w')
	out.write("""
INSTRUMENTAL                       {Header for instrumental section}
X-RAY                              {Simulate X-ray diffraction}
%(lamda)f                             {X-ray wavelength}
PSEUDO-VOIGT %(u)f %(v)f %(w)f %(gamma)f TRIM {Instrumental broadening (much slower)}

STRUCTURAL                         {Header for structural section}
%(a)f %(a)f %(c)f 120.0         {unit cell coordinates, a, b, c, gamma}
unknown
2                                  {A, B, C planes and two alternate silver stackings}
%(size)f %(size)f                           {Layers are very wide in the a-b plane}

LAYER 1
NONE
Fe3+  1  0.0  0.0  0/6  0.2  1.0
O 2-   2  2/3  1/3  1/6  0.2  1.0
Ag1+  3  2/3  1/3  3/6  0.2  1.0
O 2-   4  2/3  1/3  5/6  0.2  1.0

LAYER 2
NONE
Fe3+  1  0.0  0.0  0/6  0.2  1.0
O 2-   2  1/3  2/3  1/6  0.2  1.0
Ag1+  3  1/3  2/3  3/6  0.2  1.0
O 2-   4  1/3  2/3  5/6  0.2  1.0

STACKING                         {Header for stacking description}
recursive                        {Statistical ensemble}
%(layers)f                         {Infinite number of layers}

TRANSITIONS                      {Header for stacking transition data}
{Transitions from layer 1}
%(SF1)f   1/3   2/3  1.0    {layer 1 to layer 1 - "Rhombohedral"}
%(SF2)f   0/3   0/3  1.0    {layer 1 to layer 2 - "Hexagonal"}

{Transitions from layer 2}
%(SF2)f   0/3   0/3  1.0    {layer 2 to layer 1 - "Hexagonal"}
%(SF1)f   2/3   1/3  1.0    {layer 2 to layer 2 - "Rhombohedral"}
""" % {'lamda':params['lamda'], 'u':params['u'], 'v':params['v'], 'w':params['w'], 'gamma':params['gamma'],
       'a':params['SF:A'], 'c':params['SF:C'], 'size':params['SF:size'], 'layers':floor(params['SF:size']/params['SF:C']),
       'SF1':params['SF:Ratio'], 'SF2':(1-params['SF:Ratio']))
	out.close()
	# Amend DIFFaX control file
	# Run DIFFaX
	call(["./DIFFaX"])
	# Read In Diffraction Data
	sData = np.genfromtxt('test.spc')
	# Clean up Files
	os.remove('test.dat')
	os.remove('test.spc')
	
	
	# Write Maghemite Fault Params
	out = open('test.dat', 'w')
	out.write("""
INSTRUMENTAL
X-RAY
%(lamda)f
PSEUDO-VOIGT %(u)f %(v)f %(w)f %(gamma)f TRIM

STRUCTURAL
%(a)f %(a)f %(c)f 120.0
unknown
4
%(size)f %(size)f

{ Hex One }
LAYER 1
NONE
Fe3+   1  0.5  0.0  0.0 0.2 5/6
Fe3+   2  0.0  0.5  0.0 0.2 5/6
Fe3+   3  0.5  0.5  0.0 0.2 5/6
O 2-   4  2/3  1/3  0.5 0.2 1.0
O 2-   5  1/6  1/3  0.5 0.2 1.0
O 2-   6  2/3  5/6  0.5 0.2 1.0
O 2-   7  1/6  5/6  0.5 0.2 1.0

{ Hex Two }
LAYER 2
NONE
Fe3+   1  0.5  0.0  0.0 0.2 5/6
Fe3+   2  0.0  0.5  0.0 0.2 5/6
Fe3+   3  0.5  0.5  0.0 0.2 5/6
O 2-   4  2/3  1/3  0.5 0.2 1.0
O 2-   5  1/6  1/3  0.5 0.2 1.0
O 2-   6  2/3  5/6  0.5 0.2 1.0
O 2-   7  1/6  5/6  0.5 0.2 1.0

{ Tet One }
LAYER 3
NONE
Fe3+   1  0.0  0.0  0.0 0.2 5/6
Fe3+   2  2/3  1/3 -1/4 0.2 1.0
Fe3+   3  1/3  2/3  1/4 0.2 1.0
O 2-   4  2/3  1/3  0.5 0.2 1.0
O 2-   5  1/6  1/3  0.5 0.2 1.0
O 2-   6  2/3  5/6  0.5 0.2 1.0
O 2-   7  1/6  5/6  0.5 0.2 1.0

{ Tet Two }
LAYER 4
NONE
Fe3+   1  0.0  0.0  0.0 0.2 5/6
Fe3+   2  2/3  1/3 -1/4 0.2 1.0
Fe3+   3  1/3  2/3  1/4 0.2 1.0
O 2-   4  2/3  1/3  0.5 0.2 1.0
O 2-   5  1/6  1/3  0.5 0.2 1.0
O 2-   6  2/3  5/6  0.5 0.2 1.0
O 2-   7  1/6  5/6  0.5 0.2 1.0

STACKING
recursive
%(layers)d

TRANSITIONS
{Transitions from layer 1}
0.0   1/3   2/3  1.0
0.0   2/3   1/3  1.0
%(MP1)f   1/3   2/3  1.0
%(MP2)f   2/3   1/3  1.0

{Transitions from layer 2}
0.0   1/3   2/3  1.0
0.0   2/3   1/3  1.0
%(MP1)f   1/3   2/3  1.0
%(MP2)f   2/3   1/3  1.0

{Transitions from layer 3}
%(MP1)f   1/3   2/3  1.0
%(MP2)f   2/3   1/3  1.0
0.0   1/3   2/3  1.0
0.0   2/3   1/3  1.0

{Transitions from layer 4}
%(MP1)f   1/3   2/3  1.0
%(MP2)f   2/3   1/3  1.0
0.0   1/3   2/3  1.0
0.0   2/3   1/3  1.0""" % {'lamda':params['lamda'], 'u':params['u'], 'v':params['v'], 'w':params['w'], 'gamma':params['gamma'],
	'size':params['Mh:size'], 'layers':floor(params['Mh:size']/(0.408254*params['Mh:a'])), 'a':params['Mh:a'],
	'c':(0.408254*params['Mh:a']), 'MP1':params['Mh:Ratio'], 'MP2':(1-params['Mh:Ratio'])}
	out.close()
	# Amend DIFFaX control file
	# Run DIFFaX
	call(["./DIFFaX"])
	# Read In Diffraction Data
	mData = np.genfromtxt('test.spc')
	# Clean up Files
	os.remove('test.dat')
	os.remove('test.spc')
	
	# Calculate Polynomial
	polyBack = [0]*2301
	
	# Add models together
	return sData[:,2] + mData[:,2] + polyBack


params = {}
# Silver Ferrite Parameters
# A & B
# C
# Rhombohedral Ratio
params['SF:Ratio'] = 0.3
# Size
# Maghemite Parameters
# A & B & C
# Size
params['Mh:Ratio'] = 1.0
# Polynomial Parameters
# 2 Theta Min, 2 Theta Max, 2 Theta Step
pattern = calcDiff(params)
