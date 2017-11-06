'''
Created on 24 January 2017
Last update 06 November 2017

@author: David Gomez, modified by Joan Llobera
'''
import os
import platform
import shutil
import sys 

#import JsonToolBox
#import Logger
#import MPDSeed
#import MediaCheckpoint
#import MediaInfo
#import ConvertAudio
import ProgressConversion
#import XmlTooLBox
import config as Config
import PIL
from PIL import Image,ImageDraw,ImageOps
from distutils.command.config import config
#import Tiler

LevelProfile_264 = {'720p': '3.1', '1080p': '4', '2k': '4.2','4k': '5.1','8k': '6'}



def progress(count, total):
    bar_len = 30
    filled_len = int(round(bar_len * count / float(total)))
    #percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    print ('[%s] \r' % (bar)),
    #sys.stdout.write('[%s] %s%s -> %s\r' % (bar, percents, '%', status))
    #sys.stdout.flush()
    
def status_handler(old, new):
    print "Progress Video {0} %".format(old),
    progress(old, 100)
    

def convertVideo(inputPath, inputSource, outputSource, resolution, bitrate, segmentLength):



    '''
    Convert the video source according the input parameters
    '''

    
    
    
    
    
    resolution_size = [int(x) for x in resolution.split('x')]
    h264level = str(h264LevelProfile(resolution_size[0]))
#     logger = Logger.get_logger()
#     logger.info("ENCODING:VIDEO:%s"% inputSource) 
    print ("ENCODING:VIDEO:%s") % inputSource
     #=================================================================
    # FFmpeg parameters Configuration in Constant Rate Factor (CRF):
    #=================================================================
    if (platform.system() == "Windows"):
        base_cmd = 'ffmpeg -i %s\%s.mp4 -c copy -an -codec:v %s' % (inputPath, inputSource, Config.VIDEOCODEC)
    else:
        base_cmd = 'ffmpeg -i %s/%s.mp4 -c copy -an -codec:v %s' % (inputPath, inputSource, Config.VIDEOCODEC)
    
    
    
    if Config.VIDEOCODEC == 'libx264':
        base_cmd += ' -profile:v baseline -level ' + h264level + ' -map 0'
    segment = str(int(Config.VIDEOSAMPLINGRATE) * int(segmentLength)/1000)
    if (platform.system() == "Windows"):
        video_opts = "-force_key_frames expr:eq(mod(n,%s),0)" % segment
    else:
        video_opts = "-force_key_frames 'expr:eq(mod(n,%s),0)'" % segment
    #bufsize = (int(bitrate)*3 / int(Config.VIDEOSAMPLINGRATE))
    video_opts += " -bufsize %dk -maxrate %dk" % (int(bitrate), int(bitrate)*1.5)
    
    if Config.VIDEOCODEC == 'libx264':
        lookahead = str(int(Config.VIDEOSAMPLINGRATE) * int(segmentLength)/1000)
        video_opts += " -x264opts rc-lookahead=%s" % lookahead
    
    
    str_res = ("%sx%s") % (str(resolution_size[0]), str(resolution_size[1]))
    
    OUTPUT_NAME = inputSource+"_"+str_res + "_" + bitrate 
    output_target = "%s//%s" % (outputSource,OUTPUT_NAME)
    

    print("")
    print("We now convert to .mp4 with  an ffmpeg command: ")
    cmd = base_cmd+' '+video_opts + ' -r 25 -s '+str(resolution_size[0])+'x'+str(resolution_size[1])+  ' -f mp4 '+ output_target + ".mp4"
    print(cmd)
    
    converter = ProgressConversion.ProgressConversion()
    converter.run_session(cmd, status_handler=status_handler)
    print("Progress Video 100")
    return OUTPUT_NAME




def h264LevelProfile (width):
    print("The level profile:")
    if 1 <= width <= 1919:
        print ("is 720p or Sd")
        return LevelProfile_264['720p']
    if 1920 <= width <= 2047:
        print ("is 1080p")
        return LevelProfile_264['1080p']
    if 2048 <= width <= 3839:
        print ("is 2K")
        return LevelProfile_264['2k']
    if 3840 <= width <= 4095:
        print ("is 4K")
        return LevelProfile_264['4k']
    if 4096 <= width <= 8192:
        print ("is 8K")
        return LevelProfile_264['8k']


        
def dashVideo(segmentLength,inputPath, inputName, outputPath):
        
        MP4boxcall = "MP4Box -dash "+segmentLength + " -profile live -out " + outputPath +"//"+ inputName +".mpd " + inputPath +"//"+ inputName + ".mp4"

        print("")
        print("We now convert to .mp4 with  an ffmpeg command: ")
        print(MP4boxcall)
        os.system(MP4boxcall)
        
        
        
        
class Dasher:
   if __name__ == '__main__':
   
   
        inputPath = "C://dasher-basic//input"
        inputSource = "01_llama_drama_4096p"
        outputTemp = "C://dasher-basic//output//temp"
        outputDashed = "C://dasher-basic//output//dash"
        Config.VIDEOCODEC = 'libx264'
        segmentLength = "1000"  #in ms
        resolution="426x240"
        bitrate = "300";
        Config.VIDEOSAMPLINGRATE = "25"
   
   
        output_name = convertVideo(inputPath, inputSource, outputTemp, resolution, bitrate, segmentLength)
        dashVideo(segmentLength, outputTemp, output_name, outputDashed)




