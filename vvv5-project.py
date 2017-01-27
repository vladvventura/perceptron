##Vladimir Ventura
##CS675
##Course Project -- I decided to make a perceptron with multivariate feature selection using the F score.
##by iterating and removing the least significant features using an arbitrary threshold.
##I must note that this program took me about half an hour to run. Reading the data took 3 minutes;
##Labels 1 minute-ish, Means and F score take a bulk of time..
import sys
import math
import statistics

datafile = sys.argv[1]
f = open(datafile)
data = []
i=0
l=f.readline()
print("Reading data...")
###############
#### Read data
###############

while(l != ''):
	a=l.split()
	l2=[]
	for j in range(0, len(a), 1):
		l2.append(int(a[j]))
	l2.append(1)
	data.append(l2)
	l=f.readline()

rows = len(data)
cols = len(data[0]) ##but remember we don't want to include w0 (the last element)
##for least significant w removal.
f.close()

print("Finished reading data")
######################
### Read Labels
######################
print("Reading labels...")
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
print("Finished reading labels")
print("Reading testdata")
#########################
#### Test Data Algorithm
#################################
testfile = sys.argv[3];
t = open(testfile);
test = []
l=t.readline()
#output = open("output", "r+")
trow=0;
while(l != ''):
	a=l.split()
	l2=[]
	for j in range(0, len(a), 1):
		l2.append(int(a[j]))
	l2.append(1); #for the w0;
	test.append(l2)
	l=t.readline()
	trow+=1
tcol= len(test[0])
print("Finished reading testdata")
####################
###Compute F score using means and 
####################
##recall y[i] is the label and x[i] is the actual data point.

##w = m2-m1
print("Computing means...")
fscores=[];
m=[]
m0 =[]
m1=[]
for j in range(0, cols, 1):
	m0.append(0)
	m1.append(0)
	m.append(0)
	fscores.append(0)

for i in range(0, rows, 1):
	for j in range(0, cols, 1):
		m[j]=m[j]+data[i][j] ##average on the whole.
		if(trainlabels.get(i) != None and trainlabels[i] ==-1):
			m0[j] = m0[j] + data[i][j]
		if(trainlabels.get(i) != None and trainlabels[i]==1):
			m1[j] = m1[j]+data[i][j]

for j in range(0, cols, 1):
	m0[j] = m0[j]/n[0]
	m1[j] = m1[j]/n[1]
	m[j] = m[j]/rows;

#print(m0)
#print(m1)
#print(m)
print("finished calculating means")
#######################
## m0 is negative, m1 is positive, m is overall average.
#######################
print("Calculating F scores...")
for i in range(0, cols-1, 1): ##don't do the last column.
	left=0
	right=0
	for j in range(0, rows, 1):
		if(trainlabels.get(j) != None and trainlabels[j]==1):
			left = left + (data[j][i] - m1[i])**2 ##calculating the denominator values.
		if(trainlabels.get(j) != None and trainlabels[j]==-1):
			right= right + (data[j][i] - m0[i])**2
	#print("The denominatora is: ")
	#print(left/(n[1]-1) + right/(n[0]-1));
	fscores[i] = ((m1[i]-m[i])**2 + (m0[i]-m[i])**2 )/(left/(n[1]-1) + right/(n[0]-1));
print("F scores calculated")

##find the max F, store the feature, set it to 0 and then find the next max.
features=[]
testfeatures=[]
i=0
while(i<17):
	feature=[] ##for single feature
	testfeature=[]
	maxval=max(fscores)
	maxindex=0
	while(fscores[maxindex]!=maxval):
		maxindex+=1
	#Now we have the max index of the most significant f score.
	for j in range(0, rows, 1):
		feature.append(data[j][maxindex])
	for j in range(0, trow, 1):
		testfeature.append(test[j][maxindex])
	features.append(feature)
	testfeatures.append(testfeature)
	print(i)
	i+=1
	
	fscores[maxindex]=0 ##to find the next largest fscore

##now each feature is stored horizontally.
output  = open("newtrain.txt", "r+")
print("len(features[1]) is " + str(len(features[1])))
for j in range(0, len(features[1]), 1):
	for i in range(0, len(features), 1):
		output.write(str(features[i][j]) + " ")
	output.write("\n")
output.close()
print("Doing newtestdata.txt output")

testdataoutput= open("newtestdata.txt", "r+")
for j in range(0, len(testfeatures[1]), 1):
	for i in range(0, len(testfeatures), 1):
		testdataoutput.write(str(testfeatures[i][j]) + " ")
	testdataoutput.write("\n")
testdataoutput.close()

#fmean = statistics.mean(fscores)
#fvar = statistics.variance(fscores)
#print("F mean is: " + str(fmean) + " and F var is: " + str(fvar))

#From experience, the fmean is 0.00015288452120202178 and the fvar is 2.593176868800625e-07
#so the thresholding is VERY nitpicky (variance is super small).
#threshold will start with the fmean, especially since the variance is so low.
exit()

###################################################################
## Cross validation on random with different F score thresholds.
##################################################################
print("Removing features below fscore threshold")
thresholds =[]
thresholds.append(fmean)
for i in range(0, cols-1, 1):
	if(fscores[i]<thresholds[0]):
		for j in range(0, rows, 1):
			if(i<cols-2):
				data[j][i]=data[j][i+1]
			##if the fscore isn't high enough, delete the column of data.
			else:
				data[j][i]=0
			##now that we shifted everything by 1, we need to decrease number of columns
			##and set i back 1 to read this new shifted column
		cols=cols-1;
		i=i-1;
		##this works because we don't process the last column.
###############################################

w=[]
prevW=[]
for i in range(0, cols, 1):
	prevW.append(float(2))
	w.append(float(0))
	w[i]=0.01;
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
numLoops=0
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
		w[j]=w[j]+0.001*float(delF[j])##the step size is SUPER important here. it is the deal breaker.
	
	prevsum=sum
	sum=0
	for i in range(0, rows, 1):
		for j in range(0, cols, 1):
			dotprod=0;
			for wcols in range(0, cols ,1):
				dotprod+=w[wcols]*data[i][wcols]
			sum+=(trainlabels.get(i)-dotprod)**2
print("When using the stopping point of 0.001, w is: ")
print(w)
magnitude =0


for i in range(0, cols-1, 1):
	magnitude+= w[i]**2
magnitude=math.sqrt(magnitude)
print("The distance of plane to origin is about", abs(w[cols-1]/magnitude))


exit()
########################
### Classify unlabeled points
##########################
#Note:
#This entire section was used for finding the ber of each threshold. I did not use random rows.
#The program already took long enough to run as is.
# print("validating...")
# a=0; b=0;
# for i in range(int(0.3*rows), int(0.6*rows), 1):
	# sum=0
	# for j in range(0, cols, 1):
		# sum+= w[j]*data[i][j]
	# if(sum <0 and trainlabels[i]==1): #then it's incorrect!
		# b+=1
	# elif(sum>0 and trainlabels[i]==-1):
		# a+=1 #positive incorrectly labeled
		
# for i in range(int(0.9*rows), rows, 1):
	# sum=0
	# for j in range(0, cols, 1):
		# sum+= w[j]*data[i][j]
	# print(sum)
	# if(sum <0 and trainlabels[i]==1): #then it's incorrect!
		# b+=1
	# elif(sum>0 and trainlabels[i]==-1):
		# a+=1 #positive incorrectly labeled
	
# ber = 0.5*(a/(0.1*rows) + b/(0.3*rows))		
# print("The error rate is: " + str(ber))





output.write("The w used with this project is as follows:\n")
output.write(w)
#output.write("Note that any 0's in w means that the columns were removed/not used")
output.close()
t.close()
print("The columns used are: as follows\n" + w)
