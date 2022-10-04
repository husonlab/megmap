import os

class DiamondAlignment:

    def __init__(self, QueryFile: str ="", DatabaseIndex: str ="", OutputDirName: str ="", OutputFileName: str ="", ToolPath: str ="", Identity: int="", Coverage: int="", Evalue: str ="", Threads: int="",RAM: str = "")->None:

        self.QueryFile=QueryFile
        self.DatabaseIndex=DatabaseIndex
        self.OutputDirName=OutputDirName
        self.OutputFileName=OutputFileName
        self.ToolPath=ToolPath
        self.Identity=Identity
        self.Coverage=Coverage
        self.Evalue=Evalue
        self.Threads=Threads
        self.RAM=RAM

    def normalDIAlcommand(self)->str:
        os.system("diamond blastx --query  "+str(self.QueryFile)+" --db  "+str(self.DatabaseIndex)+" --out "+str(os.path.join(self.OutputDirName,self.OutputFileName))+" --id  "+str(self.Identity)+" --query-cover  "+str(self.Coverage)+" --evalue "+str(self.Evalue)+" --threads  "+str(self.Threads)+" --outfmt 6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovhsp ")
        return(os.path.join(self.OutputDirName,self.OutputFileName))

    def WithPathDIAlcommand(self)->str:
        os.system(os.path.join(os.path.abspath(self.ToolPath),"diamond")+"  blastx --query  "+str(self.QueryFile)+" --db  "+str(self.DatabaseIndex)+" --out "+str(os.path.join(self.OutputDirName,self.OutputFileName))+" --id  "+str(self.Identity)+" --query-cover  "+str(self.Coverage)+" --evalue "+str(self.Evalue)+" --threads  "+str(self.Threads)+" --outfmt 6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovhsp ")
        return(os.path.join(self.OutputDirName,self.OutputFileName))