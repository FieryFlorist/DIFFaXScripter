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
{0}                             {X-ray wavelength}
PSEUDO-VOIGT {1} {2} {3} {4} TRIM {Instrumental broadening (much slower)}

STRUCTURAL                         {Header for structural section}
{5} {5} {6} 120.0         {unit cell coordinates, a, b, c, gamma}
unknown
2                                  {A, B, C planes and two alternate silver stackings}
{7} {7}                           {Layers are very wide in the a-b plane}

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
{8}                         {Infinite number of layers}

TRANSITIONS                      {Header for stacking transition data}
{Transitions from layer 1}
{9}   1/3   2/3  1.0    {layer 1 to layer 1 - "Rhombohedral"}
{10}   0/3   0/3  1.0    {layer 1 to layer 2 - "Hexagonal"}

{Transitions from layer 2}
{11}   0/3   0/3  1.0    {layer 2 to layer 1 - "Hexagonal"}
{12}   2/3   1/3  1.0    {layer 2 to layer 2 - "Rhombohedral"}
""" % (params['lamda'], params['u'], params['v'], params['w'], params['gamma'],
       params['SF:A'], params['SF:C'], params['SF:size'], floor(params['SF:size']/params['SF:C']),
       params['SF:Ratio'], (1-params['SF:Ratio']), (1-params['SF:Ratio']), params['SF:Ratio']))
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
1.5418
PSEUDO-VOIGT 0.756 -1.067 0.426 0.9 TRIM

STRUCTURAL
5.8902 5.8902 2.4047 120.0
unknown
4
400 400

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
350

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
0.0   2/3   1/3  1.0""" % {'MP1':params['Mh:Ratio'], 'MP2':(1-params['Mh:Ratio'])}
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
