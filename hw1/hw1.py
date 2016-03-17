s = [0.053, 0.051, 0.049, 0.047]
C = [3, 2, 3, 102]
w = 0.3

def getPV(s, C, n, w):
	pv = 0
	for i in range(n):
		pv = pv + C[i]/( (1+s[i])**(i+w) )
	print 'pv = '+str(pv)
	return pv
def getMD(s, C, n, w):
	duration = 0
	for i in range(n):
		duration = duration + C[i]*(i+w)/(1+s[i])**(i+w)
	#print 'duration = '+str(duration)
	pv = getPV(s, C, n, w)
	duration = duration / pv
	print 'Macaulay duration = '+str(duration)
	y = getYTM(s, C, n, w, pv)
	duration = duration/(1+y)
	print 'Modified duration = '+str(duration)
	return duration
def getYTM(s, C, n, w, pv):
	accuracy = 100000
	minErr = 999999999999
	bestY = 1/accuracy
	for y in range(accuracy):
		Yield = (y+1.0)/accuracy + 1
		err = 0
		for i in range(n):
			err = err + C[i]/(Yield**(w+i))
		err = abs(pv-err)
		if err<minErr:
			print err
			minErr = err
			bestY = Yield-1
	print 'yield = '+str(bestY)
	return bestY
if __name__ == '__main__':

	n = len(s)
	if len(C)!=n:
		print "size of s and C inconsistent!"
	getMD(s, C, n, w)
