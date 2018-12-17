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
    print('* gather data from ' + pSelectionFile)
    api.gatherDataFromFile(pSelectionFile, gameClass)

    ## get all the files from the source directory
    print('* list all ' + pFileType + ' files from ' + pSource)
    files = getFiles(pSource, pFileType)
    
    ## construct the output directories and try to fill the directories with files
    print('* construct the directories in ' + pTarget + ' and fill them with files') 
    api.outputData(pTarget, files, ['(De)', '(It)', '(Sp)'])
    

def main():
    ## parse argument
    parser = argparse.ArgumentParser(description='Manage games selection')
    ##parser.add_argument('-q', '--quick', action='store_true', help='Splits file in-place without creating a copy. Only requires 4GiB free space to run')

    # parser.add_argument('target',  help='')
    # parser.add_argument('sources', help='')
    # parser.add_argument('hardware', help='game hardware plateform')
    # parser.add_argument('fileType', help='')
    # parser.add_argument('selectionFile', help='')

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
    source = 'G:\\Amiga\\adf'
    target = 'G:\\Amiga\\test'
    hardware = 'amiga'
    fileType = '.adf'

    dumpSelection(selectionFile, source, target, hardware, fileType)

if __name__ == "__main__":
    main()
    
