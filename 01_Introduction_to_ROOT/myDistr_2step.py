#!/usr/bin/python

import sys
import math
import random
from ROOT import *

gRandom = TRandom()
gRandom.SetSeed(2018)
def myDistr() :
  val = gRandom.Uniform(1.)
  if val < 0.5 : val -= 0.5 
  else: val += 0.5 
  return val

sigma = math.sqrt(7./12)
mu = 0.5

def main() :
  cFlat = TCanvas('cFlat','cFlat',800,600)
  hVal = TH1D('hVal','flat*2',300, -1., 2.)
  hVal.SetStats(0)

  for i in  range(1000000) :
    val=myDistr()
    hVal.Fill(val)

  hVal.Draw()
  cFlat.Update()
  cFlat.Print('.png')
  raw_input('press enter to exit')

if __name__ == "__main__" :
  main()
