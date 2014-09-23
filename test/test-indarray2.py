# coding=UTF8

import flux.indarray as f
import numpy as np
reload(f)

b = np.array([0.0009,0.0019,0.0029, 
              0.0109,0.0119,0.0129, 
              0.0209,0.0219,0.0229, 
              0.1009,0.1019,0.1029, 
              0.1109,0.1119,0.1129, 
              0.1209,0.1219,0.1229, 
              0.2009,0.2019,0.2029, 
              0.2109,0.2119,0.2129, 
              0.2209,0.2219,0.2229]).reshape(3,3,3)

# ind = f.Indarray()

# ind = f.Indarray(axeorder=["a","b","c"])

# ind = f.Indarray(axeorder=["a","b","c"], a=[1,2,3,4,8], b=["a","b","k"], c=[3,2,1])

ind = f.Indarray(axeorder=["geoentity","time","variable"], 
                 geoentity=["ES","EN","FR"], 
                 time=["2015","2012","2013"],
                 variable=["V4","V1","V2"],
                 data=b)

print "ind(): ", ind()
print "A : ", [x.name for x in ind.axis]
print "B : ", ind.keys("geoentity")

print "C : ", ind.axis
print "D : ", ind.size

print "E : ", ind.data


print "F :", ind[0,0,0]
print "G :", ind["ES","2012","V2"]
print "H :", ind[0:2,"2015",(0,2)]
# ind[0,"2011",0] = 44
print "I :", ind[0,"2015",0]
print "J :", ind()
print "K :", ind.select((0,1,2))
print "L :", ind.select((("ES","FR"),None,("V1","V4")))
# print ind[("ES","2012",slice(None,None))]
print "M :", ind.sort(0), ind.sort(1), ind.sort(2)
print "N :", ind.addKey("geoentity", "ii")
