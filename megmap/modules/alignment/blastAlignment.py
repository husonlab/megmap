import os

class BlastAlignment:

    def __init__(self, QueryFile: str ="", DatabaseIndex: str ="",
                 OutputDirName: str ="", OutputFileName: str ="",
                 ToolPath: str ="", Identity: int="",
                 Coverage: int="", Evalue: str ="",
                 ReadMode: str ="", Threads: int="",
                 RAM: str = "")->None:

        self.QueryFile=QueryFile
        self.DatabaseIndex=DatabaseIndex
        self.OutputDirName=OutputDirName
        self.OutputFileName=OutputFileName
        self.ToolPath=ToolPath
        self.Identity=Identity
        self.Coverage=Coverage
        self.Evalue=Evalue
        self.ReadMode=ReadMode
        self.Threads=Threads
        self.RAM=RAM

    def normalBAlcommand(self)->str:

        if (self.ReadMode=='short') or (self.ReadMode=='long'):
            os.system("blastx -query  "+str(self.QueryFile)+" -db  "+str(self.DatabaseIndex)+" -out "+str(os.path.join(self.OutputDirName,self.OutputFileName))+"  -qcov_hsp_perc  "+str(self.Coverage)+" -evalue "+str(self.Evalue)+" -num_threads  "+str(self.Threads)+" -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend qlen sstart send slen evalue bitscore qcovhsp' ")
            return(os.path.join(self.OutputDirName,self.OutputFileName))

        else:
            raise IOError("Sorry, {} read mode is not supported, please look at --readMode flag ".format(self.ReadMode))

    def WithPathBAlcommand(self)->str:

        if (self.ReadMode=='short') or (self.ReadMode=='long'):
            os.system(os.path.join(os.path.abspath(self.ToolPath),"blastx")+"  -query  "+str(self.QueryFile)+" -db  "+str(self.DatabaseIndex)+" -out "+str(os.path.join(self.OutputDirName,self.OutputFileName))+"  -qcov_hsp_perc  "+str(self.Coverage)+" -evalue "+str(self.Evalue)+" -num_threads  "+str(self.Threads)+" -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend qlen sstart send slen evalue bitscore qcovhsp' ")
            return(os.path.join(self.OutputDirName,self.OutputFileName))
        else:
            raise IOError("Sorry, {} read mode is not supported, please look at --readMode flag ".format(self.ReadMode))

