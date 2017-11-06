'''

@author: David Gomez david.gomez@i2cat.com simplified by Joan Llobera

'''



#Ffmpeg Parameters
SegmentLength =""
VIDEOSAMPLINGRATE = ""
VIDEOCODEC = "libx264"

#
def format_filename(filename):
    invalid_chars_list = '!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~ \t\n\r\x0b\x0c'
    invalid_chars = u"%s" % (invalid_chars_list)

    keyinvalidDict = {}

    for idx, chr_ in enumerate(invalid_chars):
        keyinvalidDict[chr_] = idx

    
    for k in filename:
        if k in keyinvalidDict.keys():
            filename = filename.replace(k,'_') # I don't like spaces in filenames.                
    return filename

def PrintConfig ():


    '''
    Print all internal variables for debug
    '''
    print("=================================================================")
    print(" PrintConfig ")
    print("=================================================================")
    print("-- Paths --") 
    print("InputhPath-> %s" % InputhPath) 
    print("PremierProjectName-> %s" % PremierProjectName) 
    #Paths fore share accros the program

    print("TempFolder-> %s" % TempFolder )
    

    #Ffmpeg Parameters
    print("-- Ffmpeg --") 

    print("SegmentLength-> %s" % SegmentLength)
    print("VIDEOSAMPLINGRATE-> %s" % VIDEOSAMPLINGRATE )
    print("VIDEOCODEC-> %s" % VIDEOCODEC )
     
    print("-- Media --") 
 
    print("tvList-> %s" % tvList)
    print("sphericalList-> %s" % sphericalList)
    print("portalList-> %s" % portalList)
    print("cubemapList-> %s" % cubemapList)

    print("tvBitRate-> %s" % tvBitRate)
    print("sphericalBitRate-> %s" % sphericalBitRate)
    print("portalBitRate-> %s" % portalBitRate)
    
    print("tvResolutions-> %s" % tvResolutions)
    print("sphericalResolutions-> %s" % sphericalResolutions)
    print("portalResolutions-> %s" % portalResolutions)


    
    
    