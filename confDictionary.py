
#===============================================================================
# 'I' - Integer, 'CA' - Character Array (Flags)
#===============================================================================
diameterHeader={"version":[1,0,'I'],\
            "messageLength":[3,1,'I'],\
            "commandFlags":[1,4,'CA'],\
            "commandCode":[3,5,'I'],\
            "applicationID":[4,8,'I'],\
            "hopByhopIdent":[4,12,'I'],\
            "End2EndIdent":[4,16,'I'],\
            }

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

