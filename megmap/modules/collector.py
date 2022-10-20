import pandas as pd 
import numpy as np
import os
from megmap.modules.utils.qc import ClassQC
from megmap.modules.utils.utility import OutputDirectoryGenerator,tarDir,gb_to_mb
from megmap.modules.alignment.diamondAlignment import DiamondAlignment
from megmap.modules.alignment.blastAlignment import BlastAlignment
from megmap.modules.algorithms.HitToCount import FunctionalHitToCount
from megmap.modules.algorithms.mapping import MappingHitToAnnotation

class megmapProcessorClass:

    def __init__(self,TakeInputFile: str="", TakePathOfDir: str = "", TakeDatabase: str = "", TakeTool: str ="", TakeToolPath: str ="", TakeIdentity: int="", TakeAlignmentCoverage: int="", TakeEvalue: str="", TakePrefix: str="", TakeReadMode: str="",  TakeThreads: int="", TakeRAM: str = "", TakeTopPercentage: int="")->None:

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
        self.TakeTopPercentage= TakeTopPercentage



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

        elif self.TakeTool == 'blast':
            BlastAlignmentHandler=BlastAlignment(self.TakeInputFile,
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
                AlignmentFileNameAndPath=BlastAlignmentHandler.normalBAlcommand()
            else:
                AlignmentFileNameAndPath=BlastAlignmentHandler.WithPathBAlcommand()
            return(AlignmentFileNameAndPath)

def megmapEntry(ReceiveInputFile: str ="", ReceiveOutput: str = "megmap",
                ReceiveDatabase: str = "", ReceiveMappingDir: str = "",
                ReceiveMappingPrefix: str = "", ReceiveTool: str ="",
                ReceiveToolPath: str="", ReceiveAlignmentIdentity: int=70,
                ReceiveAlignmentCoverage: int=70, ReceiveEvalue: str="",
                ReceivePrefix: str="", ReceiveReadMode: str="",
                ReceiveThreads: int="", ReceiveRAM: str = "",
                ReceiveTopPercentage: int = 10) -> None:

    DirectoryCaller=OutputDirectoryGenerator(os.path.abspath(ReceiveOutput),'megmap')
    PathOfDir=DirectoryCaller.DicGenAndCheck()
    print(PathOfDir)
    LogFilePath=""
    QCHanlder=ClassQC(ReceiveInputFile,ReceiveReadMode,os.path.abspath(ReceiveMappingDir),
                      ReceiveMappingPrefix,LogFilePath)
    checkMappingFiles=QCHanlder.__checkMappingFiles__()
    if ReceiveTool=='blast':

        returnQC=QCHanlder.__extensionType__()
        
        if returnQC==False:
            raise IOError("Sorry, something is wrong with your file format")

    elif ReceiveTool=='diamond':
        if checkMappingFiles==False:
            raise IOError("Sorry, something is wrong with your file format")


    megmapProcessorClassHandler=megmapProcessorClass(os.path.abspath(ReceiveInputFile),
                                                        PathOfDir, 
                                                        os.path.abspath(ReceiveDatabase), 
                                                        ReceiveTool, 
                                                        ReceiveToolPath,
                                                        ReceiveAlignmentIdentity,
                                                        ReceiveAlignmentCoverage,
                                                        ReceiveEvalue,
                                                        ReceivePrefix,
                                                        ReceiveReadMode,
                                                        ReceiveThreads,
                                                        ReceiveRAM,
                                                        ReceiveTopPercentage)

    ReceiveAlignmentFileNameAndPath=megmapProcessorClassHandler.Alignment()

    TempFilePath=FunctionalHitToCount(TakeAlignmentTabFile=ReceiveAlignmentFileNameAndPath,
                         TakeOutFileName=str(os.path.join(os.path.abspath(PathOfDir),ReceivePrefix))+"Count.txt",
                         TakeAligner=ReceiveTool,
                         TakeIdentity=ReceiveAlignmentIdentity,
                         TakeAlignmentCoverage=ReceiveAlignmentCoverage,
                         TakeMappingDir=os.path.abspath(ReceiveMappingDir),
                         TakeMappingPrefix=ReceiveMappingPrefix,
                         TakeThread=ReceiveThreads,
                         TakeTopPercentage=ReceiveTopPercentage).ReadFileInMemory()

    MappingHitToAnnotation(TakeInputTempFile=TempFilePath,
                           TakeOutFileName=str(os.path.join(os.path.abspath(PathOfDir),ReceivePrefix))+"Count.txt",
                           TakeTreeFile=os.path.abspath(os.path.join(ReceiveMappingDir,str(str(ReceiveMappingPrefix)+".tre"))),
                           TakeMapFile=os.path.abspath(os.path.join(ReceiveMappingDir,str(str(ReceiveMappingPrefix)+".map"))),
                           TakeAccMapFile=os.path.abspath(os.path.join(ReceiveMappingDir,str(str("acc2")+str(ReceiveMappingPrefix)+".map"))),
                           TakeThread=ReceiveThreads).__ReadMergeDistribute__()
