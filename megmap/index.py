from optparse import OptionParser, OptionGroup
import sys
import os
from multiprocessing import Queue, Process, cpu_count
from megmap.indexModule.indexCollector import indexEntry


__author__ = "Daniel H. Huson and Anupam Gautam"

# def mainFunction(args):
#     print(hello)
def main():
    parser = OptionParser("%prog [options] infile",
                          description="Index generator for metagenome mapping utilities",
                          epilog=__author__)

    parser.add_option('--d', action="store",dest="database",
                       help="provide database fasta file",metavar="database")
    parser.add_option('--out', action="store", dest="output",
                      help="output file name", metavar="output" )

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
    parser.add_option_group(aligner)
   #################General support and parameter#################
   #################General support and parameter#################
   #################General support and parameter#################
   #################General support and parameter#################
   #################General support and parameter#################
   #################General support and parameter#################

    GeneralParameter = OptionGroup(parser, "General Parameter")
    GeneralParameter.add_option('--t',action="store",dest='threads', default=cpu_count(),
                       help='Enter number of threads', metavar='threads')
    GeneralParameter.add_option('--ram',action="store",dest='ram', default="4gb",
                       help='Enter ram in gb you want to use [Default: 2gb]',metavar='ram')
    # parser.add_option(GeneralParameter)

    parser.add_option_group(GeneralParameter)
    (options, args) = parser.parse_args()

    if not options.database:
        raise IOError("OSError: Must specify --d database fasta file name or  -h/--help to print options  (use - for stdin)")
    elif not options.output:
        raise IOError("OSError: Must specify --out file name or  -h/--help to print options  (use - for stdin)")
    elif not options.tool:
        raise IOError("OSError: Must specify --al tool name or  -h/--help to print options  (use - for stdin)")


    indexEntry(ReceiveDatabaseFastaFile=options.database, ReceiveOutput=options.output, ReceiveTool=options.tool,ReceiveToolPath=options.toolpath, ReceiveThreads=options.threads, ReceiveRAM=options.ram)

if __name__ == '__main__':
	main()
