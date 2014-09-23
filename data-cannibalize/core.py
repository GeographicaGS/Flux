# coding=UTF8

# --------------------------------
# Equidna Data Engine Core Classes
# --------------------------------

import numpy as np, hashlib, arrayops
from datetime import datetime, timedelta
import calendar

VAR_TYPE_CONTINUOUS = 0
VAR_TYPE_DISCRETE = 1

COPY_ALL = 0
COPY_GEOENTITIES = 1
COPY_TIMES = 2

# TODO: There are problems with geoentity keys that have special characters in it when indexing. Fix.

class Geoentity(object):
    """TODO: Geoentity class. TODO: enable Maplex multi-name indexing and
    ordering.

    """
    pass



class Variable(object):
    """TODO: Variable class. Make stronger.

    TODO: accept names and descriptions and units as strings. Expand
    to the number of languages involved.

    - **filiation:** a dot separated filiation trace (IEPG.Economic.Energy);
    - **varType:** either VAR_TYPE_CONTINUOUS or VAR_TYPE_DISCRETE. It defaults to VAR_TYPE_CONTINUOUS;
    - **dataType:** a Numpy data type. Defaults to numpy.float64;
    - **languages:** list of language codes for names, descriptions and units. Must be declared for names, descriptions, and units to be added (["ES", "EN"]);
    - **names:** list of names in languages (["Energía", "Energy"]);
    - **descriptions:** list of descriptions (["Desc ES", "Desc EN"]);
    - **units:** list of units in languages (["Kw/h", "Kw/h"]);
    - **traits:** a dictionary with custom traits.

    """
    _filiation = None
    _languages = None
    _names = None
    _descriptions = None
    _units = None
    _varType = None
    _dataType = None
    _traits = None

    def __init__(self, filiation, varType=VAR_TYPE_CONTINUOUS, dataType=np.float_, 
                 languages=None, names=None, descriptions=None, 
                 units=None, traits=None):
        """Constructor. See general class description."""
        if filiation is None or filiation=="":
            raise EquidnaDataException("Bad filiation.")
        self._filiation = filiation.split(".")
        self._languages = languages

        if languages:
            for i in range(0, len(self._languages)):
                if names:
                    self._names = dict()
                    self._names[self._languages[i]] = names[i]
                if descriptions:
                    self._descriptions = dict()
                    self._descriptions[self._languages[i]] = descriptions[i]
                if units:
                    self._units = dict()
                    self._units[self._languages[i]] = units[i]

        self._varType = varType
        self._dataType = dataType
        self._traits = traits

    @property
    def filiation(self):
        """Variable filiation."""
        return(self._filiation)

    @property
    def languages(self):
        """Variable languages."""
        return(self._languages)

    @property
    def names(self):
        """Names."""
        return(self._names)

    @property
    def descriptions(self):
        """Descriptions."""
        return(self._descriptions)

    @property
    def units(self):
        """Variable units."""
        return(self._units)
    
    @property
    def varType(self):
        """Variable type: continuous / discrete."""
        return(self._varType)

    @property
    def dataType(self):
        """Data type (integer, etc.)."""
        return(self._dataType)
    
    @property
    def traits(self):
        """Variable traits."""
        return(self._traits)

    def __hash__(self):
        """Returns the hash."""
        return(int(hashlib.sha256(str(self._filiation)).hexdigest(), base=16))

    def __str__(self):
        """To string."""
        return(str(self._filiation))



class Time(object):
    """Time interval for Equidna.

    TODO: create a function called 'strRepresentation' with rich configuration of the time interval string representation.
    TODO: create a function to return the mid-point of the interval."""
    start = None
    end = None

    def __init__(self, *timeInit):
        """Initializator. TODO: initialize months with str syntax '2013-01'."""
        if len(timeInit)==1:
            if "|" in timeInit[0]:
                self.start = self._getDatetime(timeInit[0].split("|")[0])
                self.end = self._getDatetime(timeInit[0].split("|")[1], lowerLimit=False, initialTime=self.start)
            else:
                self.start = self._getDatetime(timeInit[0])
                self.end = self._getDatetime(timeInit[0], lowerLimit=False, initialTime=self.start)
        if len(timeInit)==2:
            self.start = self._getDatetime(timeInit[0])
            self.end = self._getDatetime(timeInit[1], lowerLimit=False, initialTime=self.start)

        if self.start and self.end and self.start>self.end:
            self.start = None
            self.end = None

    def __div__(self, time):
        """Operator overload. Returns True if time is into the interval,
        extremes included. It gets either a datetime object or a
        string in ISO.

        """
        if not isinstance(time, Time):
            time = Time(time)

        if self.start and self.end and self.start<=time.start and time.end<=self.end:
            return(True)
        if self.start and self.end is None and self.start<=time.start:
            return(True)
        if self.start is None and self.end and time.end<=self.end:
            return(True)

        return(False)

    def __lt__(self, other):
        """Less than. Compares lower limit."""
        return self.start<other.start

    def __str__(self):
        """To str."""
        return("Time: "+str(self.start)+" | "+str(self.end))

    def _getDatetime(self, strptime, lowerLimit=True, initialTime=None):
        """Get the strptime."""
        if strptime=="" or strptime is None: return(None)


        # TODO: arreglar esto para que funcione con decrecimientos de año, contemplar las dos fechas a la vez, no hacer una análisis por separado.
        if any([x in strptime for x in ("Y","M","W","D","H","m","S")]) and initialTime:
            for x in ("Y","M","W","D","H","m","S"):
                parse = strptime.split(x)
                if len(parse)>1:
                    c = int(parse[0])
                    strptime = parse[1]
                    if x=="Y":
                        initialTime += datetime(initialTime.year+c, initialTime.month, initialTime.day, \
                                                initialTime.hour, initialTime.minute, initialTime.second) - \
                            initialTime
                    if x=="M":
                        if initialTime.month==12:
                            initialTime += datetime(initialTime.year+c, 1, initialTime.day, \
                                                    initialTime.hour, initialTime.minute, initialTime.second) - \
                                initialTime
                        else:
                            initialTime += datetime(initialTime.year, initialTime.month+c, initialTime.day, \
                                                    initialTime.hour, initialTime.minute, initialTime.second) - \
                                initialTime
                    if x=="W":
                        initialTime += timedelta(weeks=c)
                    if x=="D":
                        initialTime += timedelta(days=c)
                    if x=="H":
                        initialTime += timedelta(hours=c)
                    if x=="m":
                        initialTime += timedelta(minutes=c)
                    if x=="S":
                        initialTime += timedelta(seconds=c)

            return initialTime



        strp = "%Y-%m-%d %H:%M:%S"
        dt = strptime.split(" ")

        # Process date
        ymd = dt[0].split("-")
        if len(ymd)==2:
            if lowerLimit:
                ymd.append("01")
            else:
                days = calendar.monthrange(int(ymd[0]), int(ymd[1]))[1]
                ymd.append(str(days))
        if len(ymd)==1:
            if lowerLimit:
                ymd.extend(["01","01"])
            else:
                ymd.extend(["12","31"])

        # Process time
        if len(dt)==2:
            hms = dt[1].split(":")
            if len(hms)==2:
                if lowerLimit:
                    hms.append("00")
                else:
                    hms.append("59")
            if len(hms)==1:
                if lowerLimit:
                    hms.extend(["00","00"])
                else:
                    hms.extend(["59","59"])
        else:
            if lowerLimit:
                hms = ["00","00","00"]
            else:
                hms = ["23","59","59"]

        strptime = str(int(float(ymd[0])))+"-"+ymd[1]+"-"+ymd[2]+" "+hms[0]+":"+hms[1]+":"+hms[2]
        return(datetime.strptime(strptime, strp))

    def __hash__(self):
        """Get the hash."""
        return(int(hashlib.sha256(str(self)).hexdigest(), base=16))



class GeoVariableArray(object):
    """Data array for Equidna. Instantiate it with a list of geoentities
    and times.

    TODO: test if Numpy supports discrete values.
    
    TODO: initialize time with a list of strings.

    TODO: accessing the object like "x" should return the data array

    """
    # def __init__(self, geoentity=None, time=None, variable=None, data=None):
    #     """Initializator. Gets a list of geoentities and times to initialize
    #     the data array. TODO: initialize time with a list of strings.

    #     """
    #     self.__geoentity = [geoentity] if geoentity and not isinstance(geoentity, list) else geoentity
    #     if time:
    #         time = [time] if not isinstance(time, list) else time
    #         self.__time = [Time(x) for x in time if not isinstance(x, Time)] if time else None
    #         self.__time.extend([x for x in time if isinstance(x, Time)])
    #     self.__variable = [variable] if variable and not isinstance(variable, list) else variable
        
    #     self.__addDataToMatrix(data=data)

    # def __addDataToMatrix(self, data=None, dimension=None):
    #     """Adds data if the matrix is fully configured with geoentities,
    #     times, and variables. Set it to nan if there are no data,
    #     otherwise, adds the passed data, if any, to the given
    #     dimension (if any, otherwise sets the whole matrix).

    #     TODO: this function seems to have problems adding data that
    #     contains "None", which should be translated to np.nan??? Check
    #     this. >>> Seems to be True!!! Filter None with np.nan. It is
    #     supposed that data is a ndarray, but we should explore to feed
    #     this with Python lists. Perhaps this should get only ndarray
    #     with np.nan and the functions that uses them should feed this
    #     with already None filtered ndarray.

    #     """
    #     # print "EW : ", data
    #     # print "EW : ", dimension
    #     # print "EW : ", self.__data is not None and dimension is not None

    #     # Creates the array if not there and all is in place
    #     arrayJustCreated = False
    #     if self.__data is None:
    #         if self.__variable and self.__geoentity and self.__time:
    #             self.__data = np.empty((len(self.__geoentity), len(self.__time), len(self.__variable)))
    #             arrayJustCreated = True

    #     if self.__data is not None and data is not None and dimension is None:
    #         # Initializes data to full array
    #         self.__data = np.array(data).reshape((len(self.__geoentity), 
    #                                               len(self.__time), len(self.__variable)))
    #     elif self.__data is not None and dimension is not None:
    #         # Adds data to a dimension, either blank or real data
    #         s = self.shape
    #         if dimension==0 and not arrayJustCreated:
    #             if data is not None:
    #                 dataA = data
    #             else:
    #                 dataA = np.empty((1,s[1],s[2]))
    #                 dataA[:] = np.nan
    #             self.__data = np.append(self.__data, np.array(dataA).reshape(1,s[1],s[2]), axis=dimension)
    #         elif dimension==0:
    #             if data is not None:
    #                 self.__data = np.array(data).reshape(s[0],s[1],s[2])
    #             else:
    #                 self.__data[:] = np.nan
    #         if dimension==1 and not arrayJustCreated:
    #             if data is not None:
    #                 dataA = data
    #             else:
    #                 dataA = np.empty((s[0],1,s[2]))
    #                 dataA[:] = np.nan
    #             self.__data = np.append(self.__data, np.array(dataA).reshape(s[0],1,s[2]), axis=dimension)
    #         elif dimension==1:
    #             if data is not None:
    #                 self.__data = np.array(data).reshape(s[0],s[1],s[2])
    #             else:
    #                 self.__data[:] = np.nan
    #         if dimension==2 and not arrayJustCreated:
    #             if data is not None:
    #                 dataA = data
    #             else:
    #                 dataA = np.empty((s[0],s[1],1))
    #                 dataA[:] = np.nan
    #             self.__data = np.append(self.__data, np.array(dataA).reshape(s[0],s[1],1), axis=dimension)
    #         elif dimension==2:
    #             if data is not None or data!=[]:



    #                 # print "LLLLL : "
    #                 # print "Shape : ", s

    #                 # print data.shape
    #                 # print

    #                 self.__data = np.array(data).reshape(s[0],s[1],s[2])
    #             else:
    #                 self.__data[:] = np.nan
    #     elif self.__data is not None:
    #         self.__data[:] = np.nan

    # def __call__(self):
    #     """Returns the data array."""
    #     return self.__data

    # @property
    # def geoentity(self):

    #     """Geoentity instances in the data matrix."""
    #     return(self.__geoentity)

    # @property
    # def time(self):
    #     """Times instances in the data matrix."""
    #     return(self.__time)

    # @property
    # def variable(self):
    #     """Variable instances in the data matrix."""
    #     return(self.__variable)

    # @property
    # def shape(self):
    #     """Returns dimensions of the data matrix. First item is Geoentity number, second Time, 
    #     and third Variable."""
    #     if self.__data is not None:
    #         return self.__data.shape
    #     else:
    #         return None

    # @property
    # def size(self):
    #     """Returns size of data: Geoentity x Time x Variable."""
    #     return self.__data.size

    # @property
    # def data(self):
    #     """Data matrix. It's a Numpy ndarray object."""
    #     return(self.__data)

    # def __getitem__(self, key):
    #     """Gets data directly from the internal ndarray. Supported indices:
        
    #     slices: 1:2
    #     integers: 2
    #     tuples: (2,1)
    #     string indices: "US", "2013", "V0"
    #     string tuples: ("US","ES")
    #     TODO: callables to generate tuples

    #     """
    #     # print "Geo : ", key[0], type(key[0])
    #     # print "Time : ", key[1], type(key[1])
    #     # print "Var : ", key[2], type(key[2])

    #     geo = self.__analyzeKeyGetItemGeo(key[0])
    #     time = self.__analyzeKeyGetItemTime(key[1])
    #     var = self.__analyzeKeyGetItemVar(key[2])

    #     # print
    #     # print "Geo : ", geo, type(geo)
    #     # print "Time : ", time, type(time)
    #     # print "Var : ", var, type(var)
    #     # print

    #     return self.__data[geo,time,var]

    # def select(self, geoentity, time, variable):
    #     """Returns selected data. Indices can be:

    #     integers: 2
    #     strings: "US", "2013", "V0"
    #     lists of mixed above
    #     None: all, like slice :

    #     """
    #     # print "Geo : ", key[, type(key[0])
    #     # print "Time : ", key[1], type(key[1])
    #     # print "Var : ", key[2], type(key[2])

    #     geo = self.__analyzeKeySelectGeo(geoentity)
    #     time = self.__analyzeKeySelectTime(time)
    #     var = self.__analyzeKeySelectVar(variable)

    #     # print
    #     # print "Geo : ", geo, type(geo)
    #     # print "Time : ", time, type(time)
    #     # print "Var : ", var, type(var)
    #     # print

    #     out = self.__data
    #     out = out[:,:,var]

    #     if out.ndim==3:
    #         out = out[:,time,:]
    #     else:
    #         out = out[:,time]

    #     if out.ndim==3:
    #         out = out[geo,:,:]
    #     elif out.ndim==2:
    #         out = out[geo,:]
    #     else:
    #         out = out[geo]
            
    #     return out        

    # def __setitem__(self, key, value):
    #     """Set item.

    #     Value can be a np.ndarray that matches the key. For example,
    #     in a GeoVariableArray with 4 geoentities and 7 times:

    #     gva[:,"2010","Var 1"]=np.array([0,1,2,3])

    #     should set the values for 2010 for the 4 geoentities to the
    #     given values.

    #     TODO: Try slices with steps

    #     """
    #     # print "Geo : ", key[0], type(key[0])
    #     # print "Time : ", key[1], type(key[1])
    #     # print "Var : ", key[2], type(key[2])
    #     # print

    #     geo = self.__analyzeKeyGetItemGeo(key[0])
    #     time = self.__analyzeKeyGetItemTime(key[1])
    #     var = self.__analyzeKeyGetItemVar(key[2])


    #     # print
    #     # print "Geo : ", geo, type(geo)
    #     # print "Time : ", time, type(time)
    #     # print "Var : ", var, type(var)
    #     # print

    #     self.__data[geo,time,var] = value

        # ---------------------------------------------------------------------------------
        # DO NOT DELETE THIS BLOCK! May be of use to implement a set method based on select
        # ---------------------------------------------------------------------------------

        # if any([isinstance(x, list) for x in key]):
        #     print "LISTS!!"
        
        #     if isinstance(geo, slice):
        #         start = geo.start if geo.start is not None else 0
        #         stop = geo.stop if geo.stop is not None else len(self.__geoentity)
        #         step = geo.step if geo.step is not None else 1
        #         geo = tuple(range(start, stop, step))

        #     if isinstance(time, slice):
        #         start = time.start if time.start is not None else 0
        #         stop = time.stop if time.stop is not None else len(self.__time)
        #         step = time.step if time.step is not None else 1
        #         time = tuple(range(start, stop, step))

        #     if isinstance(var, slice):
        #         start = var.start if var.start is not None else 0
        #         stop = var.stop if var.stop is not None else len(self.__variable)
        #         step = var.step if var.step is not None else 1
        #         var = tuple(range(start, stop, step))

        #     print "Value"
        #     print value

        #     for g in range(len(geo)):
        #         for t in range(len(time)):
        #             for v in range(len(var)):
        #                 print g,t,v
        #                 print self.__data[geo[g],time[t],var[v]] 
        #                 print value[g,t,v]
        #                 self.__data[geo[g],time[t],var[v]] = value[g,t,v]
                        

        # else:
        #     if all([isinstance(x, tuple) for x in key]):
        #         self.__data[geo,time,var] = value
        #         return None

        #     if any([isinstance(x, tuple) for x in key]):
        #         raise FluxException("GeoVariableArray __getitem__: cannot mix tuples with other keys.")
        


            


        # print "Geo : ", key[0], type(key[0])
        # print "Time : ", key[1], type(key[1])
        # print "Var : ", key[2], type(key[2])

        # geo = self.__analyzeKeyGeo(key[0])
        # time = self.__analyzeKeyTime(key[1])
        # var = self.__analyzeKeyVar(key[2])

        # if all([isinstance(x, tuple) for x in key]):
        #     return self.__data[geo,time,var]

        # if any([isinstance(x, tuple) for x in key]):
        #     raise FluxException("GeoVariableArray __getitem__ error: cannot mix tuples with other keys.")

        # out = self.__data

        # print
        # print "Geo : ", geo, type(geo)
        # print "Time : ", time, type(time)
        # print "Var : ", var, type(var)
        # print

        # out = out[:,:,var]

        # if out.ndim==3:
        #     out = out[:,time,:]
        # else:
        #     out = out[:,time]

        # if out.ndim==3:
        #     out = out[geo,:,:]
        # elif out.ndim==2:
        #     out = out[geo,:]
        # else:
        #     out = out[geo]
    
        # out = value


        # geo = self.__analyzeKeyGeo(key[0])
        # time = self.__analyzeKeyTime(key[1])
        # var = self.__analyzeKeyVar(key[2])
        # out = self.__data

        # # self[key] = value
        # pass
        # print "geo : ", geo
        # print "time : ", time
        # print "var : ", var

        # out = out[:,:,var]

        # if out.ndim==3:
        #     out = out[:,time,:]
        # else:
        #     out = out[:,time]

        # if out.ndim==3:
        #     out = out[geo,:,:]
        # elif out.ndim==2:
        #     out = out[geo,:]
        # else:
        #     out = out[geo]

        # out = value

        # print "JJ"
        # print out
        # print

    # def __analyzeKeyGetItemGeo(self, key):
    #     """Analyses a geoentity key for get/set.

    #     TODO: implement callable (to create tuples)
    #     TODO: work with Time object.
    #     TODO: drop old methods.
    #     """
    #     if isinstance(key, (slice)):
    #         return key

    #     key = (key,) if not isinstance(key, tuple) else key
    #     out = ()

    #     for i in key:
    #         if isinstance(i, int):
    #             out += (i,)
    #         if isinstance(i, str):
    #             out += (self.__geoentity.index(i),)

    #     return out

    # def __analyzeKeyGetItemTime(self, key):
    #     """Analyses a time key for get/set.

    #     TODO: implement callable (even list of callables)
    #     TODO: work with Time object.
    #     """
    #     if isinstance(key, (slice)):
    #         return key

    #     key = (key,) if not isinstance(key, tuple) else key
    #     out = ()

    #     for i in key:
    #         if isinstance(i, int):
    #             out += (i,)
    #         if isinstance(i, str):
    #             # TODO: PROBLEMS AHEAD!!! This can yield more elements in the resulting tuple than expected
    #             for k in range(0, len(self.__time)):
    #                 if self.__time[k]/i:
    #                     out += (k,)

    #     return out

    # def __analyzeKeyGetItemVar(self, key):
    #     """Analyses a variable key for get/set.

    #     TODO: implement callable (even list of callables)
    #     TODO: work with variable object.
    #     """
    #     if isinstance(key, (slice)):
    #         return key

    #     key = (key,) if not isinstance(key, tuple) else key
    #     out = ()

    #     for i in key:
    #         if isinstance(i, int):
    #             out += (i,)
    #         if isinstance(i, str):
    #             out += (self.__variable.index(i),)

    #     return out







    # def __analyzeKeySelectGeo(self, key):
    #     """Analyses a geoentity key for get/set.

    #     TODO: implement callable (to create tuples)
    #     TODO: work with Time object.
    #     TODO: drop old methods.
    #     """
    #     if key is None:
    #         return slice(None, None)

    #     key = [key] if not isinstance(key, list) else key
    #     out = ()

    #     for i in key:
    #         if isinstance(i, int):
    #             out += (i,)
    #         if isinstance(i, str):
    #             out += (self.__geoentity.index(i),)

    #     return out

    # def __analyzeKeySelectTime(self, key):
    #     """Analyses a time key for get/set.

    #     TODO: implement callable (even list of callables)
    #     TODO: work with Time object.
    #     """
    #     if key is None:
    #         return slice(None, None)

    #     key = [key] if not isinstance(key, list) else key
    #     out = ()

    #     for i in key:
    #         if isinstance(i, int):
    #             out += (i,)
    #         if isinstance(i, str):
    #             # TODO: PROBLEMS AHEAD!!! This can yield more elements in the resulting tuple than expected
    #             for k in range(0, len(self.__time)):
    #                 if self.__time[k]/i:
    #                     out += (k,)

    #     return out

    # def __analyzeKeySelectVar(self, key):
    #     """Analyses a variable key for get/set.

    #     TODO: implement callable (even list of callables)
    #     TODO: work with variable object.
    #     """
    #     if key is None:
    #         return slice(None, None)

    #     key = [key] if not isinstance(key, list) else key
    #     out = ()

    #     for i in key:
    #         if isinstance(i, int):
    #             out += (i,)
    #         if isinstance(i, str):
    #             out += (self.__variable.index(i),)

    #     return out









    # def getSubset(self, key):
    #     """TODO: Returns a GeoVariableArray with the given subset. Take code
    #     from __getitem__ to analyze the key, create a new private
    #     method that retrieves both indexes and data. __getitem__ will
    #     return only data and this will return a new GeoVariableArray
    #     with indexes.

    #     """
    #     pass

    # def sort(self):
    #     if self.__data is None:
    #         return

    #     unsorted = True
    #     while unsorted:
    #         unsorted = False
    #         i = 0
    #         while i<len(self.geoentity)-1:
    #             if self.geoentity[i]>self.geoentity[i+1]:
    #                 x = self.geoentity[i]
    #                 y = self.geoentity[i+1]
    #                 a = np.array(self.__data[i,:,:])
    #                 b = np.array(self.__data[i+1,:,:])
    #                 self.geoentity[i] = y
    #                 self.geoentity[i+1] = x
    #                 self.__data[i,:,:] = b
    #                 self.__data[i+1,:,:] = a
    #                 unsorted = True
    #             else:
    #                 i+=1

    #     unsorted = True
    #     while unsorted:
    #         unsorted = False
    #         i = 0
    #         while i<len(self.time)-1:
    #             if self.time[i]>self.time[i+1]:
    #                 x = self.time[i]
    #                 y = self.time[i+1]
    #                 a = np.array(self.__data[:,i,:])
    #                 b = np.array(self.__data[:,i+1,:])
    #                 self.time[i] = y
    #                 self.time[i+1] = x
    #                 self.__data[:,i,:] = b
    #                 self.__data[:,i+1,:] = a
    #                 unsorted = True
    #             else:
    #                 i+=1

    # def __analyzeKeyTime(self, key):
    #     """Analyses a time key. TODO: this has a problem when asking for a
    #     non-existent year, like in data["US","2323","V0"]. FIX!

    #     """
    #     print "UUU : ",key, type(key)

    #     if callable(key):
    #         out = ()
    #         for i in range(0, len(self.__time)):
    #             # print "ll : ", key(self.__time[i])
    #             if key(self.__time[i]):
    #                 out+=(i,)
    #         return out
    #     if isinstance(key, (str, Time)):
    #         out = ()
    #         for i in range(0, len(self.__time)):
    #             if self.__time[i]/key:
    #                 out+=(i,)
    #         return out
    #     if isinstance(key, tuple):
    #         out = ()
    #         for i in key:
    #             out+=((self.__analyzeKeyTime(i),),)

    #         print "KLLLL : ", out
    #         return tuple(x for y in out for x in y)
    #     if isinstance(key, (int, slice)):
    #         return key
        
    # def __analyzeKeyGeoentity(self, key):
    #     """Analyses key for a given dimension."""
    #     if isinstance(key, str):
    #         return(self.geoentity.index(key))
    #     if isinstance(key, tuple):
    #         out = ()
    #         for i in key:
    #             out+=((self.__analyzeKeyGeoentity(i),),)
    #         return tuple(x for y in out for x in y)
    #     if isinstance(key, (int, slice)):
    #         return key

    # def __analyzeKeyVariable(self, key):
    #     """Analyses key for a given dimension."""

    #     print "Var entry: ",key, type(key)

    #     if isinstance(key, str):
    #         return(self.variable.index(key))
    #     if isinstance(key, tuple):

    #         print "Var tuple: ", key

    #         out = ()
    #         for i in key:
    #             out+=((self.__analyzeKeyVariable(i),),)

    #         print "LLLLLLLLLLHHH: ", out, tuple(x for y in out for x in y)
    #         return tuple(x for y in out for x in y)
    #     if isinstance(key, (int, slice)):
    #         return key

    # def addGeoentity(self, geoentity, data=None):
    #     """Adds new geoentities to the geoentity dimension. Geoentity can be a
    #     string or a list of strings. WARNING! Values added to the
    #     matrix are random! Initialize true values inmediatly!

    #     TODO: provide data matrix.

    #     """
    #     geoentity = [geoentity] if not isinstance(geoentity, list) else geoentity
    #     data = [data] if data and not isinstance(data[0], list) else data

    #     if self.__geoentity is None:
    #         self.__geoentity = []

    #     for i in range(0, len(geoentity)):
    #         if geoentity[i] not in self.__geoentity:
    #             self.__geoentity.append(geoentity[i])
    #             if data is not None:
    #                 self.__addDataToMatrix(data=data[i], dimension=0)
    #             else:
    #                 self.__addDataToMatrix(dimension=0)

    # def addTime(self, time, data=None):
    #     """Adds new times to the time dimension. time can be a Time or a list
    #     of Time. WARNING! Values added to the matrix are random!
    #     Initialize true values inmediatly!

    #     """
    #     time = [time] if not isinstance(time, list) else time
    #     data = [data] if data and not isinstance(data[0], list) else data

    #     if self.__time is None:
    #         self.__time = []

    #     for i in range(0, len(time)):
    #         if time[i] not in self.__time:
    #             self.__time.append(Time(time[i]) if not isinstance(time[i], Time) else time[i])
    #             if data is not None:
    #                 self.__addDataToMatrix(data=data[i], dimension=1)
    #             else:
    #                 self.__addDataToMatrix(dimension=1)

    # def addVariable(self, variable, data=None):
    #     """Adds a new variable to the variables dimension. Variables can be a
    #     string or a list of strings. data is a unidimensional numpy
    #     ndarray or a bidimensional one. There must be enough data to
    #     fit the size of the array.

    #     TODO: DATA MUST BE A NUMPY NDARRAY! Change in all add data functions.

    #     TODO: Use Variable objects here.
    #     TODO: check other addXXX methods and reharse this. CRAP!
    #     TODO: Review merge function because of rewritten addVariable and company

    #     """
        
    #     # import ipdb
    #     # ipdb.set_trace()

    #     # print "VAR : ", variable, type(variable)
    #     # print
    #     # print "DATA : ", data, type(data)
    #     # print
    #     # print "KKK : ", isinstance(data, np.ndarray)

    #     # print "SHAPE : ", data.shape

    #     variable = [variable] if not isinstance(variable, list) else variable
    #     data = [data] if data is not None and isinstance(data, np.ndarray) else data

    #     if self.__variable is None:
    #         self.__variable = []

    #     for i in range(0, len(variable)):
    #         if variable[i] not in self.__variable:
    #             self.__variable.append(variable[i])
    #             if data is not None:
    #                 self.__addDataToMatrix(data=data[i], dimension=2)
    #             else:
    #                 self.__addDataToMatrix(dimension=2)

    # def copyStructure(self, copy=COPY_ALL):
    #     """Returns a GeoVariableArray with the same geoentities and times."""
    #     geoentity = []
    #     time = []

    #     if copy==COPY_ALL or copy==COPY_GEOENTITIES:
    #         geoentity = self.geoentity
    #     if copy==COPY_ALL or copy==COPY_TIMES:
    #         time = self.time

    #     return GeoVariableArray(geoentity, time)

    # def merge(self, geoVariableArray):
    #     """Merges two GeoVariableArrays. If a variable is present in the
    #     second GeoVariableArray that is present in the first one it's
    #     omitted.

    #     """
    #     diffGeoentityAB = arrayops.arraySubstraction(self.geoentity, geoVariableArray.geoentity)
    #     diffGeoentityBA = arrayops.arraySubstraction(geoVariableArray.geoentity, self.geoentity)

    #     # print "Shape A : ", self.shape
    #     # print "Shape B : ", geoVariableArray.shape
    #     # print "Economic : ", geoVariableArray[:,:,"IEPG.Economic.Energy"]

    #     # print "AB : ", diffGeoentityAB
    #     # print
    #     # print "BA : ", diffGeoentityBA
    #     # print

    #     if diffGeoentityBA is not None:
    #         self.addGeoentity(diffGeoentityBA)
    #     if diffGeoentityAB is not None:
    #         geoVariableArray.addGeoentity(diffGeoentityAB)

    #     diffTimeAB = arrayops.arraySubstraction(self.time, geoVariableArray.time)
    #     diffTimeBA = arrayops.arraySubstraction(geoVariableArray.time, self.time)

    #     # print "diffTimeAB : ", diffTimeAB
    #     # print
    #     # print "diffTimeBA : ", diffTimeBA
    #     # print

    #     if diffTimeBA is not None:
    #         self.addTime(diffTimeBA)

    #     if diffTimeAB is not None:
    #         geoVariableArray.addTime(diffTimeAB)

    #     self.sort()
    #     geoVariableArray.sort()

    #     diffVariable = arrayops.arraySubstraction(geoVariableArray.variable, self.variable)

    #     # print "DiffVariable : "
    #     # print [geoVariableArray[:,:,x] for x in diffVariable]


    #     # print "Shape A F: ", self.shape
    #     # print "Shape B F: ", geoVariableArray.shape
    #     # print
    #     # print

    #     # print "kkkk : "
    #     # print geoVariableArray[:,:,:]
    #     # print [geoVariableArray[:,:,x] for x in diffVariable][0]

    #     # import ipdb
    #     # ipdb.set_trace()

    #     for x in diffVariable: 
    #         # print "XX : ", x, geoVariableArray[:,:,x]
    #         self.addVariable(x, data=geoVariableArray[:,:,str(x)])

    def cluster(self, variable, nseeds):
        """Calculates clusters for a variable.

        nseeds: number of initial seeds
        seedTolerance: % of the total variable range to admit as a tolerance for falling into a seed 

        TODO: Check this development: first line returns a single
        variable data set with geoentities in axis 0 and times in axis
        1. Create therefore a generic object that can hold any
        combinations of axis.

        """
        # Get variable data
        data = self[:,:,variable].reshape(len(self.geoentity),len(self.time))
        clusters = np.empty((len(self.time), len(self.geoentity)))
        clus = []

        min = float(np.nanmin(data))
        max = float(np.nanmax(data))
        seeds = np.repeat(np.linspace(min, max, nseeds)[1:nseeds-1].reshape(1, nseeds-2),
                          len(self.geoentity), axis=0)

        # Iterate to get for each year the clusters
        for i in range(len(self.time)):
            convergingIterations = np.empty((1, len(self.geoentity)))
            timeD = data[:,i]
            timeD2 = np.repeat(timeD.reshape(timeD.size, 1), nseeds-2, axis=1)
            fall = (np.abs(seeds-timeD2)).argmin(axis=1)
            clusters[i,:] = fall
            sSeeds = set(fall)
            for s in set(fall):
                clusterIdx = np.where(fall==s)[0]

        for t in range(len(self.time)):
            clusT = []
            clus.append(clusT)
            for g in range(len(self.geoentity)):
                clusT.append(list(np.where(clusters[t,:]==clusters[t,g])[0].flatten()))

        finalClustersMembers = []
        finalClustersValues = []
        for t in range(len(clus)):
            # For each cluster, filter single clusters
            fClus = []
            [fClus.append(x) for x in clus[t] if x not in fClus]
            finalClustersMembers.append(fClus)
            fClusValues = []

            for x in fClus:
                # For each single cluster, take max and min and calculate average
                fClusValues.append(np.nanmean(self.select(x,t,variable)))

            finalClustersValues.append(fClusValues)

        return finalClustersMembers, finalClustersValues
            

