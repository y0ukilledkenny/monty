'''
Created on Jul 2, 2013

@author: SAMEERGU
'''
import decodeLib
import sys
import logging
from confDictionary import MapRecType2File,diameterHeader

decodeFMap=decodeLib.mapper()

def readConffromFile(confile):
    config=open(confile)
    header=config.readline()[:-1].split('\t')
    
    cv=[]
    row=config.readline()
    while row:
        val=row[:-1].split('\t')
        cv.append(dict(zip(header,val)))
        row=config.readline()
    config.close()
    return cv

def populateConf(fileType,RC,fileBuf):
    """
    Use FileStats and RC(record code) and RN(record number to determine the offset
    Encoding and length is hard coded to \'1 BCD Byte\' and 1
    """
    try:
        return readConffromFile(MapRecType2File[fileType][int(RC)])
    except IOError:
        print "Configuration file could not be read...exit(1)"
        sys.exit(1)
 
    
def countRecordsVoice(iFileType,iFile):
    iFile.seek(0)
    vr=iFile.read()
    recCount=0
    nextOffset=0
    fileStats={}
    while True:
        recType=decodeFMap['1 BCD Byte'](vr,1,'U',nextOffset+2)[0]
        if recType in [16,10]:
            break
        recordLength=decodeFMap['1 HEX Word'](vr,2,'U',nextOffset+0)[0]
        if recType!=1:
            recCount+=1
        if fileStats.has_key(str(recType)):
            fileStats[str(recType)][0]+=1
            fileStats[str(recType)].append(nextOffset)
        else:
            fileStats[str(recType)]=[1,nextOffset]
        nextOffset+=recordLength
    logging.debug("Record Count Statistics: %s\n"%fileStats.viewitems())
    return fileStats,vr

def printfileStats(fileStats,iFileType):
    print "File Type: ",iFileType
    print "%25s"%"Record Type"," : %s : %s"%("Record Code","Record Count")
    for foo in fileStats:
        if not MapRecType2File[iFileType].has_key(int(foo)):
            logging.debug("ERROR:: Sub Record Type not found in configuration: %s | Stats will not be printed"%foo)
            continue
        print "%25s"%MapRecType2File[iFileType][int(foo)].split('.',1)[1]," : %s : %s"%(foo,fileStats[foo][0])
    

def stripDHeader(Data):
    CER={}
    for ATT in diameterHeader:
        offset=diameterHeader[ATT][1]
        length=diameterHeader[ATT][0]
        CER[ATT]=[Data[offset:offset+length],diameterHeader[ATT][2]]
    Header=Data[:20]
    Data=Data[20:]
    return CER,Header,Data

def avpReadWrite(Data,Dlen,conFG,mode='R'):  
    if mode=='R':
        index=0
        while index!=Dlen:
            ATT=decodeFMap['DIAM'](Data[index:],4,'U','uint32')
            print("AVP: ",ATT,),
            vendorID=''
            if conFG.has_key(ATT):
                ATTName=conFG[ATT][1]
                print ATTName,
                flags=decodeFMap['DIAM'](Data[index+4:],1,'U','string')
                flags=bin(ord(flags))
                flags=(8-len(flags[2:]))*'0'+flags[2:]
                length=decodeFMap['DIAM'](Data[index+5:],3,'U','uint32')
                print "length: ",length,
                icr=0
                if flags[0]=='1':
                    vendorID=decodeFMap['DIAM'](Data[index+8:],4,'U','uint32')
                    print vendorID
                    icr=4
                VAL=decodeFMap['DIAM'](Data[index+8+icr:],length-8-icr,'U',conFG[ATT][0])
                print 'Value: ',VAL
            else:
                print "AVP Code :%d not found in configuration: unable to continue ..."%ATT
                exit(1)
            index+=(length+((4-length%4)%4))
    
    
    
def decodeEventRecord(iFileType,iFile,oFile, vr, fileStats,RC,RN,Act='R'):
    DD=populateConf(iFileType,RC,vr)
    for elm in DD:
        offset=int(fileStats[RC][RN])+int(elm['offset'])
        length=int(elm['length'])
        seq=decodeFMap[elm['encoding']](vr,length,'U',offset)
        pSeq=map(lambda x:'F' if x==15 else x,seq)
        print "%25s"%elm['FieldName']," : %s"%"".join(map(str,pSeq))
        
        if Act=='E':
            seq=list(raw_input("%25s"%'your value : '))
            if len(seq)!=0:
                pSeq=seq
            seq=map(lambda x:15 if x=='F' else int(x),pSeq)
            seq=decodeFMap[elm['encoding']](seq,len(seq),'P')
            oFile.seek(offset)
            for item in seq:
                oFile.write("%c"%item)
                

def decodeHeader():
    pass

def decodeTrailer():
    pass