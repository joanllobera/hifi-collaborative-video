
# Simple  Python Dasher

## How to run it:
Simply, type: 
> python Convert2DASH.py

To run it, you can use these content samples (put them in the input folder):
http://www.caminandes.com/download/01_llama_drama_2160p.zip
http://ftp.nluug.nl/pub/graphics/blender/demo/movies/ToS/tearsofsteel_4k.mov


## How to install it:

###In Windows
To install it manually on windows you will have to:

1. install python 2.7
2. install pip 
3. install pillow

The instruction is **pip install pillow** , and in the code it appears like **import pil**

4. install ffmpeg
https://www.ffmpeg.org/
this will require moving the downloaded folder into an apropriate location, such as c:\ffmpeg
and adding the following path in the PATH variable: C:\ffmpeg\bin

5. install gpac
https://gpac.wp.imt.fr/downloads/
Note there is a known issue with gpac: the installer has erased what was in my path variable, so it is wise to make a backup of the path variable before installing it.




### In a docker container

1. Take an image of Ubuntu
2. Use the .dockerfile included


##Known issues

Generating a DASH manifest with several qualities with gpac will make the resulting manifest to not be understood with the DASH-IF web player. In this case, instead of gpac it is recommendable to use the package bento4 https://www.bento4.com/

This is not a problem if you are using only one DASH quality.

