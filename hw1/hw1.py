import sys
s = [0.053, 0.051, 0.049, 0.047]
C = [3, 2, 3, 102]
w = 0.3

def getPV(s, C, n, w):
	pv = 0
	for i in range(n):
		pv = pv + C[i]/( (1+s[i])**(i+w) )
	#print 'pv = '+str(pv)
	return pv
def getMD(s, C, n, w):
	duration = 0
	for i in range(n):
		duration = duration + C[i]*(i+w)/(1+s[i])**(i+w)
	#print 'duration = '+str(duration)
	pv = getPV(s, C, n, w)
	duration = duration / pv
	#print 'Macaulay duration = '+str(duration)
	y = getYTM(s, C, n, w, pv)
	duration = duration/(1+y)
	print 'Modified duration = '+str(duration)
	getConvexity(s, C, n, w, y, pv)
	#getPseudoConv(s, C, n, w, y, pv)
	return duration
def getYTM(s, C, n, w, pv):
	accuracy = 1000000
	minErr = 999999999999
	bestY = 1/accuracy
	for y in range(accuracy):
		Yield = (y+1.0)/accuracy + 1
		err = 0
		for i in range(n):
			err = err + C[i]/(Yield**(w+i))
		err = abs(pv-err)
		if err<minErr:
			minErr = err
			bestY = Yield-1
	#print 'yield = '+str(bestY)
	return bestY
def getConvexity(s, C, n, w, y, pv):
	# should be 12.1813
	conv = 0
	for i in range(n):
		t = w+i
		conv = conv + C[i]*(t+1)*t / ((1+s[i])**(t+2))
		#conv = conv + C[i]*(t+1)*t / ((1+s[i])**t)
	conv = conv/pv
	print 'Convexity = '+str(conv)
def getPseudoConv(s, C, n, w, y, pv):
	deltaY = 0.005
	pv_plus = 0
	y=y+1
	for i in range(n):
		pv_plus = pv_plus + C[i]/(y+deltaY)**(w+i)
	pv_minus = 0
	for i in range(n):
		pv_minus = pv_minus + C[i]/(y-deltaY)**(w+i)
	conv = (pv_plus+pv_minus-2*pv)/pv/deltaY/deltaY
	#print 'pseudo conv = '+str(conv)

if __name__ == '__main__':
	'''s_input = raw_input("please type in the spot rates(s): ")
	s = map(float, s_input.strip().split(","))
	C_input = raw_input("please type in the cash flow(C): ")
	C = map(float, C_input.split(","))
	w_input = raw_input("please type in the w: ")
	w = float(w_input)'''
	n = len(s)
	if len(C)!=n:
		print "size of s and C inconsistent!"
		sys.exit(1)
	getMD(s, C, n, w)
