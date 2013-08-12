import struct
import logging
import codecs
import time

#===============================================================================
# lot of lousy code, I KNOW, the struct library can be used a lot more 
# efficiently ... learning
#===============================================================================

def _BcdByte(vr,length,Act,offset=0):
    retString=[]
    if Act=='U':
        for x in range(length):
            v=struct.unpack('B',vr[offset+x])[0]
            retString.extend([v&15,v>>4])
        return retString
    elif Act=='P':
        for x in range(0,length,2):
            v=vr[offset+x] | (vr[offset+x+1] <<4 )
            retString.extend("%c"%v)
        return retString
    
def _HexByte(vr,length,Act,offset=0):
    retString=[]
    if Act=='U':
        for x in range(length):
            v=struct.unpack('B',vr[offset+x])[0]
            retString.extend([v&15,v>>4])
        return retString
    elif Act=='P':
        for x in range(0,length,2):
            v=vr[offset+x] | (vr[offset+x+1] <<4 )
            retString.extend("%c"%v)
        return retString

def _HexByteR(vr,length,Act,offset=0):
    retString=[]
    if Act=='U':
        for x in range(length):
            v=struct.unpack('B',vr[offset+x])[0]
            retString.extend([v])
        return retString
    elif Act=='P':
        for x in range(0,length,2):
            v=struct.pack('B',vr[offset+x])
            retString.extend([v])
        return retString


def _BcdWord(vr,length,Act,offset=0):
    retString=[]
    if Act=='U':
        for x in range(0,length,2):
            v1=struct.unpack('B',vr[offset+x])[0]
            v2=struct.unpack('B',vr[offset+x+1])[0]
            retString.extend([v2>>4,v2&15])
            retString.extend([v1>>4,v1&15])
    if Act=='P':
        for x in range(0,length,4):
            v1=vr[offset+x+1] | (vr[offset+x] <<4 )
            v2=vr[offset+x+3] | (vr[offset+x+2] <<4 )
            retString.extend("%c"%v2)
            retString.extend("%c"%v1)
    return retString

def _VoiceStartTime(vr,length,Act,offset=0):
    retString=[]
    if Act=='U':
        for x in range(5):
            v=struct.unpack('B',vr[offset+x])[0]
            retString.extend([v>>4,v&15])
        retString.extend(_BcdWord(vr,2,Act,offset+5))
    elif Act=='P':
        for x in range(0,5*2,2):
            v=vr[offset+x+1] | (vr[offset+x] <<4 )
            retString.extend("%c"%v)
        retString.extend(_BcdWord(vr,4,Act,5*2))
    return retString

#===============================================================================
# 3 BCD Byte : orig_mcz_duration    41    156    3    3 BCD Byte    string
# 1201    0112
#===============================================================================
def _BcdByteReversed(vr,length,Act,offset=0):
    """
    1201    0112
    """
    retString=[]
    if Act=='U':
        v=''
        for x in range(length):
            v+=struct.unpack('c',vr[offset+x])[0]
        for x in range(4-len(v)):
                v+=b'\x00'
        return [struct.unpack('i',v)[0]]
    elif Act=='P':
        v="%x"%vr[0]
        for x in range(6-len(v)):
            v='0'+v
        for x in range(0,6,2):
            v1=int(v[offset+x+1]) | (int(v[offset+x]) <<4 )
            retString.extend("%c"%v1) 
    return retString[::-1]

#===============================================================================
# calling_subs_first_lac    41    99    2    1 HEX Word    string
#===============================================================================
def _HexWord(vr,length,Act,offset=0):
    retString=[]
    if Act=='U':
        v=''
        for x in range(length):
            v+=struct.unpack('c',vr[offset+x])[0]
        for x in range(4-len(v)):
                v+=b'\x00'
        return [struct.unpack('i',v)[0]]
    elif Act=='P':
        v="%x"%vr[0]
        for x in range(4-len(v)):
            v='0'+v
        for x in range(0,4,2):
            v1=int(v[offset+x+1]) | (int(v[offset+x]) <<4 )
            retString.extend("%c"%v1)
    return retString[::-1]


    
def epoch2date(sec):
    t=time.localtime(sec)
    return t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec

def date2epoch(tYear,tMon,tDate,tHr,tMin,tSec):  
    t=time.strptime("{0} {1} {2} {3} {4} {5}".format(tYear,tMon,tDate,tHr,tMin,tSec),"%Y %m %d %H %M %S")
    return time.mktime(t) 

def _uint32cod(vr,length,Act,offset=0):
    logging.debug("DiamCoder - Before fixing length\n Act: %s, length: %s" %(Act,length))
    if Act=='U':
        for x in range((4-length%4)%4):
            vr=b'\x00'+vr
        return struct.unpack('!I',vr[offset:offset+4])[0]
    elif Act=='P':
        pass

def _uint64cod(vr,length,Act,offset=0):
    logging.debug("DiamCoder - Before fixing length\n Act: %s, length: %s" %(Act,length))
    if Act=='U':
        for x in range((8-length%8)%8):
            vr=b'\x00'+vr
        return struct.unpack('!Q',vr[offset:offset+8])[0]
    elif Act=='P':
        pass

def _stringcod(vr,length,Act,offset=0):
    if Act=='U':
        val=struct.unpack('!%ds'%length,vr[offset:length])[0]
        return val
    elif Act=='P':
        pass

def _utf8Stringcod(vr,length,Act,offset=0):
    pass

def _timecod(vr,length,Act,offset=0):
    """NTP time stamp format(fixed point decimal):
    actual length 64 bits. 32 bits are epoch time since 1900, remaining 32 bits are fractional seconds(discarded) """
    if Act=='U':
        epochT=_uint32cod(vr[0:],4,'U')
        date=epoch2date(epochT)
        return date
    
#===============================================================================
# def decode_Address(data):
#     if len(data)<=16:
#         data=data[4:12]
#         ret=inet_ntop(socket.AF_INET,data.decode("hex"))
#     else:
#         data=data[4:36]    
#         ret=inet_ntop(socket.AF_INET6,data.decode("hex"))
#     return ret
#===============================================================================

def _addresscod(vr,length,Act,offset=0):
        ADType=_uint32cod(vr[0:],2,'U')
        if ADType==2:
            pass
        elif ADType==1:
            val=[]
            for x in range(4):
                val.append(str(_uint32cod(vr[2+x:],1,'U')))
            return ".".join(val)            

def mapper():
    return {'8 BCD Byte':_BcdByte,\
            '12 Hex Byte':_HexByte,\
            '1 Hex Byte':_HexByteR,\
            '5 BCD bytes + 1 BCD word':_VoiceStartTime,\
            '3 BCD Byte':_BcdByteReversed,\
            '1 HEX Word':_HexWord,\
            '10 HEX Byte':_HexByte,\
            '1 BCD Byte':_HexByteR,\
            'uint32':_uint32cod,\
            'uint64':_uint64cod,\
            'string':_stringcod,\
            'time':_timecod,\
            'address':_addresscod
            }
    

def printVal(arr):
    print "".join(map(str,arr[:-1]))