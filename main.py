import sys
import numpy as np

#open netlist text file given as argv[1]
f = open(sys.argv[1])
#split file in a list of strings using 
textFile = f.read().split('\n')
#remove empty lines from list
textFile = list( filter(lambda x:x !='', textFile) )
#remove comments from list
netlist = list( filter(lambda x:x[0] !='*', textFile))

#count total number of nodes
nodeCount = 0

#map each string from list into an array of netlist parameters as strings
for i in range(len(netlist)):
  netlist[i] = netlist[i].split()

#transform every parameter into integer and floats and count number of nodes
for i in range(len(netlist)):
  if(netlist[i][0][0] == 'R'):
    aux = netlist[i]
    aux[1] = np.uintc(aux[1])
    aux[2] = np.uintc(aux[2])
    aux[3] = np.double(aux[3])
    #swap nodes if a > b
    if(aux[1] > aux[2]):
      aux[1], aux[2] = aux[2], aux[1]
    #count node value
    if(aux[2] > nodeCount):
      nodeCount = aux[2]

  elif(netlist[i][0][0] == 'I'):
    aux = netlist[i]
    aux[1] = np.uintc(aux[1])
    aux[2] = np.uintc(aux[2])
    aux[4] = np.double(aux[4])
    #swap nodes if a > b and multiply value by -1
    if(aux[1] > aux[2]):
      aux[1], aux[2] = aux[2], aux[1]
      aux[4] = np.multiply(-1, aux[4])
    #count node value
    if(aux[2] > nodeCount):
      nodeCount = aux[2]

  elif(netlist[i][0][0] == 'G'):
    aux = netlist[i]
    aux[1] = np.uintc(aux[1])
    aux[2] = np.uintc(aux[2])
    aux[3] = np.uintc(aux[3])
    aux[4] = np.uintc(aux[4])
    aux[5] = np.double(aux[5])
    #swap nodes if a > b and multiply value by -1
    if(aux[1] > aux[2]):
      aux[1], aux[2] = aux[2], aux[1]
      aux[5] = np.multiply(-1, aux[5])
      #swap nodes if c > d and multiply value by -1
    if(aux[3] > aux[4]):
      aux[3], aux[4] = aux[4], aux[3]
      aux[5] = np.multiply(-1, aux[5])
    #count node value
    if(aux[2] > nodeCount):
      nodeCount = aux[2]
    #count node value
    if(aux[4] > nodeCount):
      nodeCount = aux[4]

Gn = np.zeros((nodeCount+1, nodeCount+1))
I = np.zeros(nodeCount+1)

print(Gn)
print(I)

print(netlist)

for i in range(len(netlist)):
  aux = netlist[i]
  #insert resistor stamp
  if(aux[0][0] == 'R'):
    a = aux[1]
    b = aux[2]
    conductance = np.double(1/aux[3])
    Gn[a][a] = Gn[a][a] + conductance
    Gn[a][b] = Gn[a][b] - conductance
    Gn[b][a] = Gn[b][a] - conductance
    Gn[b][b] = Gn[b][b] + conductance
  #insert currentSource stamp
  elif(aux[0][0] == 'I'):
    print(aux)
    a = aux[1]
    b = aux[2]
    # i represents current value from source, not an index variable
    i = aux[4]
    I[a] = I[a] - i
    I[b] = I[b] + i
    print(I)
  #insert controledCurrentSource stamp
  elif(aux[0][0] == 'G'):
    a = aux[1]
    b = aux[2]
    c = aux[3]
    d = aux[4]
    value = aux[5]
    Gn[a][c] = Gn[a][c] + value
    Gn[a][d] = Gn[a][d] - value
    Gn[b][c] = Gn[b][c] - value
    Gn[b][d] = Gn[b][d] + value

print(Gn,I)

#remove ground line/column
Gn = Gn[1:,1:]
I = I[1:]

print(Gn,I)

def solve(Gn, I ):
  e = (np.linalg.inv(Gn)).dot(I)
  e2 = np.linalg.solve(Gn,I)
  return e2

e = solve(Gn,I)
print(e)
