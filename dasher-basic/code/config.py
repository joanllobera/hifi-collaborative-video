#  RUMBA
#  Copyright (C) 2017  Fundacio i2CAT, Internet i Innovacio digital a Catalunya
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  Authors:  Joan Llobera <joan.llobera@i2cat.net>, David Gómez <david.gomez@i2cat.net>




#Ffmpeg Parameters
SegmentLength =""
VIDEOSAMPLINGRATE = ""
VIDEOCODEC = "libx264"


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


    
    
    