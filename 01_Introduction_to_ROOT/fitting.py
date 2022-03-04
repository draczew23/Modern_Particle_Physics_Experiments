#!/usr/bin/python3

import sys
import math
from ROOT import *

def average_meas(points) :
  average = 0.
  for val in  points:
    average += val
  average /= len(points)
  return average

def sigma_meas(points) :
  average = average_meas(points)
  ss=0.
  for point in points: ss+= pow(point-average,2);
  sigma = math.sqrt(ss/(len(points)-1))
  return sigma


x = [ 1,  3,   4,   5,    6,   7,   8]
y = []
e = []
a=1.
b=2.
s = [ 1., 2., 3., 1., 2.,  3., 1.]
g = TF1("g","gaus",-20.,30.)
g.SetParameter(0,1.)
gRandom.SetSeed(2022)
for i in range(len(x)):
  mean=a*x[i]+b
  g.SetParameter(1,mean)
  g.SetParameter(2,s[i])
  values = []
  nValues =10
  for j in range(nValues) :
    val = g.GetRandom()
    values.append(val)
  y.append(average_meas(values))
# e.append(s[i]/math.sqrt(nValues))
  e.append(sigma_meas(values)/math.sqrt(nValues))
  print ('point  i:',i,' x=',x[i],' y=',y[i],' error=',e[i])

gr=TGraphErrors(7)
gr.SetMarkerColor(4)
gr.SetMarkerStyle(21)

S=0
Sxx=0
Sxy=0
Sx=0
Sy=0

for i in range (len(x)) :
  gr.SetPoint(i, x[i], y[i])
  gr.SetPointError(i, 0.,e[i])

  w_i=1./e[i]/e[i]
  S+=w_i
  Sxx += x[i]*x[i]*w_i
  Sx += x[i]*w_i
  Sxy += x[i]*y[i]*w_i
  Sy += y[i]*w_i
  

D = S*Sxx-Sx*Sx
a = (S*Sxy-Sx*Sy)/D
b = (Sxx*Sy-Sx*Sxy)/D


c = TCanvas('cProsta','cProsta',600,600)
hDummy = TH1D('hDummy','Prosta',100,0.,10.)
hDummy.SetMaximum(12.)
hDummy.SetMinimum(0.)
hDummy.GetXaxis().SetTitle("x")
hDummy.GetYaxis().SetTitle("y")
hDummy.SetStats(0)
hDummy.DrawCopy()
 
gr.Draw('s p')

fline = TF1("flane", "[0]*x+[1]",0.,9.5)
fline.SetParameter(0,a)
fline.SetParameter(1,b)
fline.Draw('same')

c.Print('prosta.png')
#
input('press enter to continue')

chi2 = 0;
for i in range (0,7) :
  d = (y[i]-(a*x[i]+b))/e[i]
  chi2 += d*d
print (' a=',a,' b=',b)
print ('sa=',math.sqrt(S/D),' sb=',math.sqrt(Sxx/D))
print ('chi2/NDF=',chi2/(len(x)-2.))
gr.Fit("pol1"," ")
input('press enter to exit')
#
#
