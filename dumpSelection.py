#!/usr/bin/env python3
# Author: onaryc
# Modified Date: 
# Purpose: manage game selection

import sys
import argparse
import inspect
import glob

# import custom module
import os
print("test " + os.getcwd())

sys.path.append(os.getcwd())
from MVCFramework.Model.model import *
from MVCFramework.Controller.controller import *
from MVCFramework.Tools.tools import *

def dumpSelection ( pSelectionFile, pSource, pTarget, pHardware, pFileType ):
    gameClass = None
    if pHardware == 'amiga':
        gameClass = CAmigaGame

    if gameClass == None:
        return

    ## gather the data
    api.gatherDataFromFile(pSelectionFile, gameClass)

    ## get all the files from the source directory
    #files = getFiles(pSource, pFileType)
    
    #api.constructDir(pTarget)

def main():
    ## parse argument
    parser = argparse.ArgumentParser(description='Manage games selection')
    ##parser.add_argument('-q', '--quick', action='store_true', help='Splits file in-place without creating a copy. Only requires 4GiB free space to run')

    parser.add_argument('target', help='')
    parser.add_argument('sources', help='')
    parser.add_argument('hardware', help='game hardware plateform')
    parser.add_argument('fileType', help='')
    parser.add_argument('selectionFile', help='')

    # Check passed arguments
    args = parser.parse_args()

    ## launch the controllers
    logFile = "log.txt"
    debugLevel = 2
    global api
    api = CAPIController()
    api.initialization({'logFile' : logFile, 'debugLevel' : debugLevel})
    
    #selectionFile = args.selectionFile
    #source = args.source
    #target = args.target
    #hardware = args.hardware
    #fileType = args.fileType
    selectionFile = 'selection.txt'
    source = 'J:\\Amiga\\adf'
    target = 'J:\\Amiga\\test'
    hardware = 'amiga'
    fileType = '.adf'

    dumpSelection(selectionFile, source, target, hardware, fileType)

if __name__ == "__main__":
    main()
    
