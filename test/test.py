# coding=UTF8

import data.core as c
import numpy as np
reload(c)


a = c.GeoVariableArray(geoentity=["ES","EN","US"], time=["2011","2012","2013"], variable=["V0","V1","V2"],
                       data=[0.000,0.001,0.002, 
                             0.010,0.011,0.012, 
                             0.020,0.021,0.022, 
                             0.100,0.101,0.102, 
                             0.110,0.111,0.112, 
                             0.120,0.121,0.122, 
                             0.200,0.201,0.202, 
                             0.210,0.211,0.212, 
                             0.220,0.221,0.222])


# print a[1,2,2]
# print a[(2,0),(0,2),(0,2)]

print a[0,0,1]
