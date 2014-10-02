# coding=UTF8

# ----------------------------------------------
# Indarray object: ndarray with OO axes indexing
# ----------------------------------------------

import numpy as np
import arrayops

class _axis(object):
    """Internal axis object."""
    _name = None
    _keys = None

    def __init__(self, name, keys=None):
        self._name = name
        self._keys = keys if keys is not None else []

    def __len__(self):
        return len(self._keys)

    def __getitem__(self, key):
        """Gets an item."""
        return self._keys[key]

    def __setitem__(self, key, value):
        """Sets an item."""
        self._keys[key]=value

    @property
    def name(self):
        return self._name

    @property
    def keys(self):
        return self._keys

    def append(self, key):
        self._keys.append(key)



class Indarray(object):
    """The Indarray object is a wrapper for a Numpy ndarray whose axes are
    indexed and accessed by arrays of objects. The constructor may
    take any number of key arguments, representing the axes and the
    objects that index them. Two named key arguments are expected,
    however:

    dtype: data type for the array, in np types, defaults to float

    axis: this is mafndatory if axis are being passed. Is the
    dimensional order for the given indices, list of strings;
 
    foo / bar: the name of the indices, followed by an array of index
    objects;

    data: optional, an ndarray that will be reshaped and that
    represents the initial data;

    Objecst that serves as indices must be hashableables.

    """
    _data = None
    _dtype = None
    _axis = None

    def __init__(self, dtype, axis, **kwargs):
        """Constructor."""
        self._axis = []
        self._dtype = dtype

        # Add axes
        for i in axis:
            if i in kwargs:
                self.addAxis(i, keys=kwargs[i])
            else:
                raise FluxException("Index objects not found for axis "+i+".")
                
        # Initialise data, if any
        if "data" in kwargs:
            if not isinstance(kwargs["data"], np.ndarray):
                raise FluxException("Data must by a numpy.ndarray.")
            if len(self)!=len(kwargs["data"]):
                raise FluxException("Given data doesn't match axis dimensions.")
            self._data = kwargs["data"].reshape(self.shape)
        else:
            self._data = np.empty(self.shape)
            self._data[:] = np.nan

    def addAxis(self, name, keys=None, data=None):
        """Adds axis to the array:
        
        name: a string
        keys: initial keys
        data: a np.ndarray with data

        WARNING! This function destroys existing data.
        """
        if keys is not None:
            if len(keys)!=len(set(keys)):
                raise FluxException("Axis keys for axis "+name+" are invalid.")

        self._axis.append(_axis(name, keys=keys))

        if data is not None:
            self._data = data.reshape(self.shape)
        else:
            self._data = np.empty(self.shape, dtype=self._dtype)
            self._data[:] = np.nan

    def __call__(self):
        """Returns the data array."""
        return self._data

    @property
    def axis(self):
        """Return a list with the names of the axis."""
        return self._axis

    @property
    def dtype(self):
        """Data type."""
        return self._dtype

    @property
    def shape(self):
        """Returns shape based on the keys of indices."""
        return [len(x) for x in self._axis]

    @property
    def ndim(self):
        """Returns number of dimensions."""
        return len(self._axis)

    def __len__(self):
        """Returns size based on the keys of indices."""
        if self._axis==[]:
            return 0
        size = 1
        for i in self._axis:
            size*=len(i)

        return size

    @property
    def data(self):
        """Returns the data ndarray."""
        return self._data

    def __getitem__(self, key):
        """Gets data directly from the internal ndarray. Supported indices:
        
        slices: 1:2
        integers: 2
        tuples: (2,1)
        string indices: "US", "2013", "V0"
        string tuples: ("US","ES")
        TODO: callables to generate tuples

        ^^ With the above traditional Numpy indexing is made. If any
        element of the key is a list, special indexing is made.

        TODO HERE: getting rid of set / get and placing all indexing
        functions in _getitem_ / _setitem_ >> Continue

        """
        sp = any([isinstance(x, list) for x in key])

        if sp is False:
            fKey = ()
            for i in range(len(key)):
                fKey+=(self._analyzeKey(self._axis[i],key[i]),)

            out = self._data[fKey]
        else:
            import ipdb
            ipdb.set_trace()

            out = self._data
            i = self.ndim-1
        
            while i>=0:
                fKey = ()
                for t in range(i):
                    fKey+=(slice(None,None),)
                fKey+=(self._analyzeKey(self._axis[i],key[i]),)
                out = out[fKey]
                i-=1

        return out


    def __setitem__(self, key, value):
        """Set item.

        Value can be a np.ndarray that matches the key. For example,
        in a GeoVariableArray with 4 geoentities and 7 times:

        gva[:,"2010","Var 1"]=np.array([0,1,2,3])

        should set the values for 2010 for the 4 geoentities to the
        given values.

        TODO: Try slices with steps

        """
        fKey = ()
        for i in range(len(key)):
            fKey+=(self._analyzeKey(self._axis[i],key[i]),)

        self._data[fKey] = value

    def keys(self, axis):
        """Returns a list with the keys of the given axis (index, name or the axis object itself)."""
        return self._getAxis(axis).keys

    def addKey(self, axis, keys, data=None):
        """Inserts a new key into the given axis.
        
        axis: the index, the name or the axis object to add the key to;
        key: the key.

        TODO: add data to matrix.
        """
        axis = self._getAxis(axis)
        axisIndex = self._axis.index(axis)
        oldDim = self.shape[axisIndex]
        for i in keys:
            axis.append(i)

        diffDim = self.shape[axisIndex]-oldDim
        dims = self.shape
        dims[axisIndex] = diffDim

        if data is None:
            dataA = np.empty(dims)
            dataA[:] = np.nan
            self._data = np.append(self._data, dataA, axis=axisIndex).reshape(self.shape)
        else:
            self._data = np.append(self._data, data.reshape(dims), axis=axisIndex).reshape(self.shape)

    def _getAxis(self, id):
        """Returns the given axis. It may be addressed by name (string), by
        position (integer), or just by the axis object itself."""
        try:
            return id if isinstance(id, _axis) else self._axis[id] if isinstance(id, int) else \
                [x for x in self._axis if x.name==id][0]
        except:
            raise FluxException("Unknown axis addressed by ID "+str(id)+" ("+str(type(id))+").")

    def get(self, key):
        """Returns selected data. In a tuple, indices can be:

        integers: 2
        strings: "US", "2013", "V0"
        tuples of mixed above
        None: all, like slice :

        """
        out = self._data.view()
        i = self.ndim-1
        
        while i>=0:
            fKey = ()
            for t in range(i):
                fKey+=(slice(None,None),)
            fKey+=(self._analyzeKey(self._axis[i],key[i]),)
            out = out[fKey]
            i-=1
         
        import ipdb
        ipdb.set_trace()
   
        return out

    def set(self, key, data):
        """Sets given data to the selected ones. In a tuple, indices can be:
       
        integers: 2
        strings: "US", "2013", "V0"
        tuples of mixed above
        None: all, like slice :

        data is a Numpy ndarray of the same size and shape of the selected data.

        """
        if len(key)!=data.ndim:
            raise FluxException("Key and data should have the same dimension.")

        fKey = ()
        for t in range(self.ndim):
            fKey+=(self._analyzeKey(self._axis[t],key[t]),)

        import ipdb
        ipdb.set_trace()

        self._data[fKey] = data

        # it = np.nditer(data, flags=["multi_index"])
        # while not it.finished:

        #     for t in range(self.ndim):
        #         fKey+=(self._analyzeKey(self._axis[t],key[t][it.multi_index[t]]),)
        #     self._data[fKey] = it.value

        #     it.iternext()
        
    def _analyzeKey(self, axis, key):
        """Analyses a key for get/set.

        TODO: implement callable (to create tuples)
        """
        axis = self._getAxis(axis)

        if isinstance(key, list):
            key = tuple(key)

        if key is None:
            return slice(None, None)

        if isinstance(key, (slice)):
            return key

        key = (key,) if not isinstance(key, tuple) else key
        out = ()

        for i in key:
            if isinstance(i, int):
                out += (i,)
            if isinstance(i, str):
                try:
                    out += (axis.keys.index(i),)
                except:
                    raise FluxException("Cannot find key "+str(key)+" in axis "+axis.name+".")

        return out

    def getSubset(self, key):
        """TODO: Returns a GeoVariableArray with the given subset. Take code
        from __getitem__ to analyze the key, create a new private
        method that retrieves both indexes and data. __getitem__ will
        return only data and this will return a new GeoVariableArray
        with indexes.

        """
        pass

    def sort(self, axis, order=None):
        """Sorts the dataset based on an axis.
        TODO: sort based on a lambda."""
        if self._data is None:
            return

        axis = self._getAxis(axis)
        unsorted = True
        while unsorted:
            unsorted = False
            i = 0
            while i<len(axis)-1:
                if axis[i]>axis[i+1]:
                    x = axis[i]
                    y = axis[i+1]
                    a = np.array(self._data[self._generateSingleKey(self._axis.index(axis),i)])
                    b = np.array(self._data[self._generateSingleKey(self._axis.index(axis),i+1)])
                    axis[i] = y
                    axis[i+1] = x
                    self._data[self._generateSingleKey(self._axis.index(axis),i)] = b
                    self._data[self._generateSingleKey(self._axis.index(axis),i+1)] = a
                    unsorted = True
                else:
                    i+=1

    def _generateSingleKey(self, axis, key):
        """Returns a tuple containing an indexing key for a single dimension, e.g.:

        (2,slice(None,None),slice(None,None))

        ":" as key means slice(None,None)
        """
        axis = self._axis.index(self._getAxis(axis))
        key = slice(None,None) if key==":" else key
        out = []
        for i in range(self.ndim):
            out.append(slice(None,None),)
        out[axis] = self._analyzeKey(axis, key)
        return tuple(out)

    def merge(self, indarray):
        """Merges information present in the given Indarray into this one.
        Both Indarrays must have the same dimension and data type.

        """
        if self.ndim!=indarray.ndim:
            raise FluxException("Indarrays dimensions must match for a merge.")
        if self.dtype!=indarray.dtype:
            raise FluxException("Indarrays dtype must match for a merge.")

        keyDiffs = ()
        for i in range(self.ndim):
            keyDiff = arrayops.arraySubstraction(indarray.keys(i), self.keys(i))
            self.addKey(i, keyDiff)
            keyDiffs+=(tuple(keyDiff),)


            

        import ipdb
        ipdb.set_trace()

        """TODO: Retrieve data from the indarray"""

        print 

        # print self._generateSingleKey(0, ("A1n",))

        # for i in range(len(keyDiffs)):
        #     dataA = indarray.select(
        
        

        # diffGeoentityAB = arrayops.arraySubstraction(self.geoentity, geoVariableArray.geoentity)
        # diffGeoentityBA = arrayops.arraySubstraction(geoVariableArray.geoentity, self.geoentity)

        

        # if diffGeoentityBA is not None:
        #     self.addGeoentity(diffGeoentityBA)
        # if diffGeoentityAB is not None:
        #     geoVariableArray.addGeoentity(diffGeoentityAB)

        # diffTimeAB = arrayops.arraySubstraction(self.time, geoVariableArray.time)
        # diffTimeBA = arrayops.arraySubstraction(geoVariableArray.time, self.time)

        # # print "diffTimeAB : ", diffTimeAB
        # # print
        # # print "diffTimeBA : ", diffTimeBA
        # # print

        # if diffTimeBA is not None:
        #     self.addTime(diffTimeBA)

        # if diffTimeAB is not None:
        #     geoVariableArray.addTime(diffTimeAB)

        # self.sort()
        # geoVariableArray.sort()

        # diffVariable = arrayops.arraySubstraction(geoVariableArray.variable, self.variable)

        # # print "DiffVariable : "
        # # print [geoVariableArray[:,:,x] for x in diffVariable]


        # # print "Shape A F: ", self.shape
        # # print "Shape B F: ", geoVariableArray.shape
        # # print
        # # print

        # # print "kkkk : "
        # # print geoVariableArray[:,:,:]
        # # print [geoVariableArray[:,:,x] for x in diffVariable][0]

        # # import ipdb
        # # ipdb.set_trace()

        # for x in diffVariable: 
        #     # print "XX : ", x, geoVariableArray[:,:,x]
        #     self.addVariable(x, data=geoVariableArray[:,:,str(x)])








        

class FluxException(Exception):
    """Exception for Flux.

    """
    _message = ""

    def __init__(self, message):
        self._message = message
    
    def __str__(self):
        return(self._message)
