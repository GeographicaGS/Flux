# coding=UTF8

import flux.indarray as f
import numpy as np
reload(f)

i = f.Indarray(np.float, ["A","B"], A=["A0","A1"], B=["B0","B1"], 
               data=np.array([0,1,2,3]))

n = f.Indarray(np.float, ["An","Bn"], An=["A0","A1n"], Bn=["B0n","B1"], 
               data=np.array([0,1,2,3])+3)

print i()
print n()
print

i.merge(n)
