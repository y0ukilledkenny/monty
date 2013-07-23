import struct

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

def _BcdByteReversed(vr,length,Act,offset=0):
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


                       
def mapper():
    return {'8 BCD Byte':_BcdByte,\
            '12 Hex Byte':_HexByte,\
            '1 Hex Byte':_HexByteR,\
            '5 BCD bytes + 1 BCD word':_VoiceStartTime,\
            '3 BCD Byte':_BcdByteReversed,\
            '1 HEX Word':_HexWord,\
            '10 HEX Byte':_HexByte,\
            '1 BCD Byte':_HexByteR}
    

def printVal(arr):
    print "".join(map(str,arr[:-1]))