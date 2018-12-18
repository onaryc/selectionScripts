#!/usr/bin/env python3
# Author: onaryc
# Modified Date: 
# Purpose: manage game selection

import os
import re

def getFiles(pDirectory, pExtensions ):
    files = []
    
    if os.path.isdir(pDirectory) == True:
        for filename in os.listdir(pDirectory):
            
            completePath = os.path.join(pDirectory, filename)
            
            if os.path.isdir(completePath) == True:
                #print('completePath ' + completePath)
                files += getFiles(completePath, pExtensions)

            if os.path.isfile(completePath) == True:
                name, extension = os.path.splitext(filename)
                if extension in pExtensions:
                    #print('completePath ' + completePath)
                    files.append(completePath)

    return files

def findInFiles(pSearchRE, pFiles, pExcludedStrings):
    filenames = []
    for filename in pFiles:
        try:
            ## get the name
            path, name = os.path.split(filename)
            tmp = name.split(' (')
            resMatch = re.match(pSearchRE, tmp[0], flags=re.I)
            # if filename.startswith("Dune") == True:
                # print('test ' + filename + ' ' + str(res))
                # print('searchValue ' + searchValue)
            # print('test ' + searchValue + ' on ' + filename)
            if resMatch:
                testExcluded = True
                for excludedString in pExcludedStrings:
                    resMatch2 = re.match(excludedString, filename, flags=re.I)
                    if resMatch2:
                        # self.api.log('Exclude ' + searchValue2 + ' on ' + filename)
                        testExcluded = False

                if testExcluded == True:
                    filenames.append(filename)
                    # findAMatch = True
                    # completePath2 = os.path.join(completePath, name)
                    # if (os.path.exists(completePath2) == False) or (pForceCopy == True):                                
                        # try:
                            # copy(filename, completePath)
                        # except PermissionError:
                            # api.log('Error : can not copy ' + filename + ' to ' + completePath)
                    
        except re.error:
            api.log('Error : match between ' + pSearchRE + ' and ' + filename)

    return filenames

def arrangeRE(pString, pStartEnd=True):
    ## II vers 2
    ## III vers 3
    ## enlever tout ce qu'il y a après une virgule ou un tiret
    ## & vers and
    res = pString

    ## specific char
    res = res.replace('+', '\+')
    res = res.replace('.', '\.')
    # res = res.replace('\'', '\\\'')
    # res = res.replace('-', '')
    # res = res.replace(',', '')
    # res = res.replace('  ', ' ')

    ## specific char 2
    res = res.replace('(', '\(')
    res = res.replace(')', '\)')

    ## finish the regular expression
    res = res.replace(' ', '.*')
    # res = '.*' + res + '.*'
    if pStartEnd == True:
        res = '^' + res + '$'
    
    return res
