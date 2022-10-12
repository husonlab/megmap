import mmap
import pandas as pd
import numpy as np
from multiprocessing import  Pool

class FunctionalHitToCount:

    def __init__(self,TakeAlignmetnTabFile: str="", TakeOutFileName: str="", TakeAligner: str="", TakeIdentity: str="", TakeAlignmentCoverage: str="", TakeThread: int="", TakeTopPercentage: int="")->None:

        self.TakeAlignmetnTabFile=TakeAlignmetnTabFile
        self.TakeOutFileName=TakeOutFileName
        self.TakeOutFileNameTemp=str(TakeOutFileName)+".temp"
        self.TakeAligner=TakeAligner
        self.TakeIdentity=TakeIdentity
        self.TakeAlignmentCoverage=TakeAlignmentCoverage
        self.TakeThread=TakeThread
        self.TakeTopPercentage=TakeTopPercentage



    def ReadFileInMemory(self):
        
        with open(self.TakeAlignmetnTabFile, "r+b") as f:

            map_file = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
            counter=0
            keys=["qseqid","sseqid","pident",
                  "length","mismatch","gapopen",
                  "qstart","qend","qlen","sstart",
                  "send","slen","evalue","bitscore",
                  "qcovhsp"]

            TempFileHandler=open(self.TakeOutFileNameTemp, 'w')
            if self.TakeAligner =='blast':
                TempFileHandler.write(str("\t".join(keys))+"\t"+"PercentCoverageQuery"+"\n")
            else:
                TempFileHandler.write(str("\t".join(keys))+"\n")

            TempFileHandler.close()

            Mydict = dict([(key, []) for key in keys])
            for line in iter(map_file.readline, b""):
                line=line.decode("utf-8")
                counter=counter+1

                Mydict = self.dictionaryAppender(Mydict,line)
                if counter>=2000:
                    if Mydict['qseqid'][-1]==Mydict['qseqid'][-2]:

                        continue
                    else:
                        counter=0
                        MyFrame=pd.DataFrame.from_dict(Mydict)
                        MyFrame = MyFrame[keys]
                        MyFrame['bitscore'] = MyFrame['bitscore'].astype(float)
                        MyFrame = MyFrame[:-1]###remove last row of dataframe 
                    
                        if self.TakeAligner =='blast':
                            MyFrame=self.blastQueryCoverage(MyFrame)
                    
                        self.ParallelizeDataframe(MyFrame, self.InitialProcess)
                        Mydict = dict([(key, []) for key in keys])
                        Mydict = self.dictionaryAppender(Mydict,line)

            # print(Mydict)

        MyFrame=pd.DataFrame.from_dict(Mydict)
        MyFrame = MyFrame[keys]
        MyFrame['bitscore'] = MyFrame['bitscore'].astype(float)
        if self.TakeAligner =='blast':
            MyFrame=self.blastQueryCoverage(MyFrame)

        self.ParallelizeDataframe(MyFrame, self.InitialProcess)


        map_file.close()


    def ParallelizeDataframe(self,TakeDataframe,Process):


        dataframeSplit=TakeDataframe.groupby('qseqid')
        pool = Pool(int(self.TakeThread))
        dataframe = pd.concat(pool.map(Process, [group for name, group in dataframeSplit]))
        pool.close()
        pool.join()
        if dataframe.empty==False:
            dataframe.to_csv(self.TakeOutFileNameTemp, sep="\t", mode='a', index=False, header=False)

        # dataframeSplit = np.array_split(TakeDataframe, int(self.TakeThread))
        # pool = Pool(int(self.TakeThread))
        # dataframe = pd.concat(pool.map(Process, dataframeSplit))
        # pool.close()
        # pool.join()
        # print(dataframe)

    
    def InitialProcess(self,dfsplit):

        n=(100-int(self.TakeTopPercentage))/100
        filt = (dfsplit.sort_values(by='bitscore',ascending=False)
                .groupby('qseqid',group_keys=False)
                .apply(lambda x:x[x['bitscore'].astype(float)>=float(x['bitscore'].astype(float).max())*float(n)])
                .reset_index(drop=True))

        # firstMerge = pd.merge(dfsplit,filt,on=['qseqid','bitscore'])
        # filt1 = dfsplit.groupby(['qseqid'])['evalue'].min().to_frame().reset_index()
        # final = pd.merge(firstMerge,filt1,on=['qseqid','evalue'])
        return(filt)
        # filt = dfsplit.groupby(['qseqid'])['bitscore'].max().to_frame().reset_index()
        # #print(filt)
        # firstMerge = pd.merge(dfsplit,filt,on=['qseqid','bitscore'])
        # filt1 = dfsplit.groupby(['qseqid'])['evalue'].min().to_frame().reset_index()
        # final = pd.merge(firstMerge,filt1,on=['qseqid','evalue'])
        # return(final)

    def blastQueryCoverage(self,dataFrame):
        dataFrame['PercentCoverageQuery'] = ((dataFrame['qend'].astype(int)-dataFrame['qstart'].astype(int)+1)/dataFrame['qlen'].astype(int))*100
        dataFrame=dataFrame[(dataFrame['PercentCoverageQuery']>=float(self.TakeAlignmentCoverage)) & (dataFrame['pident'].astype(float)>=float(self.TakeIdentity))]
        return(dataFrame)

    @staticmethod    
    def dictionaryAppender(dictToAppend,lineToAppend):
        lineToAppend=lineToAppend.strip("\n").split("\t")
        dictToAppend['qseqid'].append(lineToAppend[0])
        dictToAppend['sseqid'].append(lineToAppend[1])
        dictToAppend['pident'].append(lineToAppend[2])
        dictToAppend['length'].append(lineToAppend[3])
        dictToAppend['mismatch'].append(lineToAppend[4])
        dictToAppend['gapopen'].append(lineToAppend[5])
        dictToAppend['qstart'].append(lineToAppend[6])
        dictToAppend['qend'].append(lineToAppend[7])
        dictToAppend['qlen'].append(lineToAppend[8])
        dictToAppend['sstart'].append(lineToAppend[9])
        dictToAppend['send'].append(lineToAppend[10])
        dictToAppend['slen'].append(lineToAppend[11])
        dictToAppend['evalue'].append(lineToAppend[12])
        dictToAppend['bitscore'].append(lineToAppend[13])
        dictToAppend['qcovhsp'].append(lineToAppend[14])
        return(dictToAppend)
