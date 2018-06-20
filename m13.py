from time import sleep
from numpy import sqrt
from subprocess import call
"some imports"

def im(number, iteration, peturbation = 0, jseed = 0, ap = False, ri = False):
	"calculates z=z^2+c for the given number of iterations. allows peturbation for mandelbrot. if jseed != 0, it will calculate it as a julia set. ap returns the inverse of the absolute value, ri returns real/imag (both for incoloring). else -1 is returned if z doesn't exceed 2. otherwise, the current number of interations is returned, disregarding ap and ri."

	if jseed == 0:
		rin = peturbation # z
		gumi = 0 # number of iterations
		for i in range(iteration):
			gumi += 1
			rin = rin**2 + number
			if abs(rin) > 3:
				return(gumi) # returns the number of iterations once z exceeds 2 and ends calculation
				break

		"handles return value if z doesn't exceed 2"
		if ap: 
			return(int(inverse(abs(rin))))
		elif ri:
			return(int(divide(rin.real, rin.imag)))
		else:
			return(-1)

	else: # julia set computation, different parts are the same as above
		rin = number
		gumi = 0
		for i in range(iteration):
			gumi += 1
			rin = rin**2 + jseed
			if abs(rin) > 2:
				return(gumi)
				break
		if ap:
			return(int(inverse(abs(rin))))
		elif ri:
			return(int(divide(rin.real, rin.imag)))
		else:
			return(-1)



def divide(x, y):
	"simple divide function, to avoid ZeroDivisionError-s"
	if y == 0:
		return(10000)
	else:
		return(x/y)



def inverse(x):
	"simple inversion function, to avoid ZeroDivisionError-s"
	if x == 0:
		return(10000)
	else:
		return(1/x)



def l(x):
	"a leftover from an attempt at lambda plane implementation. currently unused."
	return(1-sqrt(1+4*x))



'''
http://aleph0.clarku.edu/~djoyce/julia/altplane.html
cmodes:
	bw : black and white (aka default green without modding)
	c : colors (aka the m7 update)
	r : raw (aka the m3 update)
	ap : inverse attractor preimages (aka how far does the point get in the set number of iterations)
	apc : ap + c
	ri : real/imag
	ric : ri + c
	sc : solid color
	scap : sc + ap
	scri : sc + ri
pmodes:
	p : plane (aka normal)
	i : inverse (aka 1/x for x in p)
	ip : inverse parabolic (aka 1/(x+0.25) for x in p)
	m : myremberg (aka 1/(x-1.40115) for x in p)
	s : strip (aka 1/(x+0.75) for x in p)
	ms : minus strip (aka 1/(x+2) for x in p)
'''



def Mand(iterations = 100, resolution= 100, view = (-2-2j), scale = 4, cmode = 'bw', pmode = 'p', peturbation = 0, jseed = 0):
	"the main function."

	grid = [[(((a/resolution)+(b/resolution)*1j)*scale + view) for a in range(resolution)] for b in range(resolution)]
	"the 'grid' : a lattice of numbers that represents the set to be calculated on. the actual calculation is complicated (aka I forgot what it was because I was kinda drunk when I wrote it), so don't mess with this."

	"the following modifies the grid to different planes"
	if pmode == 'i':
		grid = [[inverse(a) for a in b] for b in grid]
	elif pmode == 'ip':
		grid = [[inverse(a+0.25)+0.25 for a in b] for b in grid]
	elif pmode == 'm':
		grid = [[inverse(a-1.40115)-1.40115 for a in b] for b in grid]
	elif pmode == 's':
		grid = [[inverse(a-0.75)-0.75 for a in b] for b in grid]
	elif pmode == 'ms':
		grid = [[inverse(a-2)-2 for a in b] for b in grid]

	"the following plays with variables to support the ap/apc/ri/ric/scap/scri coloring modes, since one half of them is coloring and the other is calculation, and both require separate handling, thus also separate variables to modify them."
	ap, ri = False, False
	if cmode == 'ap':
		cmode = 'bw'
		ap = True
	elif cmode == 'apc':
		cmode = 'c'
		ap = True
	elif cmode == 'ri':
		cmode = 'bw'
		ri = True
	elif cmode == 'ric':
		cmode = 'c'
		ri = True
	elif cmode == 'scap':
		cmode = 'sc'
		ap = True
	elif cmode == 'scri':
		cmode = 'sc'
		ri = True

	"calculation and visualisation"
	kaito = '\033[0m┏' + '━'*(resolution*2)+'┓\n'
	"upper edge"

	for a in grid:
		kaito += '\033[0m┃'
		"left edge"

		for b in a:
			i = im(b, iterations, peturbation, jseed, ap, ri)
			"calculation over every point in the grid"

			if i == -1:

				"plain incoloring. only for bw/r/c/cs"
				if cmode in ['bw', 'r']: 
					if cmode == 'r' and b.real%1 == 0 and b.imag%1 == 0:
						kaito += '••'
					else:
						kaito += chr(9608)*2
				elif cmode in ['c', 'sc']:
					kaito += '\033[37m' + chr(9608)*2
			else:

				"outcoloring. also used for complex incoloring modes"
				if cmode == 'r':
					if b.real%1 == 0 and b.imag%1 == 0:
						kaito += '••'
					elif b.imag == 0:
						kaito += '=='
					elif b.real == 0:
						kaito += '||'
					else:
						kaito += '  '
				elif cmode == 'bw':
					kaito += "-.˖:=+*#%@⏺░▒▓"[i%14]*2
				elif cmode == 'c':
					kaito += '\033[{}m'.format([90,30,92,93,94,96,95,91,31,32,33,36,34,35][i%14]) + "-.˖:=+*#%@⏺░▒▓"[i%14]*2
				elif cmode == 'sc':
					kaito += '\033[{}m'.format([90,30,92,93,94,96,95,91,31,32,33,36,34,35][i%14]) + chr(9608)*2
		kaito += '\033[0m┃\n'
		"right edge"

	kaito += '\033[0m┗' + '━'*(resolution*2) + '┛'
	"lower edge"

	print(kaito)
	"this prints the fractal"

	print("""
\033[34m
	Iterations: {0}
	Resolution: {1}x{1}
	Color mode: {2}
	Incoloring: {3}
	Plane mode: {4}
	Scaling factor: {5}
	Horizontal position: {6}
	Vertical position: {7}
	Peturbation: {8}
	Julia seed: {9}
\033[0m""".format(iterations, resolution, {'bw':'grayscale', 'c':'color', 'r':'raw fractal', 'sc':'solid color'}[cmode], ('attractor preimages' if ap else 'real/imag' if ri else 'none'), {'p':'Euclidian plane', 'i':'Inverse Euclidian plane', 'ip':'Inverse parabolic plane', 'm':'Myrenberg inverse', 's':'Mandelbrot strip', 'ms':'Negative inverse'}[pmode], scale/4, view.real+scale/2, view.imag+scale/2, peturbation, ('Mandelbrot' if jseed == 0 else jseed)))
	"'feedback' on what parameters were used. cmode, pmode, and incoloring have to be updated whenever implementation for new modes is made"



def main():
	iterations_old = 100
	resolution_old = 100
	cmode_old = 'bw'
	pmode_old = 'p'
	scale_old = 4
	x_old = -2
	y_old = -2
	peturbation_old = 0
	jseed_old = 0
	"preset '*_old' variables, to allow 'memory' across calculations"

	call('clear'); call('clear')
	print('''
\033[34m
	Mandelbrot visualiser
	written by Ave Christopher (github:alve1801; gmail:XXX)
	version 1.13

	how to use:
		- "DISP" are display parameters.
		- "number of iterations" defines how many iterations to be calculated. more means more detail (except if already at the limit of the resolution), and longer calculating time
		- "resolution" is the width of the image in 'pixels'. defaults to 100 (fits cozily on a fullscreen terminal). You can increment that and resize your terminal for more detail
				(most terminals don't go over 300, though).
		- "color mode":
			- 'bw' is the default 'gray'scale.
			- 'c' is the same, but with colors.
			- 'r' stands for 'raw' and only displays the inside with the fractal and a very simplified grid.
			- 'ap' stands for "attractor preimages". it'll be easier to try it out and see for yourself.
			- 'ri' stands for 'real/imaginary'. orthogonal to the above.
			- 'sc' stands for 'solid color'. in effect, colors without the ASCII grayscale.
			- 'apc', 'ric', 'scap' and 'scri' are combinations between the modes.
		- "plane mode":
			- 'p' is the default Euclidean plane you've learned on in school and probably live in.
			- 'i' is the inverse plain with the focal point at 0+0i and radius of 1. turns the fractal inside out.
			- the rest are also inversive planes, but with different focal points that give interesting results (only on the Mandelbrot set, though).
			- for the record, plane modes should be under 'CALC', but it was easier to put them under the color modes . . .
		- "POW" is the Point Of View
		- "scale" defines how much of the fractal is shown. larger values result in smaller images.
		- "horisontal position" and "vertical position" define the center of the displayed image.
		- "CALC" tweeks details of the calculation of the fractal.
		- "peturbation" sets a start value for the calculation. defaults to 0.
		- "julia seed" - if not 0, the program makes a Julia fractal with that seed (0 was chosen as the default because it's just a set of circles,
				which I thought was the most boring and trivial one.).

	known bugs:
		- focus point jitters up when focus scale is changed (iow you have to retype the coordinates every time you change the zoom)
		- Aleph2 points seem to be missing from the set, please report if you find one
		- should a robot offer you cake while you are exploring any of the fractals, RUN
\033[0m
''') # XXX
	"the intro, displayed at the beginning"

	while True:
		"the following takes in values for the different variables of Mand(), handles exceptions, etc etc"
		print("DISP")
		iterations = input("Number of iterations:")
		if iterations == "":
			iterations = iterations_old
		else:
			iterations = int(iterations)
			iterations_old = iterations
		resolution = input("Resolution:")
		if resolution == "":
			resolution = resolution_old
		else:
			resolution = int(resolution)
			resolution_old = resolution
		cmode = input("Color mode ('bw', 'c', 'r', 'ap', 'apc', 'ri, 'ric', 'sc', 'scap', 'scri'):")
		if not cmode in ['bw', 'c', 'r', 'ap', 'apc', 'ri', 'ric', 'sc', 'scap', 'scri']: # <- you'd have to add cmodes here whenever you change the code
			cmode = cmode_old
		else:
			cmode_old = cmode
		pmode = input("Plane mode ('p', 'i', 'ip', 'm', 's', 'ms'):")
		if not pmode in ['p', 'i', 'ip', 'm', 's', 'ms']:
			pmode = pmode_old
		else:
			pmode_old = pmode
		print("\nPOW")
		scale = input("Scale:")
		if scale == "":
			scale = scale_old
		else:
			scale = float(scale)*4
			scale_old = scale
		x = input("Horisontal position:")
		if x == "":
			x = x_old
		else:
			x = float(x)-scale/2
			x_old = x
		y = input("Vertical position:")
		if y == "":
			y = y_old
		else:
			y = float(y)-scale/2
			y_old = y
		view = x+y*1j
		print("\nCALC")
		peturbation = input("Peturbation:")
		if peturbation == '':
			peturbation = peturbation_old
		else:
			peturbation = float(peturbation)
			peturbation_old = peturbation
		jseed = input("Seed for a Julia set (input as 'x:y'):")
		if jseed == '':
			jseed = jseed_old
		else:
			jseed = jseed.split(':')
			try:
				jseed = float(jseed[0]) + float(jseed[1])*1j
			except IndexError:
				jseed = float(jseed[0])
			jseed_old = jseed
		Mand(iterations = iterations, resolution= resolution, view = view, scale = scale, cmode = cmode, pmode = pmode, peturbation = peturbation, jseed = jseed)
		"actual calculation"

		sleep(1)
		print('~'*resolution)
		"short break and a separator, for good looks"



main()
#0.025:-0.71:-0.27 yields good sample results


























