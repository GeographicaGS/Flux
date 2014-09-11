# coding=UTF8

import data.core as c
import numpy as np
reload(c)

a = np.array([0.0009,0.0019,0.0029, 
              0.0109,0.0119,0.0129, 
              0.0209,0.0219,0.0229, 
              0.1009,0.1019,0.1029, 
              0.1109,0.1119,0.1129, 
              0.1209,0.1219,0.1229, 
              0.2009,0.2019,0.2029, 
              0.2109,0.2119,0.2129, 
              0.2209,0.2219,0.2229]).reshape(3,3,3)

gva = c.GeoVariableArray(geoentity=["ES","EN","US"], time=["2011","2012","2013"], variable=["V0","V1","V2"],
                         data=a)

# geo = [
#     1,
#     (1,0),
#     ("US","EN"),
#     slice(None,None),
#     slice(0,2),
#     "US",
#     0,
#     ["US","EN"],
#     0,
#     slice(1,3),
#     "US"
# ]

# time = [
#     2,
#     (2,1),
#     ("2012","2011"),
#     slice(None,None),
#     slice(None,None),
#     "2012",
#     "2013",
#     0,
#     "2013",
#     ["2013","2011"],
#     slice(1,3)
# ]

# var = [
#     2,
#     (1,2),
#     ("V1","V0"),
#     slice(None,None),
#     slice(None,None),
#     "V1",
#     2,
#     slice(None,None),
#     ["V2","V0"],
#     slice(0,2),
#     1
# ]

# value = [
#     0,
#     [100,10],
#     [100,10],
#     np.array([0,0,0,
#               0,0,0,
#               0,0,0,
#               0,0,0,
#               0,0,0,
#               0,0,0,
#               0,0,0,
#               0,0,0,
#               0,0,0]).reshape(3,3,3),
#     np.array([0,0,0,0,0,0,0,0,0,
#               0,0,0,0,0,0,0,0,0]).reshape(2,3,3),
#     0,
#     0,
#     np.array([0,0,0,0,0,0]).reshape(2,1,3),
#     np.array([0,0]).reshape(1,1,2),
#     np.array([0,0,0,0,0,0,0,0]).reshape(2,2,2),
#     np.array([0,0]).reshape(1,2,1)
# ]


# for i in range(len(geo)):
#     print "---------------------"

#     gva = c.GeoVariableArray(geoentity=["ES","EN","US"], time=["2011","2012","2013"], variable=["V0","V1","V2"],
#                              data=a)
#     print gva[geo[i],time[i],var[i]] 
#     print
#     gva[geo[i],time[i],var[i]] = value[i]
#     print gva[geo[i],time[i],var[i]] 
#     print

