import os

class BlastIndexGenerator:

    def __init__(self,DatabaseFastaFile: str ="", OutputFileName: str ="", ToolPath: str =""):

        self.DatabaseFastaFile=DatabaseFastaFile
        self.OutputFileName=OutputFileName
        self.ToolPath=ToolPath

    def normalBcommand(self)->None:
    	os.system("makeblastdb -in "+str(self.DatabaseFastaFile)+" -out   "+str(self.OutputFileName)+" -dbtype prot")

    def WithPathBcommand(self)->None:
    	os.system(os.path.join(os.path.abspath(self.ToolPath),"makeblastdb")+" -in "+str(self.DatabaseFastaFile)+" -out   "+str(self.OutputFileName)+" -dbtype prot")