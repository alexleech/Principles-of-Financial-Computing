'''
Inputs: 
		S (stock price at time 0), 
		X (strike price), 
		T (maturity in years), 
		s (%) (annual volatility), 
		r (%) (continuously compounded annual interest rate), 
		n (number of periods), and 
		k (number of simulation paths). 
'''

from __future__ import division
import sys
import json
from math import *
import numpy as np

def MCLSQ(data):

    # Initial value
    S = data['S']
    X = data['X']
    T = data['T']
    s = data['s'] / 100  # from percentage to decimal
    r = data['r'] / 100
    n = data['n']
    k = data['k']
    #r = 0.05
    #T = 3
    #n = 3
    #k = 8
    # data after calc
    deltaT = T/n
    firstParam = (r-s*s/2)*deltaT
    secondParam_without_norm = s*(sqrt(deltaT))
    discountFactor = 1 / exp(r * deltaT)
    #print discountFactor
    # Initial matrix
    StockPath = np.zeros((k, n))

    for i in range(k):
    	StockPath[i, 0] = S*exp(firstParam+secondParam_without_norm*np.random.normal())
    	for j in range(n-1):
    		StockPath[i, j+1] = StockPath[i, j]*exp(firstParam+secondParam_without_norm*np.random.normal())
    #print StockPath
    StockPath[ StockPath>X ] = 0
    #print StockPath
    # Create Cash Flow matrix
    CashFlow = np.zeros((k, n))
    for i in range(k):
    	CashFlow[i,n-1] = 0 if StockPath[i,n-1]==0 else X-StockPath[i,n-1]
    #print CashFlow
    # Backward pricing with regression
    for i in range(n-2, -1, -1):
    	#print "i = " + str(i)
    	selected_path_id = np.where(StockPath[:,i] > 0)[0]
    	len_selected_path_id = len(selected_path_id)
    	#print selected_path_id
    	x_reg = StockPath[selected_path_id, i]
    	#print "xreg: " + str(x_reg)
    	y_reg = np.zeros(len_selected_path_id)
    	
    	for j in range(len_selected_path_id):
    		for t in range(i+1, n):
    			if CashFlow[selected_path_id[j], t]>0:
    				y_reg[j] = CashFlow[selected_path_id[j], t] * pow(discountFactor, t-i)
    				break
    		#d = min(np.where(CashFlow[selected_path_id[j], :]>0))[0] - i
    		#print "d = " + str(d)
    		#y_reg[j] = CashFlow[selected_path_id[j], i+d] * pow(discountFactor, d)
    	#print "yreg: " + str(y_reg)
    	coefs = np.polyfit(x_reg, y_reg, 2)
    	#print coefs
    	ffit = np.poly1d(coefs)																																																													
    	#print ffit
    	continuation = ffit(x_reg)
    	exercise = X - StockPath[selected_path_id, i]
    	#print "cont: " + str(continuation)
    	#print "exer: " + str(exercise)
    	#print exercise
    	for j in range(len_selected_path_id):
    		CashFlow[selected_path_id[j],i] = exercise[j] if exercise[j]>continuation[j] else 0
    	#continuation = pre
    	#print CashFlow
    #	arrange to present value
    presentValue = np.zeros(k)
    for i in range(k):
    	for j in range(n):
    		if(CashFlow[i, j]>0):
    			presentValue[i] = CashFlow[i, j]*pow(discountFactor, j+1)
    			#print j+1
    			break
    #print presentValue
    mean = np.mean(presentValue)
    print mean
    return mean
    #print np.std(presentValue)
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location) as data_file:
            data = json.load(data_file)
        times = 30
        for test in data:
			ans = np.zeros(times)
			for i in range(times):
				print i
				ans[i] = MCLSQ(test)
			print np.mean(ans)
			print np.std(ans)
        print "finished!"
    else:
        print 'Requires an input file. (e.g. python hw3.py data)'