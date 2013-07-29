import sys
import logging
import parseFunctions as PF
from shutil import copyfile
from optparse import OptionParser

logging.basicConfig(filename='monty.log',level=logging.DEBUG)
    

if __name__=='__main__':
    parser=OptionParser()
    parser.add_option("-t",dest='iFileType',type="string",default="",help="Type of input file (\'voice, sms etc\'")
    parser.add_option("-i",dest='iFile',type="string",default="",help="absolute path to input file")
    parser.add_option("-o",dest='oFile',type="string",default="",help="aboslute path to output file")
    parser.add_option("-m",dest='mode',type="string",default="I",help="Editing mode : R - Read, E - Edit, I - Interactive, Default: I")
    (options,args)=parser.parse_args()
    
    print options
    if options.iFile!="":    
        try:
            iFile=open(options.iFile,'r+')
        except IOError:
            print "Input file could not be read...exit(1)"
            sys.exit(1)
    else:
        print "Input file is necessary...exit(1)"
        sys.exit(1)
    
    if options.oFile!="" and options.oFile!=options.iFile:    
        try:
            ret=copyfile(options.iFile,options.oFile)
            oFile=open(options.oFile,'r+')
        except IOError:
            print "Unable to create/open an output file...exit(1)"
            sys.exit(1)
    else:
        oFile=iFile
    
    if options.iFileType=="":
        print "Input file type is required in order to correctly parse the input file...exit(1)"
        sys.exit(1)
    else:
        if not PF.MapRecType2File.has_key(options.iFileType):
            print "Input file type unspecified in configuration: unable to handler...exit(1)"
            sys.exit(1)
        else:
            iFileType=options.iFileType

    if options.mode=='I':
        if iFileType=="voice":
            fileStats,vr=PF.countRecordsVoice(iFileType,iFile)
            PF.printfileStats(fileStats,iFileType)
            while True:
                inp=raw_input("(action(R,E),record code,record number)$ ").split(',')
                if len(inp)<3:
                    print "! All three inputs mandatory"
                    continue
                Act,RC,RN=inp
                RN=int(RN)
                if Act not in ('E','R'):
                    print "! Unsupported Action"
                    continue
                if not fileStats.has_key(RC):
                    print "! Invalid record code"
                    continue
                if fileStats[RC][0]<RN:
                    print "! Record Number out of bounds"
                    continue
                PF.decodeEventRecord(iFileType,iFile,oFile,vr, fileStats,RC,int(RN),Act)

        