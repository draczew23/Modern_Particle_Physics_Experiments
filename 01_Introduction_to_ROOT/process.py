#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from ROOT import *
from array import array

## A C/C++ structure is required, to allow memory based access
gROOT.ProcessLine(
   "struct Vertex_t {\
    Int_t id;\
    Double_t x,y,z; \
    double perp() { return sqrt(x*x+y*y); } \
};")
lvec=TLorentzVector()
gRandom.SetSeed(2022)
vertex = Vertex_t()
pid = array('i',[0])

f = TFile('myTree.root','RECREATE')
myTree  = TTree('myTree','simple tree with vertex data')
myTree.Branch('vertex',vertex)
myTree.Branch('pid',pid,'pid/I')
myTree.Branch('lvec',lvec)
for i in range(100) :
  pid[0] = gRandom.Integer(100)
  vertex.id = i
  vertex.x = gRandom.Uniform(10.)
  vertex.y = gRandom.Uniform(10.)
  vertex.z = gRandom.Uniform(200.)
  lvec.SetXYZT(vertex.x,vertex.y,vertex.z,0.)
  
  print ('vertex id:{0:3d}, perp={1:5.2f}'.format(vertex.id,vertex.perp()))
  myTree.Fill()       
myTree.Print("all")
f.Write()
f.Close()  