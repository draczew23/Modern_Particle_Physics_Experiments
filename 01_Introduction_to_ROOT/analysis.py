#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ROOT import *
from array import array
gROOT.ProcessLine(
 "struct Vertex_t {\
    Int_t id;\
    Double_t x,y,z; \
    double perp() { return sqrt(x*x+y*y); } \
};")
pid=array('i',[0])
lvec=TLorentzVector()
myVert=Vertex_t()

myChain=TChain('myTree')
myChain.Add('myTree.root')
myChain.SetBranchAddress("vertex",myVert)
myChain.SetBranchAddress("pid",pid)
myChain.SetBranchAddress("lvec",lvec)
nEntries = myChain.GetEntries()
for iev in range (nEntries) :
  myChain.GetEntry(iev)
  print ('vertex: ',pid[0],myVert.id, myVert.z,myVert.perp(),lvec.Perp())
print ('entires:',nEntries)