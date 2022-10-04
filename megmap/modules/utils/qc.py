import filetype

class ClassQC:

    def __init__(self,TakeFile: str="" ,TakeReadMode: str="",  TakeLogFile: str="")->None:

        self.TakeFile=TakeFile
        self.TakeReadMode=TakeReadMode
        self.TakeLogFile=TakeLogFile

    def __extensionType__(self)->bool:

        FileExtension=filetype.guess(self.TakeFile)
        if FileExtension.extension is None:

            self.__CheckIfFasta__(self.TakeFile,FileExtension.extension)

        elif FileExtension.extension in ["gz","bz2","gzip"]:
        	raise IOError("OSError: blast doesn't support compressed files with the extensions .gz, .bz2, and .gzip, please uncompress your fasta file and then use megmap")


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
            except:
                return (False)





