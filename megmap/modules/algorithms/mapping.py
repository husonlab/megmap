from ete3 import Tree
import pandas as pd
import mmap
from multiprocessing import  Pool


class MappingHitToAnnotation:

    def __init__(self, TakeInputTempFile: str="",TakeOutFileName: str="",  TakeTreeFile: str="",
                 TakeMapFile: str="", TakeAccMapFile: str="",TakeThread: int="")->None:

        self.TakeInputTempFile=TakeInputTempFile
        self.TakeOutFileName=TakeOutFileName
        self.TakeTreeFile=TakeTreeFile
        self.TakeMapFile=TakeMapFile
        self.TakeAccMapFile=TakeAccMapFile
        self.TakeThread=TakeThread
        self.tree =Tree(self.TakeTreeFile,format=8)
        self.root=self.tree.get_tree_root().name
        d = {}
        with open(self.TakeMapFile) as f:
            for line in f:
                (key, val) = line.strip("\n").split("\t")
                d[key] = val
        self.MapFiledictionary=d

    def __ReadMergeDistribute__(self)->None:
        
        accmapFile=pd.read_csv(self.TakeAccMapFile,sep="\t",
                               names=['FastaAccession','TreeLeafOrNodeID'],
                               header=None)
        
        with open(self.TakeInputTempFile, "r+b") as f:

            map_file = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
            lineCounter=0
            counter=0
            sumCounter=0
            for line in iter(map_file.readline, b""):
                line=line.decode("utf-8")
                if lineCounter==0:
                    keys=line.strip("\n").split("\t")
                    lineCounter=lineCounter+1
                    Mydict = dict([(key, []) for key in keys])
                else:
                    counter=counter+1
                    Mydict = self.dictionaryAppender(keys,Mydict,line)
                    
                    if counter>=2999:
                        if Mydict['qseqid'][-1]==Mydict['qseqid'][-2]:

                            continue
                        else:
                            counter=0
                            MyFrame=pd.DataFrame.from_dict(Mydict)
                            MyFrame = MyFrame[keys]
                            MyFrame['bitscore'] = MyFrame['bitscore'].astype(float)
                            MyFrame = MyFrame[:-1]###remove last row of dataframe 
                            MyFrame=pd.merge(MyFrame,accmapFile,
                                            left_on='sseqid',right_on='FastaAccession',
                                            how="left")
                            MyFrame = MyFrame[MyFrame['TreeLeafOrNodeID'].notna()]
                            
                            dfReturned=self.__map__(MyFrame, self.__SendToTree__)
                            
                            if sumCounter==0:
                                dfToWrite=dfReturned
                                sumCounter=sumCounter+1
                            else:
                                dfToWrite = pd.concat([dfToWrite, dfReturned]).groupby('path')['freq'].sum().reset_index()
                    
                            
                            Mydict = dict([(key, []) for key in keys])
                            Mydict = self.dictionaryAppender(keys,Mydict,line)

            # print(Mydict)

        MyFrame=pd.DataFrame.from_dict(Mydict)
        MyFrame = MyFrame[keys]
        MyFrame['bitscore'] = MyFrame['bitscore'].astype(float)
        MyFrame=pd.merge(MyFrame,accmapFile,
                        left_on='sseqid',right_on='FastaAccession',
                        how="left")
        MyFrame = MyFrame[MyFrame['TreeLeafOrNodeID'].notna()]
        
        dfReturned=self.__map__(MyFrame, self.__SendToTree__)
        if sumCounter==0:
            dfToWrite=dfReturned
        else:
            dfToWrite = pd.concat([dfToWrite, dfReturned]).groupby('path')['freq'].sum().reset_index()
        
        map_file.close()

        dfToWrite.sort_values(by='freq', ascending=False).to_csv(self.TakeOutFileName,
                                                                 sep="\t",
                                                                 index=False,
                                                                 header=[self.MapFiledictionary[self.root],"count"])

    def __map__(self,TakeDataframe,Process):


        dataframeSplit=TakeDataframe.groupby('qseqid')
        pool = Pool(int(self.TakeThread))
        dataframe = pd.concat(pool.map(Process, [group for name, group in dataframeSplit]))
        pool.close()
        pool.join()

        dataframe=dataframe.drop(columns=['qseqid'])
        dataframe=dataframe.value_counts().rename_axis('path').reset_index(name='freq')

        return(dataframe)
        # if dataframe.empty==False:
        #     dataframe.to_csv(self.TakeOutFileNameTemp, sep="\t", mode='a', index=False, header=False)

  
    def __SendToTree__(self,dfsplit):

        filt =  dfsplit[dfsplit.groupby(['qseqid'])['bitscore'].transform(max) == dfsplit['bitscore']].drop_duplicates(["qseqid","TreeLeafOrNodeID"],keep='first').reset_index(drop=True)
        return(self.__pathAndName__(filt))


    def __pathAndName__(self,dfsplit):

        dfToStore = pd.DataFrame(columns=['qseqid', 'path'])

        for index, row in dfsplit.iterrows():
            path = []
            name =[]
            # print(row['c1'], row['c2'])
            # print(row['TreeLeafOrNodeID'])
            D = self.tree.search_nodes(name=str(row['TreeLeafOrNodeID']))
            node = D
            for i in range(0,len(node)):
                for value in node[i]:
                    while value.up:
                        path.append(value.name)
                        name.append(self.MapFiledictionary[value.name])
                        value = value.up
                    path.append(self.root)
                    name.append(self.MapFiledictionary[self.root])
                    dfToStore = pd.concat([dfToStore, pd.DataFrame([{'qseqid': row['qseqid'], 'path':str(", ".join(name[::-1]))}])])

        return(dfToStore)

    @staticmethod    
    def dictionaryAppender(Takekeys,dictToAppend,lineToAppend):
        lineToAppend=lineToAppend.strip("\n").split("\t")
        for i in range(0,len(Takekeys)):
            dictToAppend[Takekeys[i]].append(lineToAppend[i])
        return(dictToAppend)