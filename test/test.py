# coding=UTF8

import data.core as c
import numpy as np
import numpy.random as nr
reload(c)


# array([[[56, 58, 35],          Data for ES
#         [95, 27,  1],          Rows are data for a year for all variables
#         [16,  7, 17]],         Columns are data for a variable for all years

#        [[20, 17, 50],          Data for EN
#         [20, 93, 55],
#         [77, 84, 29]],

#        [[16, 60, 19],          Data for US
#         [99, 33, 94],
#         [70, 51, 22]]])




b = np.array([0.0009,0.0019,0.0029, 
              0.0109,0.0119,0.0129, 
              0.0209,0.0219,0.0229, 
              0.1009,0.1019,0.1029, 
              0.1109,0.1119,0.1129, 
              0.1209,0.1219,0.1229, 
              0.2009,0.2019,0.2029, 
              0.2109,0.2119,0.2129, 
              0.2209,0.2219,0.2229]).reshape(3,3,3)

a = nr.randint(0,100,(6,7,3))

a[0,:,:]+=1000
a[1,:,:]+=100

# print "Initial data: "
# print a
# print

gva = c.GeoVariableArray(geoentity=["ES","EN","FR","US","NZ","NL"], 
                         time=["2011","2012","2013","2014","2015","2016","2017"], variable=["V0","V1","V2"],
                         data=a)

gva.cluster("V0", 40)
