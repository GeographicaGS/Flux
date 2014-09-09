# coding=UTF8

import data.core as c
import numpy as np
reload(c)

# Index matrices in a reverse way. a["ES","2011","V0"] is 0.000, while a["ES","2011","V2"] is 0.002. 

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

# Order in the flat matrix is as follows:
# data=[0.000,0.001,0.002,      # ES data for year 2011 for the three variables
#       0.010,0.011,0.012,      # ES data for year 2012 for the three variables
#       0.020,0.021,0.022,      # ES data for year 2013 for the three variables
#       0.100,0.101,0.102,      # EN data for year 2011 for the three variables
#       0.110,0.111,0.112,      # EN data for year 2012 for the three variables
#       0.120,0.121,0.122,      # EN data for year 2013 for the three variables
#       0.200,0.201,0.202,      # US data for year 2011 for the three variables
#       0.210,0.211,0.212,      # US data for year 2012 for the three variables
#       0.220,0.221,0.222])     # US data for year 2013 for the three variables

# print a.shape

# print a()
# print 

# print a[0,0,0]
# print
# print a[("US","ES"),("2013","2011"),("V2","V0")]
# print

# print "AA"
# a["US","2013","V0"] = 1.220
# print a["US","2013","V0"]
# print

# print "BB"
# a[("US","ES"),"2011","V0"] = [2.200, \
#                               2.000]
# print a[("US","ES"),"2011","V0"]
# print

# print "CC"
# a["US","2011",("V0","V2")] = [3.200,3.202]
print a[("US","ES"),"2011","V0"]
print
print a["US",("2011","2013"),"V0"]
print
print a["US","2011",("V0","V2")]
print
print a[("US","ES"),"2011",("V0","V2")]
print
print a[("US","ES"),("2011","2013"),("V0","V2")]
print

# print "CC"
# e = np.array([3.012,3.212,3.220,3.222,3.010,3.210,3.020,0.220]).reshape((2,2,2))
# print e
# print 
# a[("US","ES"),("2012","2013"),("V0","V2")] = e
# print a[("US","ES"),("2012","2013"),("V0","V2")].flatten()


# print



# # print '000 : x[:,:,:]'
# # print x[:,:,:]
# # print
# # print '010 : x[0,0,2]'
# # print x[0,0,2]
# # print
# # print '020 : x[0:1, 0:2, 1:3]'
# # print x[0:1, 0:2, 1:3]
# # print
# # print '030 : x[(0,1), 1, (0,2)]'
# # print x[(0,1), 1, (0,2)]
# # print
# # print '040 : x["DE", 0, "V0"]'
# # print x["DE", 0, "V0"]
# # print
# # print '050 : x[("DE", "ES"), 1, ("V0", "V2")]'
# # print x[("DE", "ES"), 1, ("V0", "V2")]
# # print
# # print '055 : x[:,"2012-7-1",:]'
# # print x[:,"2012-7-1",:]
# # print
# # print '060 : x[("ES"), lambda x: x/c.Time("2011-7-1"), ("V2")]'
# # print x[("ES"), lambda x: x/c.Time("2012-7-1"), ("V2")]
# # print
# # print '070 : x[("US", "ES"), "2011-7-1", ("V0", "V2")]'
# # print x[("US", "ES"), "2011-7-1", ("V0", "V2")]
# # print
# # print '080 : x["DE", c.Time("2011-7-1"), "V2"]'
# # print x["DE", c.Time("2011-7-1"), "V2"]
# # print
