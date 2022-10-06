import filetype

class ClassQC:

    def __init__(self,TakeFile: str="" ,TakeReadMode: str="",  TakeLogFile: str="")->None:

        self.TakeFile=TakeFile
        self.TakeReadMode=TakeReadMode
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





