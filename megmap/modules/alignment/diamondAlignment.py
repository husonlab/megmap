import os

class DiamondAlignment:

    def __init__(self, QueryFile: str ="", DatabaseIndex: str ="",
                 OutputDirName: str ="", OutputFileName: str ="",
                 ToolPath: str ="", Identity: int="",
                 Coverage: int="", Evalue: str ="",
                 frameshift: int="",
                 ReadMode: str ="", Threads: int="",
                 RAM: str = "", TopPercentage: int="")->None:

        self.QueryFile=QueryFile
        self.DatabaseIndex=DatabaseIndex
        self.OutputDirName=OutputDirName
        self.OutputFileName=OutputFileName
        self.ToolPath=ToolPath
        self.Identity=Identity
        self.Coverage=Coverage
        self.Evalue=Evalue
        self.frameshift=frameshift
        self.ReadMode=ReadMode
        self.Threads=Threads
        self.RAM=RAM
        self.TopPercentage=TopPercentage
        print(self.Identity)
        print(self.Coverage)

    def normalDIAlcommand(self)->str:

        if self.ReadMode=='short':
            os.system("diamond blastx --query  "+str(self.QueryFile)+" --db  "+str(self.DatabaseIndex)+" --out "+str(os.path.join(self.OutputDirName,self.OutputFileName))+" --id  "+str(self.Identity)+" --query-cover  "+str(self.Coverage)+" --evalue "+str(self.Evalue)+" --threads  "+str(self.Threads)+" --outfmt 6 qseqid sseqid pident length mismatch gapopen qstart qend qlen sstart send slen evalue bitscore qcovhsp ")
            return(os.path.join(self.OutputDirName,self.OutputFileName))

        elif self.ReadMode=='long':
            os.system("diamond blastx --query  "+str(self.QueryFile)+" --db  "+str(self.DatabaseIndex)+" --out "+str(os.path.join(self.OutputDirName,self.OutputFileName))+" --id  "+str(self.Identity)+" --query-cover  "+str(self.Coverage)+" --evalue "+str(self.Evalue)+" --threads  "+str(self.Threads)+"  --range-culling --top "+str(self.TopPercentage)+" -F "+str(self.frameshift)+" --outfmt 6 qseqid sseqid pident length mismatch gapopen qstart qend qlen sstart send slen evalue bitscore qcovhsp  ")
            return(os.path.join(self.OutputDirName,self.OutputFileName))

        else:
            raise IOError("Sorry, {} read mode is not supported, please look at --readMode flag ".format(self.ReadMode))

    def WithPathDIAlcommand(self)->str:

        if self.ReadMode=='short':
            os.system(os.path.join(os.path.abspath(self.ToolPath),"diamond")+"  blastx --query  "+str(self.QueryFile)+" --db  "+str(self.DatabaseIndex)+" --out "+str(os.path.join(self.OutputDirName,self.OutputFileName))+" --id  "+str(self.Identity)+" --query-cover  "+str(self.Coverage)+" --evalue "+str(self.Evalue)+" --threads  "+str(self.Threads)+" --outfmt 6 qseqid sseqid pident length mismatch gapopen qstart qend qlen sstart send slen evalue bitscore qcovhsp ")
            return(os.path.join(self.OutputDirName,self.OutputFileName))

        elif self.ReadMode=='long':
            os.system(os.path.join(os.path.abspath(self.ToolPath),"diamond")+"  blastx --query  "+str(self.QueryFile)+" --db  "+str(self.DatabaseIndex)+" --out "+str(os.path.join(self.OutputDirName,self.OutputFileName))+" --id  "+str(self.Identity)+" --query-cover  "+str(self.Coverage)+" --evalue "+str(self.Evalue)+" --threads  "+str(self.Threads)+" --range-culling --top "+str(self.TopPercentage)+" -F "+str(self.frameshift)+"  --outfmt 6 qseqid sseqid pident length mismatch gapopen qstart qend qlen sstart send slen evalue bitscore qcovhsp ")
            return(os.path.join(self.OutputDirName,self.OutputFileName))

        else:
            raise IOError("Sorry, {} read mode is not supported, please look at --readMode flag ".format(self.ReadMode))

