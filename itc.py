#pip install scikit-dsp-comm

import sk_dsp_comm.fec_block as block
import numpy as np

n = int(input("Enter n: \t")) #Input the n,k values for a hamming code
k = int(input("Enter k: \t"))
parity = n-k

hh1 = block.fec_hamming(parity) #Instantiating a fec_hamming class instance(hh1)

print(f"\nn: {hh1.n} \nk: {hh1.k} \nGenerator Matrix:\n\n{hh1.G}") #n,k and generator matrix of the hamming code

msg_len = (2**hh1.k) - 1

msg_array = [x for x in range(msg_len+1)]
print(f"\nMessage array(Decimal Form): {msg_array}") #Creating a decimal message array

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
# print(code)
msg_len = (2**hh1.k)-1
Table = [] #Table of added codewords
for i in range(msg_len+1):
  for j in range(msg_len+1):
    Table.append(tostring(code[i,:]^code[j,:]))
# Table

code1 = [] #container to hold the original codewords in a string form
m,n = np.shape(code)
for i in range(m):
  code1.append(tostring(code[i,:]))
print(f"\nCodewords:\n{code1}")

Table_grid = np.array(Table) #Array to print a table
Table_grid.resize((2**hh1.k,2**hh1.k)) # Resize the table to (2^k + 1)x(2^k + 1)

#np.shape(Table_grid)

def gridprint(aray):
  '''Custom function to print the table with clear grid lines'''
  m,n = np.shape(aray)
  for i in range(0,m):
    for j in range(0,n):
      print(aray[i][j] + ' | ', end= '')
    print('\n---------------------------------------------------------------------------------------------------------------------------------------------------------------')
print("\nTable:\n")
gridprint(Table_grid) #Print the table
print("\n")

#Check if all elements in 'Table' are valid codewords(elements in 'code')
count = 0
bol = True
for i in range(len(Table)):
  if Table[i] in code1:
    print("Resultant codeword is valid")
  else:
    print("Not Valid")
    bol = False
if bol == True:
  print("\nAll codewords are valid.Hence proved.\n\n")