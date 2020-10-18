# -*- coding: utf-8 -*-
"""ITC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MPFL61mhS-24ACDxZzn5FLbxU3rOd3Dh
"""

# pip install scikit-dsp-comm - Required library

import sk_dsp_comm.fec_block as block
import numpy as np
import pandas as pd
from IPython import display

n = int(input("Enter n: \t")) #Input the n,k values for a hamming code
k = int(input("Enter k: \t"))
parity = n-k

hh1 = block.fec_hamming(parity) #Instantiating a fec_hamming class instance(hh1)

print(f"n: {hh1.n} \nk: {hh1.k}\nGenerator Matrix:\n{hh1.G}") #n,k and generator matrix of the hamming code

msg_len = (2**hh1.k) - 1

msg_array = [x for x in range(msg_len+1)]
print(f"Message array(Decimal Form): {msg_array}") #Creating a decimal message array

def dToBi(n):
  '''Returns a fixed length binary bit array for a given message'''  
  return bin(n).replace("0b","").zfill(hh1.k) 
def tostring(aray):
  '''Converts a bit array to a string'''
  string = ''
  aray = aray.tolist()
  for i in range(len(aray)):
    string = string + str(aray[i])
  return string

def ham(msg):
  '''Returns a hamming encoded message for a given input message'''
  x = np.array([int(a) for a in dToBi(msg)])
  y = hh1.hamm_encoder(x)
  y = np.array([int(a) for a in y])
  return y

code = [] #Empty list to hold codewords 
for i in msg_array:
  code.append(ham(i))
code = np.array(np.concatenate(code, axis=0)) #Concatenate the codeword(list to string)
code.resize((2**hh1.k,hh1.n)) #Resize the codeword list
msg_len = (2**hh1.k)-1
Table = [] #Table of added codewords
for i in range(msg_len+1):
  for j in range(msg_len+1):
    Table.append(tostring(code[i,:]^code[j,:]))

code1 = [] #container to hold he original codewords in a string form
m,n = np.shape(code)
for i in range(m):
  code1.append(tostring(code[i,:]))
print(f"Codewords:\n{code1}") #All possible codewords

Table_grid = np.array(Table) #Array to print a table
Table_grid.resize((2**hh1.k,2**hh1.k)) # Resize the table to (2^k + 1)x(2^k + 1)

np.shape(Table_grid)

Table_grid = pd.DataFrame(Table_grid, index = code1, columns = code1)
print("Table:\n")
display.display(Table_grid)

"""Property 1: The all zero codeword is always a codeword."""
print("\n\nProperty 1: ")
print('0000000' in code1)

"""Property 2: The sum of two codewords belonging to the code is also a codeword belonging to the code."""

#Check if all elements in 'Table' are valid codewords(elements in 'code')
bol = True
for i in range(len(Table)):
  if Table[i] in code1:
    print("Resultant codeword is valid")
  else:
    print("Not Valid")
    bol = False
if bol == True:
  print("\nAll codewords are valid.Hence proved.")

"""Property 3: The minimum Hamming distance between two codewords of a linear block code is equal to the minimum Hammingweight of any non-zero codeword, i.e., d* = w*."""

code_xor = []
for i in range(msg_len+1):
  for j in range(msg_len+1):
    if i == j:
      continue
    code_xor.append(np.count_nonzero(code[i,:]^code[j,:]))
min_dist = np.min(code_xor) #Minimum hamming distance
weights = []
for i in range(1, msg_len+1):
  weights.append(np.count_nonzero(code[i,:]^code[0,:])) #Excluded all zeros as weight will be zero
min_weight = np.min(weights)

print("\nProperty 3: ")
print(min_weight == min_dist)