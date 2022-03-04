import sys

def readData(fileName, throw1, throw2) :
  file = open(fileName,'r')
  for line in file:
    columns = line.strip().split()
    r1 = int(columns[0])
    r2 = int(columns[1])
    throw1.append(r1)
    throw2.append(r2)
  return

