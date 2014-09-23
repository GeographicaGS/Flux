# coding=UTF8

import flux.indarray as f
import numpy as np
reload(f)

i = f.Indarray(dtype=np.float)

print "A :", i()

i.addAxis("a", keys=["A","B","C"], data=np.array([0,1,2]))

print "B :", i()

i.addAxis("b", keys=["A","B"], data=np.array([0,1,2,3,4,5]))

print "C :", i()
