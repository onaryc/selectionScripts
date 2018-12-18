#!/usr/bin/env python3
# Author: onaryc
# Modified Date: 
# Purpose: manage game selection

import sys
import os
# import re
from shutil import copy
# from colorama import init
# init()
# from colorama import Fore, Back, Style
# import inspect

#sys.path.append(".")
from MVCFramework.Model.model import *
from MVCFramework.Tools.tools import *

global api

class CController(CObject):
    _instanceAttributes = [
        {'name': 'api', 'defaultValue': ''}
    ]
    def __init__(self, pData = {}):
        CObject.__init__(self, pData)

class CDebugController(CController):
    _instanceAttributes = CController._instanceAttributes + [
        {'name': 'debugLevel', 'defaultValue': 0}
        ]
        
    def __init__(self, pData = {}):
        CController.__init__(self, pData)

    def initialization(self, pData = {}):
        pass
        
    def APIdprint(self, pString, pLevel = 1):
        if pLevel <= self.debugLevel: 
            print('Debug : ' + pString)
        # print(Fore.RED + pString)
        
class CLogController(CController):
    _instanceAttributes = CController._instanceAttributes + [
        {'name': 'logFile', 'defaultValue': ''}
        ]
        
    def __init__(self, pData = {}):
        CController.__init__(self, pData)

    def initialization(self, pData = {}):
        self.resetLog()

    def resetLog(self):
        try:
            with open(self.logFile, "w"):
                pass
        except FileNotFoundError:
            self.api.dprint("no instance attributes", 2)
            
    def APIlog(self, pString, pPrint=False):
        try:
            fd = open(self.logFile,'a')

            fd.write(pString + '\n')
            
            fd.close()

            if pPrint == True:
                print(pString)
        except FileNotFoundError:
            self.api.dprint('file ' + self.logFile + ' does not exist', 2)

    def APIlog2(self, pFile, pString, pPrint=False):
        try:
            fd = open(pFile,'a')

            fd.write(pString + '\n')
            
            fd.close()

            if pPrint == True:
                print(pString)
        except FileNotFoundError:
            self.api.dprint('file ' + pFile + ' does not exist', 2)

class CDataController(CController):
    _instanceAttributes = CController._instanceAttributes + [
        {'name': 'instances', 'defaultValue': []}
        ]
    def __init__(self, pData = {}):
        CController.__init__(self, pData)

    def initialization(self, pData = {}):
        pass

    def APIcreate(self, pClass, pData = {}):
        instance = pClass(pData)

        self.instances.append(instance)

        return instance

    # def APIgatherData(self, pInstance, pString):
        # pInstance.gatherData(pString)
    def APIgatherDataFromDir(self, pSources, pFileTypes, pGameClass ):
        for directory in pSources:
            if os.path.isdir(directory) == True:
                for filename1 in os.listdir(directory):
                    completePath1 = os.path.join(directory, filename1)
                    #print('completePath1 ' + completePath1 + ' ' + str(os.path.isdir(completePath1)))
                    if os.path.isdir(completePath1) == True:
                        for filename2 in os.listdir(completePath1):
                            completePath2 = os.path.join(completePath1, filename2)
                            #print('completePath2 ' + completePath2 + ' ' + str(os.path.isfile(completePath2)))
                            if os.path.isfile(completePath2) == True:
                                name, extension = os.path.splitext(filename2)
                                if extension in pFileTypes:
                                    instance = self.api.create(pGameClass, {'extension' : extension, 'tags' : filename1, 'filename': completePath2})
                                    instance.gatherData(name)
                                else:
                                    self.api.log(filename2 + ' extension does not correspond (' + str(pFileTypes) + ')')

    def APIgatherDataFromFile(self, pSource, pGameClass ):
        fd = open(pSource,'r')
        lines = fd.readlines()
        linesCount = len(lines)
        lines = lines[1:linesCount]

        for line in lines:
            #print('line : ' + line)
            instance = self.api.create(pGameClass)

            if instance != None:
                instance.deserialize(line)
                # print('test ' + instance.name)
                # print('filename ' + instance.filename)
            
        fd.close()
        
    def APIserialize(self, pFile, pClass ):
        ## open it
        try:
            fd = open(pFile,'w')

            ## write the header
            header = pClass.serializeHeader()
            fd.write(header)
            
            ## write instance serialization
            for instance in self.instances:
                serialize = instance.serialize() 
                fd.write(serialize)
                
            ## close the file
            fd.close()
        except FileNotFoundError:
            api.log('file ' + pFile + ' does not exist')

    def APIdeserialize(self, pFile, pClass ):
        pass
        
    def APIoutputData(self, pTarget, pFiles, pExcludedStrings, pMissingFile='missing.txt', pForceCopy=False):
        for instance in self.instances:
            ## create the tag directories
            tags = instance.tags
            completePath = os.path.join(pTarget, tags)
            if os.path.exists(completePath) == False:
                os.makedirs(completePath)
                # print('tags ' + tags)

            ## output info
            tmp = 'Searching for ' + instance.name
            self.api.log('Searching for ' + instance.name + '(' + tags + ')', True)
            
            ## try to find a correspond value in the file list
            ## construct the regular search value
            searchValue = arrangeRE(instance.name)

            ## add optional excluded strings
            excludedStrings = []
            for excludedString in pExcludedStrings:
                excludedStrings.append(arrangeRE(excludedString, False))

            
            foundFiles = findInFiles(searchValue, pFiles, excludedStrings)
            if not foundFiles:
                ## try to widen the search
                searchValue = arrangeRE(instance.name, False)
                foundFiles = findInFiles(searchValue, pFiles, excludedStrings)

            # print('foundFiles ' + str(foundFiles))

            if foundFiles:
                self.api.log('\tfound ' + str(foundFiles), True)
                for filename in foundFiles:
                    # print('found ' + str(foundFiles))
                    path, name = os.path.split(filename)
                    completePath2 = os.path.join(completePath, name)
                    if (os.path.exists(completePath2) == False) or (pForceCopy == True):                                
                        try:
                            print('\tcopy ' + filename + ' to ' + completePath2)
                            copy(filename, completePath)
                        except PermissionError:
                            self.api.log('Error : can not copy ' + filename + ' to ' + completePath)
                    else:
                        self.api.log('\t' + completePath2 + ' already exists')
            else:
                self.api.log('\tNot found')
                self.api.log2(pMissingFile, 'Missing ' + instance.name + '(' + tags + ')')
            # for filename in pFiles:
                # try:
                    # ## get the name
                    # path, name = os.path.split(filename)
                    # tmp = name.split(' (')
                    # res = re.match(searchValue, tmp[0], flags=re.I)
                    # # if filename.startswith("Dune") == True:
                        # # print('test ' + filename + ' ' + str(res))
                        # # print('searchValue ' + searchValue)
                    # # print('test ' + searchValue + ' on ' + filename)
                    # if res:
                        # testExcluded = True
                        # for excludedString in excludedStrings:
                            # res2 = re.match(excludedString, filename, flags=re.I)
                            # if res2:
                                # # self.api.log('Exclude ' + searchValue2 + ' on ' + filename)
                                # testExcluded = False

                        # if testExcluded == True:
                            # findAMatch = True
                            # completePath2 = os.path.join(completePath, name)
                            # if (os.path.exists(completePath2) == False) or (pForceCopy == True):                                
                                # try:
                                    # copy(filename, completePath)
                                # except PermissionError:
                                    # self.api.log('Error : can not copy ' + filename + ' to ' + completePath)
                            
                # except re.error:
                    # self.api.log('Error : match between ' + searchValue + ' and ' + filename)
                    
            # if findAMatch == False:
                # self.api.log('No match for ' + instance.name + ' ('+ searchValue + ') (' + tags + ')')
         
            
        
class CAPIController(CController):
    _instanceAttributes = CController._instanceAttributes + [
        {'name': 'controllers', 'defaultValue': []}
        ]
        
    def __init__(self, pData = {}):
        CController.__init__(self, pData)

    def initialization(self, pData = {}):
        ## create the controllers
        pData['api'] = self
        self.controllers.append(CDebugController(pData))
        self.controllers.append(CLogController(pData))
        self.controllers.append(CDataController(pData))

        ## dynamically add the APIs from the controllers
        for ctrl in self.controllers:            
            ## get the apis of the controller
            apis = ctrl.getMethods('API')
            for api in apis:
                ## remove the API prefix to define the new function within the APIController class
                newName = api[0][3:]
                self.set(newName, api[1])

        ## initialize the controllers
        for ctrl in self.controllers:
            ctrl.initialization()
            

    
