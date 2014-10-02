# coding=UTF8

import unittest
import numpy.testing as npt
import flux.indarray as f
import numpy as np
reload(f)

class TestIndarray(unittest.TestCase):
    nda = None
    data = [0.0009,0.0019,0.0029, 
            0.0109,0.0119,0.0129, 
            0.0209,0.0219,0.0229, 
            0.1009,0.1019,0.1029, 
            0.1109,0.1119,0.1129, 
            0.1209,0.1219,0.1229, 
            0.2009,0.2019,0.2029, 
            0.2109,0.2119,0.2129, 
            0.2209,0.2219,0.2229]

    def restartData(self):
        self.nda = f.Indarray(np.float,
                              ["geoentity","time","variable"],
                              geoentity=["ES","EN","US"],
                              time=["2011","2012","2013"],
                              variable=["V0","V1","V2"], data=np.array(self.data))

    def test_initialise(self):
        i = f.Indarray(np.float, ["A","B"], A=["A0","A1"], B=["B0","B1"])
        npt.assert_array_equal(i(), np.array([np.nan,np.nan,np.nan,np.nan]).reshape(2,2))

        i = f.Indarray(np.float, ["A","B"], A=["A0","A1"], B=["B0","B1"], 
                       data=np.array([0,1,2,3]))
        npt.assert_array_equal(i(), np.array([0,1,2,3]).reshape(2,2))

        self.assertRaises(f.FluxException, f.Indarray, np.float, ["A","B"], 
                          A=["A0"], B=["B0","B1"], 
                          data=np.array([0,1,2,3]))

        self.assertRaises(f.FluxException, f.Indarray, np.float, ["A","B"], 
                          B=["B0","B1"], 
                          data=np.array([0,1,2,3]))

        self.assertRaises(f.FluxException, f.Indarray, np.float, ["A","B"], 
                          A=["A0"], B=["B0","B1"], 
                          data=[0,1,2,3])

    def test_addAxis(self):
        i = f.Indarray(np.float, ["A"], A=["A0"])
        npt.assert_array_equal(i(), np.array([np.nan]))
        i.addAxis("b", keys=["A","B"], data=np.array([0,1]))
        npt.assert_array_equal(i(), np.array([0,1]).reshape(1,2))
        i.addKey("A", keys=["A","B"], data=np.array([2,3,4,5]))
        npt.assert_array_equal(i(), np.array([[0, 1],
                                              [2, 3],
                                              [4, 5]]))

    def test_addKeys(self):
        i = f.Indarray(np.float, ["A","B"], A=["A0","A1"], B=["B0","B1"], 
                       data=np.array([0,1,2,3]))
        i.addKey("A", ["A2","A3"])
        self.assertEqual(i.keys("A"), ["A0","A1","A2","A3"])
        self.assertEqual(i.shape, [4,2])
        i.addKey("B", ["B2","B3"], data=np.array([[8,10],[9,11],[12,13],[14,15]]))
        self.assertEqual(i.keys("B"), ["B0","B1","B2","B3"])
        self.assertEqual(i.shape, [4,4])
        npt.assert_array_equal(i(), 
                               np.array([[0,1,8,10],[2,3,9,11],
                                         [np.nan,np.nan,12,13],[np.nan,np.nan,14,15]]))
        
    def test_generalProperties(self):
        self.restartData()
        self.assertEqual([x.name for x in self.nda.axis], ['geoentity', 'time', 'variable'])
        self.assertEqual(self.nda.shape, [3, 3, 3])
        self.assertEqual(self.nda.ndim, 3)
        self.assertEqual(len(self.nda), 27)
        self.assertEqual(self.nda.dtype, np.float)
        npt.assert_array_equal(self.nda.data, np.array(self.data).reshape(3,3,3))

    def test_getset(self):
        self.restartData()

        npt.assert_array_equal(np.array([0.1229]), self.nda[1,2,2])
        npt.assert_array_equal(np.array([0.1219,0.0129]), self.nda[(1,0),(2,1),(1,2)])
        npt.assert_array_equal(np.array([ 0.2229,  0.0009]), 
                               self.nda[("US","ES"),("2013","2011"),("V2","V0")])
        npt.assert_array_equal(self.nda.data, self.nda[:,:,:])
        npt.assert_array_equal(np.array([[[ 0.0009,  0.0019,  0.0029],
                                           [ 0.0109,  0.0119,  0.0129],
                                           [ 0.0209,  0.0219,  0.0229]],
                                          [[ 0.1009,  0.1019,  0.1029],
                                           [ 0.1109,  0.1119,  0.1129],
                                           [ 0.1209,  0.1219,  0.1229]]]), self.nda[0:2,:,:])
        npt.assert_array_equal(np.array([[[ 0.0109,  0.0119,  0.0129],
                                           [ 0.0209,  0.0219,  0.0229]],
                                          [[ 0.1109,  0.1119,  0.1129],
                                           [ 0.1209,  0.1219,  0.1229]]]), self.nda[0:2,1:3,:])
        npt.assert_array_equal(np.array([[[ 0.0109,  0.0119],
                                           [ 0.0209,  0.0219]],
                                          [[ 0.1109,  0.1119],
                                           [ 0.1209,  0.1219]]]), self.nda[0:2,1:3,0:2])
        npt.assert_array_equal(np.array([[[ 0.0129],
                                           [ 0.0229]],
                                          [[ 0.1129],
                                           [ 0.1229]]]), self.nda[0:2,1:3,2])
        npt.assert_array_equal(np.array([0.2119]), self.nda["US","2012","V1"])
        npt.assert_array_equal(np.array([0.0229]), self.nda[0,"2013",2])
        npt.assert_array_equal(np.array([ 0.0229,  0.0209]), self.nda[0,"2013",("V2","V0")])
        npt.assert_array_equal(np.array([[[ 0.1209,  0.1219],
                                           [ 0.1009,  0.1019]],
                                          [[ 0.2209,  0.2219],
                                           [ 0.2009,  0.2019]]]), self.nda[1:3,("2013","2011"),0:2])
        npt.assert_array_equal(np.array([[ 0.2119, 0.2219]]), self.nda["US",1:3,1])

        self.restartData()
        self.nda[1,2,1] = 0.1215
        npt.assert_array_equal(np.array([0.1215]), self.nda[1,2,1])

        self.restartData()
        self.nda[(1,0),(2,1),(1,2)] = np.array([0.1215,0.0125])
        npt.assert_array_equal(np.array([0.1215,0.0125]), self.nda[(1,0),(2,1),(1,2)])

        self.restartData()
        self.nda[("US","ES"),("2013","2011"),("V2","V0")] = np.array([0.2225,0.0005])
        npt.assert_array_equal(np.array([0.2225,0.0005]), self.nda[("US","ES"),("2013","2011"),("V2","V0")])

        self.restartData()
        self.nda[:,:,:] = 0
        npt.assert_array_equal(np.zeros((3,3,3)), self.nda[:,:,:])

        self.restartData()
        self.nda[0:2,:,:] = np.array([[[ 0.0005,  0.0015,  0.0025],
                                       [ 0.0105,  0.0115,  0.0125],
                                       [ 0.0205,  0.0215,  0.0225]],
                                      [[ 0.1005,  0.1015,  0.1025],
                                       [ 0.1105,  0.1115,  0.1125],
                                       [ 0.1205,  0.1215,  0.1225]]])
        npt.assert_array_equal(np.array([[[ 0.0005,  0.0015,  0.0025],
                                           [ 0.0105,  0.0115,  0.0125],
                                           [ 0.0205,  0.0215,  0.0225]],
                                          [[ 0.1005,  0.1015,  0.1025],
                                           [ 0.1105,  0.1115,  0.1125],
                                           [ 0.1205,  0.1215,  0.1225]]]), self.nda[0:2,:,:])

        self.restartData()
        self.nda["US","2012","V1"] = 0.2115
        npt.assert_array_equal(np.array([0.2115]), self.nda["US","2012","V1"])

        self.restartData()
        self.nda[0,"2013",2] = 0.0225
        npt.assert_array_equal(np.array([0.0225]), self.nda[0,"2013",2])

        self.restartData()
        self.nda[0,"2013",("V2","V0")] = np.array([ 0.0225,  0.0205])
        npt.assert_array_equal(np.array([ 0.0225,  0.0205]), self.nda[0,"2013",("V2","V0")])

        self.restartData()
        self.nda[1:3,("2013","2011"),0:2] = np.array([[[ 0.1205,  0.1215],
                                                       [ 0.1005,  0.1015]],
                                                      [[ 0.2205,  0.2215],
                                                       [ 0.2005,  0.2015]]])
        npt.assert_array_equal(np.array([[[ 0.1205,  0.1215],
                                           [ 0.1005,  0.1015]],
                                          [[ 0.2205,  0.2215],
                                           [ 0.2005,  0.2015]]]), self.nda[1:3,("2013","2011"),0:2])

        self.restartData()
        self.nda["US",1:3,1] = np.array([[ 0.2115, 0.2215]])
        npt.assert_array_equal(np.array([[ 0.2115, 0.2215]]), self.nda["US",1:3,1])

    def test_get(self):
        self.restartData()

        npt.assert_array_equal(np.array(self.data).reshape(3,3,3), self.nda.get((None,None,None)))
        npt.assert_array_equal(np.array([[[ 0.2129]]]), self.nda.get((2,1,2)))
        npt.assert_array_equal(self.nda.get(((2,0),1,(1,2))), 
                               np.array([[[ 0.2119,  0.2129]],
                                         [[ 0.0119,  0.0129]]]))
        npt.assert_array_equal(self.nda.get((("US","ES"),"2012",("V2","V0"))),
                               np.array([[[ 0.2129,  0.2109]],
                                         [[ 0.0129,  0.0109]]]))

    def test_set(self):
        self.restartData()
        newD = np.array([-1,-10])

        self.nda.set((("US","ES"),0,1), newD.reshape(2,1,1))
        npt.assert_array_equal(self.nda.get((("US","ES"),0,1)), newD.reshape(2,1,1))

    def test_sort(self):
        self.restartData()

        self.nda.sort("geoentity")
        npt.assert_array_equal(self.nda(), np.array([[[ 0.1009,  0.1019,  0.1029],
                                                      [ 0.1109,  0.1119,  0.1129],
                                                      [ 0.1209,  0.1219,  0.1229]],
                                                     [[ 0.0009,  0.0019,  0.0029],
                                                      [ 0.0109,  0.0119,  0.0129],
                                                      [ 0.0209,  0.0219,  0.0229]],
                                                     [[ 0.2009,  0.2019,  0.2029],
                                                      [ 0.2109,  0.2119,  0.2129],
                                                      [ 0.2209,  0.2219,  0.2229]]]))

    def test_merge(self):
        i = f.Indarray(np.float, ["A"], A=["A0","A1"], 
                       data=np.array([0,1]))
        n = f.Indarray(np.float, ["An","Bn"], An=["A0","A1n"], Bn=["B0n","B1"], 
                       data=np.array([0,1,2,3])+3)
        self.assertRaises(f.FluxException, i.merge, n)

        i = f.Indarray(np.int, ["A","B"], A=["A0","A1"], B=["B0","B1"],
                       data=np.array([0,1,2,3]))
        n = f.Indarray(np.float, ["An","Bn"], An=["A0","A1n"], Bn=["B0n","B1"], 
                       data=np.array([0,1,2,3])+3)
        self.assertRaises(f.FluxException, i.merge, n)

        i = f.Indarray(np.float, ["A","B"], A=["A0","A1"], B=["B0","B1"],
                       data=np.array([0,1,2,3]))
        n = f.Indarray(np.float, ["An","Bn"], An=["A0","A1n"], Bn=["B0n","B1"], 
                       data=np.array([0,1,2,3])+3)


        i.merge(n)



if __name__ == "__main__":
    unittest.main()
