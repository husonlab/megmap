import os
from megmap.indexModule.indexDiamond import DiamondIndexGenerator

class IndexGeneratorClass:

    def __init__(self,TakeDatabaseFastaFile: str ="", TakeOutputFileName: str ="", TakeTool: str ="", TakeToolPath: str ="", TakeThreads: int="",TakeRAM: str =""):

        self.TakeDatabaseFastaFile = TakeDatabaseFastaFile
        self.TakeOutputFileName = TakeOutputFileName
        self.TakeTool = TakeTool
        self.TakeToolPath = TakeToolPath
        self.TakeThreads= TakeThreads
        self.TakeRAM= TakeRAM

    def distributor(self)->None:
        
        if self.TakeTool == 'diamond':
            DiamondIndexGeneratorHandler=DiamondIndexGenerator(self.TakeDatabaseFastaFile, self.TakeOutputFileName, self.TakeToolPath, self.TakeThreads, self.TakeRAM)

            if not self.TakeToolPath: ##check if self.TakeToolPath variable is empty
                DiamondIndexGeneratorHandler.normalDIcommand()
            else:
                DiamondIndexGeneratorHandler.WithPathDIcommand()






def indexEntry(ReceiveDatabaseFastaFile: str ="", ReceiveOutput: str = "megmap", ReceiveTool: str ="", ReceiveToolPath: str="",ReceiveThreads: int="",ReceiveRAM: str = "") -> None:

    IndexGeneratorClassHandler=IndexGeneratorClass(os.path.abspath(ReceiveDatabaseFastaFile), os.path.abspath(ReceiveOutput), ReceiveTool, ReceiveToolPath,ReceiveThreads,ReceiveRAM)
    IndexGeneratorClassHandler.distributor()



