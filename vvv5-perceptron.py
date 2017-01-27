##Vladimir Ventura
##CS675
##Due 9/30/2014
##Assignment 2

import sys
import math

datafile = sys.argv[1]
f = open(datafile)
data = []
i=0
l=f.readline()
###############
#### Read data
###############

while(l != ''):
	a=l.split()
	l2=[]
	for j in range(0, len(a), 1):
		l2.append(float(a[j]))
	l2.append(1)
	data.append(l2)
	l=f.readline()

rows = len(data)
cols = len(data[0])
f.close()

######################
### Read Labels
######################

labelfile=sys.argv[2]
f=open(labelfile)
trainlabels = {}
n=[]
n.append(0)##number of 0s and 1s labels.
n.append(0)##n[0] == 0th label; n[1] == 1th label
l=f.readline()

while(l!=''):
	a = l.split()
	if(int(a[0]) ==0): ##enter -1 instead of 0 for perceptron purposes.
		trainlabels[int(a[1])] = -1
	else:
		trainlabels[int(a[1])]= int(a[0])
	l=f.readline()
	n[int(a[0])] +=1

####################
###Compute Means and w, w0
####################
##recall y[i] is the label and x[i] is the actual data point.

##w = m2-m1
m0 =[]

for j in range(0, cols, 1):
	m0.append(0)
m1=[]
for j in range(0, cols, 1):
	m1.append(0)

for i in range(0, rows, 1):
	if(trainlabels.get(i) != None and trainlabels[i] ==-1):
		for j in range(0, cols, 1):
			m0[j] = m0[j] + data[i][j]
	if(trainlabels.get(i) != None and trainlabels[i]==1):
		for j in range(0, cols, 1):
			m1[j] = m1[j]+data[i][j]

for j in range(0, cols, 1):
	m0[j] = m0[j]/n[0]
	m1[j] = m1[j]/n[1]

#print(m0)
#print(m1)
w=[]
prevW=[]
for i in range(0, cols, 1):
	prevW.append(float(2))
	w.append(float(0))
	w[i]=m1[i]-m0[i]
#print("Starting w = m2-m1: ")
#print(w)##this is the starting w

#####################################
###		compute until convergence
#####################################

#delF=[]
#for i in range(0, cols, 1):
#	delF.append(0) ##as many columns, or dimensions of data, there are in the datapoints will be needed in delF
#print(prevW)
#print(w)
#math.sqrt((prevW[0]-w[0])**2 + (prevW[1]-w[1])**2)

# prevDelF=[]
# prevDelF.append(0)
# prevDelF.append(0)
# prevDelF.append(0)
#print(delF)
sum=1
prevsum=0
print("while loop starting")
#while(abs(delF[0]- prevDelF[0])>0.001 and abs(delF[1]-prevDelF[1])/abs(delF[0]-prevDelF[0])> 0.001):
while(abs(sum-prevsum)>0.001):	
	##delF = sigma((labelpoint[i]- w*datapoint[i])*datapoint[i][0], (yi-w*datapoint[i])*datapoint[i][1]
	#prevDelF=delF
	delF=[] #start delF at 0 everytime we do an iteration.
	for i in range(0, cols, 1):
		delF.append(float(0)) ##as many columns, or dimensions of data, there are in the datapoints will be needed in delF

	for i in range(0, rows, 1):
		for j in range(0, cols, 1):
			dotprod=0
			for wcols in range(0, cols, 1):
				dotprod+=w[wcols]*data[i][wcols]
			delF[j]+= 2*(trainlabels.get(i) - dotprod)*data[i][j]
	#print("Del F is:")
	#print(delF)
	#prevW=w;
#	w=w+0.001*float(delF)
	for j in range(0, cols, 1):
			w[j]=w[j]+0.000000000000000001*float(delF[j])
	
	
	prevsum=sum
	sum=0
	for i in range(0, rows, 1):
		for j in range(0, cols, 1):
			dotprod=0;
			for wcols in range(0, 3 ,1):
				dotprod+=w[wcols]*data[i][wcols]
			sum+=(trainlabels.get(i)-dotprod)**2
	print("Sum is: " + str(sum) + " prevsum is: " + str(prevsum))
print("When using the stopping point of 0.001, w is: ")
print(w)
magnitude =0
for i in range(0, cols-1, 1):
	magnitude+= w[i]**2
magnitude=math.sqrt(magnitude)
print("The distance of plane to origin is about", abs(w[cols-1]/magnitude))

# while(abs(sum-prevsum)>0):	
	# ##delF = sigma((labelpoint[i]- w*datapoint[i])*datapoint[i][0], (yi-w*datapoint[i])*datapoint[i][1]
	# #prevDelF=delF
	# delF=[] #start delF at 0 everytime we do an iteration.
	# for i in range(0, cols, 1):
		# delF.append(float(0)) ##as many columns, or dimensions of data, there are in the datapoints will be needed in delF

	# for i in range(0, rows, 1):
		# for j in range(0, cols, 1):
			# dotprod=0
			# for wcols in range(0, 3, 1):
				# dotprod+=w[wcols]*data[i][wcols]
			# delF[j]+= 2*(trainlabels.get(i) - dotprod)*data[i][j]
	# #print("Del F is:")
	# #print(delF)
	# #prevW=w;
# #	w=w+0.001*float(delF)
	# for j in range(0, cols, 1):
			# w[j]=w[j]+0.001*float(delF[j])
	
	
	# prevsum=sum
	# sum=0
	# for i in range(0, rows, 1):
		# for j in range(0, cols, 1):
			# dotprod=0;
			# for wcols in range(0, cols ,1):
				# dotprod+=w[wcols]*data[i][wcols]
			# sum+=(trainlabels.get(i)-dotprod)**2
	# #print(sum-prevsum)
# print()
# print("When letting the equation converge, the w will be:")
# print(w)
# error=0
# #for i in range (0, rows, 1):
# #	for j in range(0, cols, 1):
# #		dotprod=0
# #		for k in range(0, cols, 1):
# #			dotprod+=w[k]*data[i][k]
# #		sum+=(trainlabels.get(i) - 
# print("The error is: ", sum)
# magnitude =0
# for i in range(0, cols-1, 1):
	# magnitude+= w[i]**2
# magnitude=math.sqrt(magnitude)
# print("The distance of plane to origin is about", abs(w[cols-1]/magnitude))

########################
### Classify unlabld points
##########################

print("classifying!\n\n\n\n")
testfile = sys.argv[3];
t = open(testfile);
test = []
l=t.readline()
output = open("testoutput.txt", "r+")
trow=0;
while(l != ''):
	a=l.split()
	l2=[]
	for j in range(0, len(a), 1):
		l2.append(int(a[j]))
	l2.append(1); #for the w0;
	sum=0
	for j in range(0, len(a), 1):
		sum+=w[j]*l2[j]; ##get the sum wTx+w0 = y.
	print(sum)
	if (sum>0):
		output.write(str(1) + " " + str(trow) + "\n")
	else:
		output.write(str(0) + " " + str(trow) + "\n")
	trow+=1
	test.append(l2)
	l=t.readline()
#output.write("The w used with this project is as follows:\n")
#output.write("Note that any 0's in w means that the columns were removed/not used")
output.close()
t.close()
print("The columns used are as follows\n")
print(w)

