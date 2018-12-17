#!/usr/bin/env python3
# Author: onaryc
# Modified Date: 
# Purpose: manage game selection

import inspect

class CObject(object):
    def __init__( self, pData = {} ):
        try:
            for k, v in enumerate(self._instanceAttributes):
                name = v['name']
                try:
                    value = pData[name]
                except KeyError:
                    value = v['defaultValue']

                ## add dynamically the attribute the instance
                self.set(name, value)
        except AttributeError:
            api.dprint("no instance attributes", 2)

    def set(self, pName, pValue ):
        self.__dict__[pName] = pValue
        
    def get(self, pName ):
        return self.__dict__[pName] 

    # @classmethod
    # def setClass(cls, pName, pValue ):
        # super(cls).__setattr__(pName, pValue)
        # # cls.__setattr__(pName, pValue)

    # @classmethod
    # def getClass(cls, pName ):
        # return cls.__dict__[pName]
        
    def getAttributes( self ):
        res = []
        attributes = inspect.getmembers(self,lambda a:not(inspect.ismethod(a)))

        for attribute in attributes:
            #print('test ' + str(attribute) + ' ' + str(inspect.ismethod(attribute)) + ' ' + str(inspect.isfunction(attribute)))
            
            if not((attribute[0].startswith('__') and attribute[0].endswith('__')) or attribute[0].startswith('_') or (inspect.ismethod(attribute))) :
                res.append(attribute)

        return res

    def getMethods (self, pPattern = ''):
        res = []
        methods = inspect.getmembers(self,lambda a:(inspect.ismethod(a)))

        for method in methods:
            ## remove the internal methods
            if not((method[0].startswith('__') and method[0].endswith('__'))):
                if pPattern != '':
                    if method[0].startswith(pPattern) :
                        res.append(method)
                else:
                    res.append(method)

        return res
        
class CGame(CObject):
    _instanceAttributes = [
        {'name': 'name', 'defaultValue': '', 'index' : 0},
        {'name': 'region', 'defaultValue': '', 'index' : 1},
        {'name': 'tags', 'defaultValue': '', 'index' : 2},
        {'name': 'filename', 'defaultValue': '', 'index' : 3},
        {'name': 'extension', 'defaultValue': '', 'index' : 4},
        {'name': 'favorite', 'defaultValue': 'false', 'index' : 5},
        {'name': 'languages', 'defaultValue': '', 'index' : 6},
        ]
    def __init__(self, pData = {}):
        CObject.__init__(self, pData)
    
    def serialize( self ):
        line = []
        res = ""
        try:
            for k, v in enumerate(self._instanceAttributes):
                #print(str(k) + ' = ' + str(v))
                index = v['index']
                line.insert(index, eval('self.' + v['name']))

            res = '\t'.join(line) + '\n'
            # stringToSerialize = '\t'.join(line)
            # pFile.write(stringToSerialize + '\n')
        except AttributeError:
            pass

        return res

    def deserialize (self, pString ):
        ## remove the \n
        stringToAnalyze = pString[0:-1]
        
        tmp = stringToAnalyze.split('\t')
        try:
            for k, v in enumerate(self._instanceAttributes):
                index = v['index']
                name = v['name']

                ## adapt special character
                value = tmp[index]
                value = value.replace('\'', ' ')
                value = value.replace('\\', '\\\\')

                self.set(name, value)
                
                # execStr = 'self.' + name + ' = ' + '\'' + value + '\''
                #print('execStr ' + execStr)
                # exec(execStr)
        except AttributeError:
            pass

    @classmethod
    def serializeHeader ( cls ):
        header = []
        res = ""
        
        ## sort the header according to the index value
        try:
            for k, v in enumerate(cls._instanceAttributes):
                index = v['index']
                header.insert(index, v['name'])

            res = '\t'.join(header) + '\n'
            #print('header ' + str(header))
            # for k, v in enumerate(header):
                # print('v ' + v)
                # pFile.write(v + '\t')


        except AttributeError:
            pass

        return res
                
class CAmigaGame(CGame):
    _instanceAttributes = CGame._instanceAttributes + [
        {'name': 'disk', 'defaultValue': '', 'index' : 6},
        ]
    
    def __init__(self, pData = {}):
        CGame.__init__(self, pData)

    def gatherData(self, pString):
        if self.extension == ".ipf":
            tmp = pString.split(' (')
            #print('tmp ' + str(tmp))
            for k, v in enumerate(tmp):
                if k == 0:
                    self.name = v
                elif k == 1:
                    self.region = v[0:-1]
                else:
                    if v.startswith("Disk") == True:
                        tmp2 = v.split(' ')
                        self.disk = tmp2[1][0:-1]
                    # if v.startswith("Fr") == True:
                        # self.languages = 'Fr'
                    # if v.startswith("De") == True:
                        # self.languages = 'De'
                    # if v.startswith("It") == True:
                        # self.languages = 'It'
                    # if v.startswith("Sp") == True:
                        # self.languages = 'Sp'
