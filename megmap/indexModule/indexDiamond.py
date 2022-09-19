import os

class DiamondIndexGenerator:

    def __init__(self,DatabaseFastaFile: str ="", OutputFileName: str ="", ToolPath: str ="", Threads: int="",RAM: str = ""):

        self.DatabaseFastaFile=DatabaseFastaFile
        self.OutputFileName=OutputFileName
        self.ToolPath=ToolPath
        self.Threads=Threads
        self.RAM=RAM

    def normalDIcommand(self)->None:
    	os.system("diamond makedb --in "+str(self.DatabaseFastaFile)+" -d  "+str(self.OutputFileName)+" --threads  "+str(self.Threads))

    def WithPathDIcommand(self)->None:
    	os.system(os.path.join(os.path.abspath(self.ToolPath),"diamond")+" makedb --in "+str(self.DatabaseFastaFile)+" -d  "+str(self.OutputFileName)+" --threads  "+str(self.Threads))