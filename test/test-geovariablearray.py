# coding=UTF8

import unittest
import numpy.testing as npt
import data.core as c
reload(c)

class TestGeoVariableArray(unittest.TestCase):
    def test_getset(self):
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

        print "Testing get item method"
        npt.assert_almost_equal(a.data[1,2,2], a[1,2,2])
        npt.assert_almost_equal(a.data[(1,0),2,2], a[(1,0),2,2])
        npt.assert_almost_equal(a.data[0,(1,0),2], a[0,(1,0),2])
        npt.assert_almost_equal(a.data[0,1,(1,0)], a[0,1,(1,0)])



# print "a[(2,0),(0,2),(0,2)]"
# print a[(2,0),(0,2),(0,2)]
# print









if __name__ == "__main__":
    unittest.main()
