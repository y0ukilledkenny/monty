'''
Created on Jul 2, 2013

@author: SAMEERGU
'''
import decodeLib
import sys


diameterSt={"version":[1,0],\
            "messageLength":[3,1],\
            "commandFlags":[1,4],\
            "commandCode":[3,5],\
            "applicationID":[4,8],\
            "hopByhopIdent":[4,12],\
            "End2EndIdent":[4,16],\
            "AVP":[4,20]
            }

#command code to AVP conf mapper
CC2Conf={'257':'CER.Config'}

MapRecType2File={'voice':{1:'config.voice.moc',\
                     2:'config.voice.mtc',\
                     3:'config.voice.cfw',\
                     4:'config.voice.crs',\
                     8:'config.voice.smo',\
                     11:'config.voice.poc',\
                     12:'config.voice.ptc',\
                     24:'config.voice.coc',\
                     5:'config.voice.sup',\
                     0:'config.header.voice',\
                     10:'config.trailer.voice'},\
                 'header':{'voice':'header.voice',\
                           'sms':'header.sms'},\
                 'trailer':{'voice':'header.voice',\
                            'sms':'header.sms'}\
                 }

RecTypeDict={'voice':{'header':41,'offset':2,'length':1,'encoding':'1 BCD Byte'}}

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
    return cv



def populateConf(fileType,fileBuf):
    RecTypeConf=RecTypeDict[fileType]
    actualOffset=RecTypeConf['offset']+RecTypeConf['header']
    
    recType=decodeFMap[RecTypeConf['encoding']](fileBuf,RecTypeConf['length'],'U',actualOffset)
    try:
        return readConffromFile(MapRecType2File[fileType][recType[0]])
    except IOError:
        print "Configuration file could not be read...exit(1)"
        sys.exit(1)
    
    
    
    
    
def countRecords(iFileType,iFile):
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
    return fileStats,vr

def decodeDMfileInp(Data):
    CER={}
    for ATT in diameterSt:
        offset=2*diameterSt[ATT][1]
        length=2*diameterSt[ATT][0]
        print ATT,": ",Data[offset:offset+length]
        CER[ATT]=Data[offset:offset+length].decode("hex")
    return CER
    
    
    
    
def decodeEventRecord(iFileType,iFile,oFile, vr, fileStats,recNumber):
    DD=populateConf(iFileType,vr)
    for elm in DD:
        offset=int(fileStats['1'][recNumber])+int(elm['offset'])
        length=int(elm['length'])
        seq=decodeFMap[elm['encoding']](vr,length,'U',offset)
        pSeq=map(lambda x:'F' if x==15 else x,seq)
        print elm['FieldName'],": ","".join(map(str,pSeq))
        seq=list(raw_input('your value: '))
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