#Aaron Schlessman
#CS4630
#Homework4 short
#Leslie matrix and Eigenvalue

import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la

with open('HW4shortData.txt', 'r') as file:
    DataList = file.read().splitlines()

Distribution = np.array(DataList[3].split(' ')).reshape(3, 1).astype(np.float64)

DataList = DataList[:3]

print("Leslie Matrix:")
for x in DataList: print(x)

DataList = [x.split(' ') for x in DataList]

DataMatrix = np.asarray(DataList).astype(np.float64)

Eigenvalues, Eigenvectors = la.eig(DataMatrix)

print("Eigenvalues: \n", Eigenvalues)
print("Eigenvectors: \n", Eigenvectors)

if (Eigenvalues[0] > 1): print("Population is growing")
if (Eigenvalues[0] == 1): print("Population is stable")
if (Eigenvalues[0] < 1): print("Popoulation is declining")

PopMatrix = []
PopMatrix.append(np.dot(DataMatrix, Distribution))

for x in range(1,101):
    PopMatrix.append(np.dot(DataMatrix, PopMatrix[x-1]))

t = [np.sum(x) for x in PopMatrix]

pop0 = []
pop1 = []
pop2 = []

for x in PopMatrix:
    pop0.append(x[0])
    pop1.append(x[1])
    pop2.append(x[2])

percent0 = []
percent1 = []
percent2 = []
for x in range(101):
    percent0.append(pop0[x]/t[x])
    percent1.append(pop1[x]/t[x])
    percent2.append(pop2[x]/t[x])

print("Age Distribution 0:", percent0[100])
print("Age Distribution 1:", percent1[100])
print("Age Distribution 2:", percent2[100])

x = np.arange(0.0, 101.0, 1)
fig, ax = plt.subplots()
ax.plot(x, percent0, color="red", label="Age 0 Dist")
ax.plot(x, percent1, color="blue", label="Age 1 Dist")
ax.plot(x, percent2, color="green", label="Age 2 Dist")
ax.set_xlabel('Time Period')
ax.set_ylabel('Population')
ax.set_title("Percentage Distribution")
ax.legend(loc=0)
plt.show()