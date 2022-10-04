from optparse import OptionParser, OptionGroup
import sys
import os
from multiprocessing import Queue, Process, cpu_count
from megmap.modules.collector import megmapEntry


__author__ = "Daniel H. Huson and Anupam Gautam"

# def mainFunction(args):
#     print(hello)
def main():
    parser = OptionParser("%prog [options] infile",
                          description="Metagenome mapping utilities",
                          epilog=__author__)


    parser.add_option('--in', action="store", dest="inputFile",
                       help="provide input fasta file",metavar="inputFile")
    parser.add_option('--out',default="megmap", action="store", dest="output",
                      help="output folder path [Default: megmap]", metavar="output" )
    parser.add_option('--d', action="store",dest="database",
                       help="provide database",metavar="database")
   #################Aligner support and parameter#################
   #################Aligner support and parameter#################
   #################Aligner support and parameter#################
   #################Aligner support and parameter#################
   #################Aligner support and parameter#################
   #################Aligner support and parameter#################
    aligner = OptionGroup(parser,"Aligner Parameter")

    aligner.add_option('--al', default='diamond', action="store",dest="tool", 
                       help="Enter tool to use for alignment diamond, blast etc [Default: diamond]",metavar="tool")
    aligner.add_option('--tp', default='', action="store",dest="toolpath", 
                       help="Enter path to tool to use for alignment diamond, blast etc",metavar="toolpath")
    aligner.add_option('--id', default=70, action="store",dest="alignmentidentity", 
                       help="minimum identity% to report an alignment, [Default: 70]",metavar="alignmentidentity")
    aligner.add_option('--c', dest="alignmentcoverage", action="store", default=70,
                       help='Enter alignment coverage for the longer sequence, if set to 70 the alignment must covers 70%% of the sequence [Default: 70]',metavar='alignmentcoverage')
    aligner.add_option('--evalue', dest="evalue", action="store", default='1e-05',
                       help='Enter max E-value for hit to be consider. [Default: 1e-05, max=0.01]',metavar='evalue')
    parser.add_option_group(aligner)

   #################General support and parameter#################
   #################General support and parameter#################
   #################General support and parameter#################
   #################General support and parameter#################
   #################General support and parameter#################
   #################General support and parameter#################

    GeneralParameter = OptionGroup(parser, "General Parameter")
    GeneralParameter.add_option('--p',action="store",dest='prefix', default="prefix",
                       help='Enter prefix', metavar='prefix')
    GeneralParameter.add_option('--readMode',action="store",dest='readMode', default="short",
                       help='Enter short for short read file and long for long reads file  [Default: short]', metavar='readMode')
    GeneralParameter.add_option('--t',action="store",dest='threads', default=cpu_count(),
                       help='Enter number of threads', metavar='threads')
    GeneralParameter.add_option('--ram',action="store",dest='ram', default="4gb",
                       help='Enter ram in gb you want to use [Default: 2gb]',metavar='ram')
    # parser.add_option(GeneralParameter)

    parser.add_option_group(GeneralParameter)
    (options, args) = parser.parse_args()


    if not options.inputFile:
        raise IOError("OSError: Must specify --in fastq or fasta or  -h/--help to print options  (use - for stdin)")
    elif not options.output:
        raise IOError("OSError: Must specify --out file name or  -h/--help to print options  (use - for stdin)")
    elif not options.database:
        raise IOError("OSError: Must specify --d database file name or  -h/--help to print options  (use - for stdin)")
    elif not options.tool:
        raise IOError("OSError: Must specify --al tool name or  -h/--help to print options  (use - for stdin)")



    megmapEntry(ReceiveInputFile=options.inputFile, ReceiveOutput=options.output,
                ReceiveDatabase=options.database, ReceiveTool=options.tool,
                ReceiveToolPath=options.toolpath, ReceiveAlignmentIdentity=options.alignmentidentity,
                ReceiveAlignmentCoverage=options.alignmentcoverage, ReceiveEvalue=options.evalue,
                ReceivePrefix=options.prefix, ReceiveReadMode=options.readMode,
                ReceiveThreads=options.threads, ReceiveRAM=options.ram)

if __name__ == '__main__':
	main()
