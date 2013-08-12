class diameterFlags:
    DIAMETER_FLAG_MANDATORY = 0x40
    DIAMETER_FLAG_VENDOR    = 0x80


diameterHeader={"version":[1,0,'uint32'],\
            "messageLength":[3,1,'uint32'],\
            "commandFlags":[1,4,'string'],\
            "commandCode":[3,5,'uint32'],\
            "applicationID":[4,8,'uint32'],\
            "hopByhopIdent":[4,12,'uint32'],\
            "End2EndIdent":[4,16,'uint32'],\
            }

CC2Conf={257:'AVP.Dict',914:'AVP.Dict'}


MapRecType2File={'voice':{1:'config/config.voice.moc',\
                     2:'config/config.voice.mtc',\
                     3:'config/config.voice.cfw',\
                     4:'config/config.voice.crs',\
                     8:'config/config.voice.smo',\
                     11:'config/config.voice.poc',\
                     12:'config/config.voice.ptc',\
                     24:'config/config.voice.coc',\
                     5:'config/config.voice.sup',\
                     0:'config/config.header.voice',\
                     10:'config/config.trailer.voice'},\
                 'header':{'voice':'config/header.voice',\
                           'sms':'/config/header.sms'},\
                 'trailer':{'voice':'config/header.voice',\
                            'sms':'config/header.sms'}\
                 }

