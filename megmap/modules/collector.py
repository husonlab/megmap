import pandas as pd 
import numpy as np
import os
from megmap.modules.utils.qc import ClassQC
from megmap.modules.utils.utility import OutputDirectoryGenerator,tarDir,gb_to_mb
from megmap.modules.alignment.diamondAlignment import DiamondAlignment
from megmap.modules.HitToCount import FunctionalHitToCount

class megmapProcessorClass:

    def __init__(self,TakeInputFile: str="", TakePathOfDir: str = "", TakeDatabase: str = "", TakeTool: str ="", TakeToolPath: str ="", TakeIdentity: int="", TakeAlignmentCoverage: int="", TakeEvalue: str="", TakePrefix: str="", TakeReadMode: str="",  TakeThreads: int="", TakeRAM: str = "")->None:

        self.TakeInputFile = TakeInputFile
        self.TakePathOfDir = TakePathOfDir
        self.TakeDatabase = TakeDatabase
        self.TakeTool = TakeTool
        self.TakeToolPath = TakeToolPath
        self.TakeIdentity = TakeIdentity
        self.TakeAlignmentCoverage = TakeAlignmentCoverage
        self.TakeEvalue = TakeEvalue
        self.TakePrefix= TakePrefix
        self.TakeReadMode= TakeReadMode
        self.TakeThreads= TakeThreads
        self.TakeRAM= TakeRAM



    def Alignment(self)->str:
        
        if self.TakeTool == 'diamond':
            DiamondAlignmentHandler=DiamondAlignment(self.TakeInputFile,
                                                    self.TakeDatabase,
                                                    self.TakePathOfDir,
                                                    str(self.TakePrefix+".tab"),
                                                    self.TakeToolPath,
                                                    self.TakeIdentity,
                                                    self.TakeAlignmentCoverage,
                                                    self.TakeEvalue,
                                                    self.TakeThreads,
                                                    self.TakeRAM)

            if not self.TakeToolPath: ##check if self.TakeToolPath variable is empty
                AlignmentFileNameAndPath=DiamondAlignmentHandler.normalDIAlcommand()
            else:
                AlignmentFileNameAndPath=DiamondAlignmentHandler.WithPathDIAlcommand()
            return(AlignmentFileNameAndPath)

def megmapEntry(ReceiveInputFile: str ="", ReceiveOutput: str = "megmap",
                ReceiveDatabase: str = "", ReceiveTool: str ="",
                ReceiveToolPath: str="", ReceiveAlignmentIdentity: int=70,
                ReceiveAlignmentCoverage: int=70,ReceiveEvalue: str="",
                ReceivePrefix: str="",ReceiveReadMode: str="", 
                ReceiveThreads: int="",ReceiveRAM: str = "") -> None:

    DirectoryCaller=OutputDirectoryGenerator(os.path.abspath(ReceiveOutput),'megmap')
    PathOfDir=DirectoryCaller.DicGenAndCheck()
    print(PathOfDir)
    LogFilePath=""
    if ReceiveTool=='blast':

        ClassQC(ReceiveInputFile,ReceiveReadMode,LogFilePath).__extensionType__()

    megmapProcessorClassHandler=megmapProcessorClass(os.path.abspath(ReceiveInputFile),
                                                        PathOfDir, 
                                                        os.path.abspath(ReceiveDatabase), 
                                                        ReceiveTool, 
                                                        ReceiveToolPath,
                                                        ReceiveAlignmentIdentity,
                                                        ReceiveAlignmentCoverage,
                                                        ReceiveEvalue,
                                                        ReceivePrefix,
                                                        ReceiveThreads,
                                                        ReceiveRAM)

    ReceiveAlignmentFileNameAndPath=megmapProcessorClassHandler.Alignment()
    FunctionalHitToCount(TakeAlignmetnTabFile=ReceiveAlignmentFileNameAndPath,
                         TakeThread=ReceiveThreads).ReadFileInMemory()
