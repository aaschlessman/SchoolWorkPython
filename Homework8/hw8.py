#Aaron Schlessman
#HW8
#4630

import scipy.stats as stats
import math
import numpy

claimaverage = 293
foundaverage = 270
standarddeviation = 50
samplesize = 20
significance = 0.05
confidence = 1 - significance

crit = stats.t.isf(significance/2, samplesize - 1)

t = (foundaverage / claimaverage) / (standarddeviation / numpy.sqrt(samplesize))

p = stats.t.sf(numpy.abs(t), samplesize - 1) * 2

print("The Null Hypothesis - The mean life of the batteries under normal use are", claimaverage, "hours")
print("The Alternate Hypothesis - The mean life of the batteries are not", claimaverage, "hours")
print("t statistic =", t)
print("critical value =", crit)
print("p =", p)

if numpy.abs(t) < crit:
    print("The null hypothesis is not rejected at confidence level", confidence, "%, because t (", t, ") is within the bound of the Critical Value (", crit, ")")
else:
    print("The null hypothesis is rejected at confidence level", confidence, "%, because t (", t, ") is outside the bound of the Critical Value (", crit, ")")

olderAdults = numpy.array([45, 38, 52, 48, 25, 39, 51, 46, 55, 46])
youngerAdults = numpy.array([34, 22, 15, 27, 37, 41, 24, 19, 26, 36])
samplesize = len(olderAdults)
significance = 0.05
confidence = 1 - significance
crit = stats.t.isf(significance/2, samplesize-1)
ttest = stats.ttest_ind(olderAdults, youngerAdults)

print("The Null Hypothesis - The Life Satisfaction scores are not significant different")
print("The Alternate Hypothesis - The Life Satisfaction scores are significantly different")
print("t statistic =", ttest[0])
print("critical value =", crit)
print("p =", ttest[1])

if numpy.abs(ttest[0]) < crit:
    print("The null hypothesis is not rejected at confidence level", confidence, "%, because t (", ttest[0], ") is within the bound of the Critical Value (", crit, ")")
else:
    print("The null hypothesis is rejected at confidence level", confidence, "%, because t (", ttest[0], ") is outside the bound of the Critical Value (", crit, ")")
