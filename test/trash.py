# coding=UTF8

import unittest
import numpy.testing as npt
import flux.indarray as f
import numpy as np
reload(f)

data = [0.0009,0.0019,0.0029, 
        0.0109,0.0119,0.0129, 
        0.0209,0.0219,0.0229, 
        0.1009,0.1019,0.1029, 
        0.1109,0.1119,0.1129, 
        0.1209,0.1219,0.1229, 
        0.2009,0.2019,0.2029, 
        0.2109,0.2119,0.2129, 
        0.2209,0.2219,0.2229]

nda = f.Indarray(np.float64, 
                 ["geoentity","time","variable"],
                 geoentity=["ES","EN","US"],
                 time=["2011","2012","2013"],
                 variable=["V0","V1","V2"],
                 data=np.array(data))

print nda[[2,0],(1,0),0]
print
print nda[(2,0),(1,0),0]
print

# zero = np.zeros((1,3,1))

# nda.set(("US",None,0), zero)



