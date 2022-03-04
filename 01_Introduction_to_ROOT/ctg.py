#!/usr/bin/python3

import sys
import math
from ROOT import *

from myDistr_2step import myDistr, sigma, mu 

cCTG = TCanvas('cCTG','cCTG',1000,500)
hCTG = TH1D('hCTG','hCTG',100, -5., 5.)
hVal = TH1D('hVal','hVal',300, -1., 2.)

#
# loop over experiments, each gives and average X_i
#
nDistrib = 50000 #
for idist in range (0,nDistrib) :


# single try X_i, repeated nProb
#
  sum = 0
  nProb = 25 #enough for average
  for proba in range(0,nProb) :
    val = myDistr()
    hVal.Fill(val)
    sum += val
  #
  # result for singe X_i computation is histogrammed
  #
  ctg_numerator = (sum/nProb)-mu  
  ctg_denominator = sigma/math.sqrt(nProb)
  ctg = ctg_numerator/ctg_denominator
  hCTG.Fill(ctg)


gStyle.SetOptStat(1110)
cCTG.Divide(2,1)
cCTG.cd(1)
gStyle.SetOptStat(1110)
hVal.DrawCopy()

cCTG.cd(2)
hCTG.Scale(1./nDistrib*10)    #10 due to bin whdth
hCTG.Draw('hist')

g1 = TF1("g1", "gaus",-5,5 )
sigmaGauss = 1.
g1.SetParameter(0, 1./sigmaGauss/math.sqrt(2*math.pi) )
g1.SetParameter(1,0)
g1.SetParameter(2,sigmaGauss)
g1.DrawCopy('same')
cCTG.Update()
input('press any key')
cCTG.Print("cCTG.png")