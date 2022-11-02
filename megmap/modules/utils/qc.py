import filetype
import os
import traceback

class ClassQC:

    def __init__(self,TakeFile: str="" ,TakeReadMode: str="", TakeMappingDir: str="",
                 TakeMappingPrefix: str="", TakeMappingdb: str="", TakeLogFile: str="")->None:

        self.TakeFile=TakeFile
        self.TakeReadMode=TakeReadMode
        self.TakeMappingDir=TakeMappingDir
        self.TakeMappingPrefix=TakeMappingPrefix
        self.TakeMappingdb=TakeMappingdb
        self.TakeLogFile=TakeLogFile

    def __extensionType__(self)->bool:

        FileExtension=filetype.guess(self.TakeFile)

        if FileExtension is None:

            return(self.__CheckIfFasta__(self.TakeFile,FileExtension))

        else:
            if FileExtension.extension in ["gz","bz2","zip"]:
                raise IOError("OSError: blast doesn't support compressed files with the extensions .gz, .bz2, and .gzip, please uncompress your fasta file and then use megmap")
            elif FileExtension.extension in ["txt"]:
                return(self.__CheckIfFasta__(self.TakeFile,FileExtension))
            else:
                raise IOError("Sorry, no support for file format {}".format(FileExtension.mime))


    def __checkMappingFiles__(self)->bool:

        mapFile=os.path.join(self.TakeMappingDir,str(str(self.TakeMappingPrefix)+".map"))
        treFile=os.path.join(self.TakeMappingDir,str(str(self.TakeMappingPrefix)+".tre"))
        acessionToClassificationMapFile=os.path.join(self.TakeMappingDir,str(str("acc2")+str(self.TakeMappingPrefix)+".map"))       
        try:
            counter=0
            if (os.path.exists(mapFile) and os.path.getsize(mapFile)>0):
                counter=counter+1
            else:
                raise IOError("Sorry, something is wrong with your "+str(mapFile)+" file")
            if (os.path.exists(treFile) and os.path.getsize(treFile)>0):
                counter=counter+1
            else:
                raise IOError("Sorry, something is wrong with your "+str(treFile)+" file")
            if self.TakeMappingdb:
                if os.path.exists(os.path.abspath(self.TakeMappingdb)):
                    counter=counter+1
                else:
                    raise IOError("Sorry, something is wrong with your "+str(self.TakeMappingdb)+" file")
            else:
                if(os.path.exists(acessionToClassificationMapFile) and os.path.getsize(acessionToClassificationMapFile)>0):
                    counter=counter+1
                else:
                    raise IOError("Sorry, something is wrong with your "+str(acessionToClassificationMapFile)+" file")

            if counter==3:
                return (True)
            elif counter<3:
                return (False)

        except Exception:

            traceback.print_exc()
            return(False)



    @staticmethod
    def __CheckIfFasta__(FastaFile: str="", ExtensionOfFile: str="")->bool:

        if ExtensionOfFile is None:
            FileRead=open(FastaFile,"r")
            counter=0
            try:
                for line in FileRead:
                    if '>' in line:
                        counter=counter+1
                        if counter > 10000:
                            break

                FileRead.close()
                if counter>0:
                    return (True)
                else:
                    return (False)
            except:
                return (False)





