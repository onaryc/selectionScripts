#!/usr/bin/env python3
# Author: onaryc
# Modified Date: 
# Purpose: manage game selection

import os

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
                    files += completePath

    return files
