
#===============================================================================
# 'I' - Integer, 'CA' - Character Array (Flags)
#===============================================================================
diameterHeader={"version":[1,0,'uint32'],\
            "messageLength":[3,1,'uint32'],\
            "commandFlags":[1,4,'string'],\
            "commandCode":[3,5,'uint32'],\
            "applicationID":[4,8,'uint32'],\
            "hopByhopIdent":[4,12,'uint32'],\
            "End2EndIdent":[4,16,'uint32'],\
            }

CC2Conf={257:'CER.config'}


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

