import sys
import time
import datetime
import tarfile
import gzip
import shutil
import os

def gb_to_mb(gb):
    #######convert gb to mb
	return(int(gb.replace("gb",""))*1024)

class tarDir:
        def __init__(self,InputDirectoryPathToTar):

            self.InputDirectoryPathToTar=InputDirectoryPathToTar


        def tarIt(self):
            tar = tarfile.open(str(self.InputDirectoryPathToTar)+".tar.gz", "w:gz")
            tar.add(str(self.InputDirectoryPathToTar), arcname=os.path.basename(os.path.abspath(self.InputDirectoryPathToTar.strip("\n"))))
            tar.close()
            shutil.rmtree(str(self.InputDirectoryPathToTar), ignore_errors=True)

class OutputDirectoryGenerator:
 
    def __init__(self, TakeDir,TakeMode):
        self.TakeDir = TakeDir
        self.TakeMode = TakeMode

    def DicGenAndCheck(self):
        if not self.TakeDir:
            # print(os.path.abspath(os.getcwd()))
            x=datetime.datetime.now()
            x=str(x).replace(" ","_").replace("/", "")
            NameDir=self.TakeMode+x
            ModeDir=os.path.join(os.path.abspath(os.getcwd()),NameDir)
            os.mkdir(ModedDir)
            return(ModeDir)
        else:
            if os.path.isdir(os.path.abspath(self.TakeDir)):
                x=datetime.datetime.now()
                x=str(x).replace(" ","_").replace("/", "")
                NameDir=self.TakeMode+x
                ModeDir=os.path.join(os.path.abspath(self.TakeDir),NameDir)
                os.mkdir(ModeDir)
                return(ModeDir)
            else:
                os.mkdir(os.path.abspath(self.TakeDir))
                x=datetime.datetime.now()
                x=str(x).replace(" ","_").replace("/", "")
                NameDir=self.TakeMode+x
                ModeDir=os.path.join(os.path.abspath(self.TakeDir),NameDir)
                os.mkdir(ModeDir)
                return(ModeDir)