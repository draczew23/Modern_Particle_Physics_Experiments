#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from ROOT import *
from readData import readData 

throw1 = []
throw2 = []

#
# read data 
#
readData('data_dice.txt', throw1, throw2)

#
# cat data 
#
print ('numbwer of throws1: {0:2d}, number of throws2: {1:2d}'.format(len(throw1),len(throw2)) )
nThrows = len(throw1) 
t1=0
t2=0
for i in range(nThrows) :
  print ('  {0:1d}, {1:1d}'.format(throw1[i], throw2[i]))
  t1 += throw1[i]
  t2 += throw2[i]
print (' summ t1: {0:3d}, summ t2: {1:3d}, nThrows: {2:3d}, average: {3:5.3f}'.format(t1,t2,nThrows, double(t1+t2)/nThrows))
input('press enter to continue (1)')

#
# define a Canva and histogram
#
c = TCanvas('cHistogram','cHistogram',500,500)
hDice = TH1D('hDice','Throw 1 and 2 combined; sum of dice; #events',6,0.5,6.5)
hDice.Sumw2()

# decorations 
hDice.SetMinimum(0) 
hDice.GetXaxis().SetNdivisions(106)
hDice.SetStats(0)
hDice.SetFillStyle(1)
hDice.SetBarWidth(0.8)
hDice.SetBarOffset(0.1)
c.SetGrid(0,1)

sumOfDice = throw1+throw2
for i in range(len(sumOfDice)) :
  hDice.Fill( sumOfDice[i])

hDice.DrawCopy('b hist')
print('-----------')
c.Print('.png')
input('press enter to store histo and exit')
outfile=TFile.Open('histos.root',"RECREATE")
outfile.cd()
hDice.Write()
outfile.Close()

