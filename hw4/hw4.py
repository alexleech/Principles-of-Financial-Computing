'''
Inputs: 
		x (year), 
		y (year), 
		r (%) (initial short rate), 
		b (%) and 
		m (%), 
		s (%), 
		n (the number of steps during the option's life), and 
		strike price X (% of par).
'''

from __future__ import division
import sys
import json
from math import *
import numpy as np
import time

def BinomialCIR(data):

	# Initial value
	t = data['x']
	T = data['y']
	r = data['r'] / 100
	b = data['b'] / 100  # from percentage to decimal
	m = data['m'] / 100
	s = data['s'] / 100
	n = data['n']
	X = data['X'] / 100

	# data after calc
	deltaT = T/n
	print "deltaT = "+str(deltaT)
	x_r = 2*sqrt(r)/s
	deltaX = sqrt(deltaT)
	optionDuration = n*t/T
	print optionDuration
	# Initial Price
	Price = np.ones(n+1)
	# Binomial CIR model
	for j in reversed(range(n)):
		for i in range(j+1):
			p = 1
			x_prime = x_r + (j-2*i)*deltaX
			r_prime = x_prime*x_prime*s*s/4
			if not r_prime == 0:
				r_plus = x_prime+deltaX
				r_plus = r_plus*r_plus*s*s/4
				r_minus = x_prime-deltaX
				r_minus = r_minus*r_minus*s*s/4
				p = (b*(m-r_prime)*deltaT+r_prime-r_minus) / (r_plus-r_minus)
			else:
				print "FUCK!!!"
			if p<0: 
				p=0
			elif p>1:
				p=1
			discountFactor = 1 / exp(r_prime * deltaT)
			#print "dis = "+str(discountFactor)
			Price[i] = (p*Price[i]+(1.0-p)*Price[i+1])*discountFactor
			print "j = "+str(j)+" i = "+str(i)+" r = "+str(r_prime)+" p = "+str(p)+" $ = " +str(Price[i])
			if j<=optionDuration and Price[i]>X:
				Price[i] = 0
	return Price[0]

if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
		with open(file_location) as data_file:
			data = json.load(data_file)
		for test in data:
			#tic = time.clock()
			ans = BinomialCIR(test)
			#toc = time.clock()
			#print toc-tic
			print "price = "+str(ans)
		#print "finished!"
	else:
		print 'Requires an input file. (e.g. python hw4.py data)'