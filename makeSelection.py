#!/usr/bin/env python3
# Author: onaryc
# Modified Date: 
# Purpose: manage game selection

import sys
import os
import argparse
import inspect

# import custom module
sys.path.append(os.getcwd())
from MVCFramework.Model.model import *
from MVCFramework.Controller.controller import *
from MVCFramework.Tools.tools import *
        
def makeSelectionFile( pSelectionFile, pSources, pHardware, pFileTypes ):
    ## select the class
    gameClass = None
    if pHardware == 'amiga':
        gameClass = CAmigaGame

    if gameClass == None:
        return
        
    ## gather the data
    api.gatherDataFromDir(pSources, pFileTypes, gameClass)

    ## serialize data
    api.serialize(pSelectionFile, gameClass)
                
def main():
    ## parse argument
    parser = argparse.ArgumentParser(description='Manage games selection')
    ##parser.add_argument('-q', '--quick', action='store_true', help='')

    #parser.add_argument('sources', help='')
    #parser.add_argument('hardware', help='game hardware plateform')
    #parser.add_argument('fileType', help='')
    #parser.add_argument('filename', help='')

    # Check passed arguments
    args = parser.parse_args()

    ## launch the controllers
    logFile = "log.txt"
    debugLevel = 2
    global api
    api = CAPIController()
    api.initialization({'logFile' : logFile, 'debugLevel' : debugLevel})
    
    #sources = args.sources
    #hardware = args.hardware
    #fileType = args.fileType
    #filename = args.filename
    sources = ['G:\\Amiga\\ECS-OCS']
    hardware = 'amiga'
    fileType =['.ipf']
    filename = 'selection.txt'

    # make selection file
    makeSelectionFile(filename, sources, hardware, fileType)

if __name__ == "__main__":
    main()
