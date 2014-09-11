# coding=UTF8

import unittest
import numpy.testing as npt
import numpy as np
import data.core as c
reload(c)

class TestGeoVariableArray(unittest.TestCase):
    nda = None

    def restartData(self):
        data=[0.0009,0.0019,0.0029, 
              0.0109,0.0119,0.0129, 
              0.0209,0.0219,0.0229, 
              0.1009,0.1019,0.1029, 
              0.1109,0.1119,0.1129, 
              0.1209,0.1219,0.1229, 
              0.2009,0.2019,0.2029, 
              0.2109,0.2119,0.2129, 
              0.2209,0.2219,0.2229]

        self.nda = c.GeoVariableArray(geoentity=["ES","EN","US"], time=["2011","2012","2013"],
                                      variable=["V0","V1","V2"], data=data)

    def test_getset(self):
        self.restartData()


        print "Testing get item method by integer indices"
        npt.assert_almost_equal(np.array([0.1229]), self.nda[1,2,2])


        print "Testing get item method by tuples"
        npt.assert_almost_equal(np.array([0.1219,0.0129]), self.nda[(1,0),(2,1),(1,2)])

        npt.assert_almost_equal(np.array([ 0.2229,  0.0009]), 
                                self.nda[("US","ES"),("2013","2011"),("V2","V0")])

        
        print "Testing get item method by slices"
        npt.assert_almost_equal(self.nda.data, self.nda[:,:,:])

        npt.assert_almost_equal(np.array([[[ 0.0009,  0.0019,  0.0029],
                                           [ 0.0109,  0.0119,  0.0129],
                                           [ 0.0209,  0.0219,  0.0229]],
                                          [[ 0.1009,  0.1019,  0.1029],
                                           [ 0.1109,  0.1119,  0.1129],
                                           [ 0.1209,  0.1219,  0.1229]]]), self.nda[0:2,:,:])

        npt.assert_almost_equal(np.array([[[ 0.0109,  0.0119,  0.0129],
                                           [ 0.0209,  0.0219,  0.0229]],
                                          [[ 0.1109,  0.1119,  0.1129],
                                           [ 0.1209,  0.1219,  0.1229]]]), self.nda[0:2,1:3,:])

        npt.assert_almost_equal(np.array([[[ 0.0109,  0.0119],
                                           [ 0.0209,  0.0219]],
                                          [[ 0.1109,  0.1119],
                                           [ 0.1209,  0.1219]]]), self.nda[0:2,1:3,0:2])

        npt.assert_almost_equal(np.array([[[ 0.0129],
                                           [ 0.0229]],
                                          [[ 0.1129],
                                           [ 0.1229]]]), self.nda[0:2,1:3,2])

        
        print "Testing get item method by strings"
        npt.assert_almost_equal(np.array([0.2119]), self.nda["US","2012","V1"])

        npt.assert_almost_equal(np.array([0.0229]), self.nda[0,"2013",2])


        print "Testing get item method by mixed index types"
        npt.assert_almost_equal(np.array([ 0.0229,  0.0209]), self.nda[0,"2013",("V2","V0")])

        npt.assert_almost_equal(np.array([[[ 0.1209,  0.1219],
                                           [ 0.1009,  0.1019]],
                                          [[ 0.2209,  0.2219],
                                           [ 0.2009,  0.2019]]]), self.nda[1:3,("2013","2011"),0:2])

        npt.assert_almost_equal(np.array([[ 0.2119, 0.2219]]), self.nda["US",1:3,1])


        print "Testing set item by integer indices"
        self.restartData()
        self.nda[1,2,1] = 0.1215
        npt.assert_almost_equal(np.array([0.1215]), self.nda[1,2,1])

        print "Testing set item by tuples"
        self.restartData()
        self.nda[(1,0),(2,1),(1,2)] = np.array([0.1215,0.0125])
        npt.assert_almost_equal(np.array([0.1215,0.0125]), self.nda[(1,0),(2,1),(1,2)])

        self.restartData()
        self.nda[("US","ES"),("2013","2011"),("V2","V0")] = np.array([0.2225,0.0005])
        npt.assert_almost_equal(np.array([0.2225,0.0005]), self.nda[("US","ES"),("2013","2011"),("V2","V0")])


        print "Testing set item by slices"
        self.restartData()
        self.nda[:,:,:] = 0
        npt.assert_almost_equal(np.zeros((3,3,3)), self.nda[:,:,:])

        self.restartData()
        self.nda[0:2,:,:] = np.array([[[ 0.0005,  0.0015,  0.0025],
                                       [ 0.0105,  0.0115,  0.0125],
                                       [ 0.0205,  0.0215,  0.0225]],
                                      [[ 0.1005,  0.1015,  0.1025],
                                       [ 0.1105,  0.1115,  0.1125],
                                       [ 0.1205,  0.1215,  0.1225]]])
        npt.assert_almost_equal(np.array([[[ 0.0005,  0.0015,  0.0025],
                                           [ 0.0105,  0.0115,  0.0125],
                                           [ 0.0205,  0.0215,  0.0225]],
                                          [[ 0.1005,  0.1015,  0.1025],
                                           [ 0.1105,  0.1115,  0.1125],
                                           [ 0.1205,  0.1215,  0.1225]]]), self.nda[0:2,:,:])


        print "Testing set item by strings"
        self.restartData()
        self.nda["US","2012","V1"] = 0.2115
        npt.assert_almost_equal(np.array([0.2115]), self.nda["US","2012","V1"])

        self.restartData()
        self.nda[0,"2013",2] = 0.0225
        npt.assert_almost_equal(np.array([0.0225]), self.nda[0,"2013",2])


        print "Testing set item by mixed index types"
        self.restartData()
        self.nda[0,"2013",("V2","V0")] = np.array([ 0.0225,  0.0205])
        npt.assert_almost_equal(np.array([ 0.0225,  0.0205]), self.nda[0,"2013",("V2","V0")])

        self.restartData()
        self.nda[1:3,("2013","2011"),0:2] = np.array([[[ 0.1205,  0.1215],
                                                       [ 0.1005,  0.1015]],
                                                      [[ 0.2205,  0.2215],
                                                       [ 0.2005,  0.2015]]])
        npt.assert_almost_equal(np.array([[[ 0.1205,  0.1215],
                                           [ 0.1005,  0.1015]],
                                          [[ 0.2205,  0.2215],
                                           [ 0.2005,  0.2015]]]), self.nda[1:3,("2013","2011"),0:2])

        self.restartData()
        self.nda["US",1:3,1] = np.array([[ 0.2115, 0.2215]])
        npt.assert_almost_equal(np.array([[ 0.2115, 0.2215]]), self.nda["US",1:3,1])








        


        # TODO: test for select and __setitem__















        # print "Testing get item method by lists"
        # npt.assert_almost_equal(np.array([[[ 0.0209,  0.0219,  0.0229],
        #                                    [ 0.0009,  0.0019,  0.0029]],
        #                                   [[ 0.1209,  0.1219,  0.1229],
        #                                    [ 0.1009,  0.1019,  0.1029]],
        #                                   [[ 0.2209,  0.2219,  0.2229],
        #                                    [ 0.2009,  0.2019,  0.2029]]]).reshape(3,2,3), self.nda[:,["2013","2011"],:])
        # npt.assert_almost_equal(np.array([[[ 0.2229,  0.2209],
        #                                    [ 0.2029,  0.2009]],
        #                                   [[ 0.0229,  0.0209],
        #                                    [ 0.0029,  0.0009]]]).reshape(2,2,2), 
        #                         self.nda[["US","ES"],["2013","2011"],["V2","V0"]])




        # npt.assert_almost_equal(np.array([[[ 0.2009,  0.2019,  0.2029],
        #                                    [ 0.2109,  0.2119,  0.2129],
        #                                    [ 0.2209,  0.2219,  0.2229]],
        #                                   [[ 0.0009,  0.0019,  0.0029],
        #                                    [ 0.0109,  0.0119,  0.0129],
        #                                    [ 0.0209,  0.0219,  0.0229]]]), self.nda[["US","ES"],:,:])






        

        # print "Testing set item methods by integers"
        # self.nda[0,0,0] = 9
        # npt.assert_almost_equal(np.array([[[9]]]), self.nda[0,0,0])







if __name__ == "__main__":
    unittest.main()
