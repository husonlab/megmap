import mmap
import pandas as pd
import numpy as np
from multiprocessing import  Pool

class FunctionalHitToCount:

    def __init__(self,TakeAlignmetnTabFile: str="",TakeThread: int="")->None:

        self.TakeAlignmetnTabFile=TakeAlignmetnTabFile
        self.TakeThread=TakeThread



    def ReadFileInMemory(self):
        
        with open(self.TakeAlignmetnTabFile, "r+b") as f:

            map_file = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
            counter=0
            keys=["qseqid","sseqid","pident",
                  "length","mismatch","gapopen",
                  "qstart","qend","sstart","send",
                  "evalue","bitscore","qcovhsp"]
            Mydict = dict([(key, []) for key in keys])
            for line in iter(map_file.readline, b""):
                line=line.decode("utf-8")
                line=line.strip("\n").split("\t")
                counter=counter+1
                Mydict['qseqid'].append(line[0])
                Mydict['sseqid'].append(line[1])
                Mydict['pident'].append(line[2])
                Mydict['length'].append(line[3])
                Mydict['mismatch'].append(line[4])
                Mydict['gapopen'].append(line[5])
                Mydict['qstart'].append(line[6])
                Mydict['qend'].append(line[7])
                Mydict['sstart'].append(line[8])
                Mydict['send'].append(line[9])
                Mydict['evalue'].append(line[10])
                Mydict['bitscore'].append(line[11])
                Mydict['qcovhsp'].append(line[12])
        
                if counter==1000:
                    counter=0
                    MyFrame=pd.DataFrame.from_dict(Mydict)
                    MyFrame = MyFrame[keys]
                    self.ParallelizeDataframe(MyFrame, self.InitialProcess)
                    Mydict = dict([(key, []) for key in keys])

            # print(Mydict)

        MyFrame=pd.DataFrame.from_dict(Mydict)
        MyFrame = MyFrame[keys]
        map_file.close()

    def ParallelizeDataframe(self,TakeDataframe,Process):

        dataframeSplit = np.array_split(TakeDataframe, int(self.TakeThread))
        pool = Pool(int(self.TakeThread))
        dataframe = pd.concat(pool.map(Process, dataframeSplit))
        pool.close()
        pool.join()
        print(dataframe)

    @staticmethod
    def InitialProcess(dfsplit):
        filt = dfsplit.groupby(['qseqid'])['bitscore'].max().to_frame().reset_index()
        #print(filt)
        firstMerge = pd.merge(dfsplit,filt,on=['qseqid','bitscore'])
        filt1 = dfsplit.groupby(['qseqid'])['evalue'].min().to_frame().reset_index()
        final = pd.merge(firstMerge,filt1,on=['qseqid','evalue'])
        return(final)


