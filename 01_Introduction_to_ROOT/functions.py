#!/usr/bin/python3
import math
from ROOT import *

cFunctions=TCanvas('cFunctions')
f1=TF1("f1","[0]*x*sin([1]*x)",0.,10.)
f1.SetParameter(0,5.)
f1.SetParameter(1,1.)
f1.SetLineColor(kYellow)
f1.DrawCopy()

f2=TF1('f2','gaus(x,[0..2])*expo(x,[3..4])',0.,10.)
f2.SetParameter(0,0.1)
f2.SetParameter(1,1.)
f2.SetParameter(2,1.)
f2.SetParameter(3,3.)
f2.SetParameter(4,1.)
f2.SetLineColor(kRed)
f2.DrawCopy('same')

def mySin(x, par):
    return par[0]*sin(par[1]*x[0])

f3 = TF1('f3',mySin, 0., 10., 2)
f3.SetParameter(0, 20.);
f3.SetParameter(1, 0.5);
f3.SetLineColor(kBlue)
f3.DrawCopy('same')

legend=TLegend(0.1,25,4.,40.,"","")
legend.AddEntry(f1,'[0]*x*sin([1]*x)')
legend.AddEntry(f2,'gaus(0)*expo(3)')
legend.AddEntry(f3,'mySin')
legend.Draw()

cFunctions.Update()
cFunctions.Print('.png')
input("press any key")
