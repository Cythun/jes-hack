#ORIGINAL COMMENT from JES media.py BELOW
#
# Media Wrappers for "Introduction to Media Computation"
# Started: Mark Guzdial, 2 July 2002
# Revisions:
# 18 June 2003: (ellie)
#    Added (blocking)play(AtRate)InRange methods to Sound class
#      and global sound functions
#    Changed getSampleValue, setSampleValue to give the appearance
#      of 1-based indexing
#    Added getLeftSampleValue and getRightSampleValue to Sound class
# 14 May 2003: Fixed discrepancy between getMediaPath and setMediaFolder (AdamW)
# 8 Nov: Fixed getSamplingRate (MarkG)
# 1 Nov: Fixed printing pixel
# 31 Oct: Fixed pickAColor (MarkG)
# 30 Oct: Added raises, fixed error messages. Added repaint (MarkG)
# 10 Oct: Coerced value to integer in Sound.setSampleValue   (MarkR)
# 2 Oct:  Corrected calls in setSampleValueAt  (MarkG):
# 30 Aug: Made commands more consistent and add type-checking (MarkG)
# 2 Aug: Changed to getSampleValueAt and setSampleValueAt (MarkG)
# 1 Dec 2005: made max makeEmptySound size 600
#             made max makeEmptyPicture dimensions 10000x10000
#             fixed the off-by-one error in makeEmptyPicture
# 14 June 2007: (Pam Cutter, Kalamazoo College)
#              Fixed off-by-one error in copyInto.  Now allows copying
#		of same-sized picture, starting at top-left corner
#
# 6 July 2007: (Pam Cutter/Alyce Brady, Kalamazoo College)
#              Added flexibility to make an empty picture of a specified color.  Added
#                  additional, 3-parameter constructor to Picture and SimplePicture classes to support this.
#              Modified copyInto so that it will copy as much of the source picture as will fit
#              Added crop and copyInto methods to Picture class to support these.
#
# 8 July 2007: (Pam Cutter/ Alyce Brady, Kalamazoo College)
#              Changed all  _class_ comparisons to use isinstance instead so that
#                   they will work with subclasses as well (e.g., subclasses of Picture
#                   are still pictures)
#              Added getSampleValue, setSampleValue functions with same functionality, but
#                   more intuitive names, as the getSample, setSample function, respectively.
#              Added global getDuration function to return the number of seconds in a sound
#
# 10 July 2007: (Pam Cutter, Kalamazoo College)
#              Added a global duplicateSound function
# 11 July 2007: (Pam Cutter, Kalamazoo College)
#              Added global addTextWithStyle function to allow users to add text to images
#                  with different font styles.
#
# 17 July 2007: (Pam Cutter, Kalamazoo College)
#              Added global addOval, addOvalFilled, addArc and addArcFilled functions.
#              Added global getNumSamples function as more meaningful name for getLength of a sound.
#
# 19 July 2007: (Pam Cutter, Kalamazoo College)
#              Modified the SoundExplorer class to be consistent with sounds in JES
#                  starting at sample index 1.
#              Modified the PictueExplorer class to initially show color values from
#			 pixel 1,1, instead of 0,0.
#
# 1 Nov 2007: Added __add__ and __sub__ to Color class (BrianO)
# 29 Apr 2008: Changed makeEmptySound to take an integer number of samples
#	       Added optional second argument to makeEmptySound for sampleRate
# 6 June 2008: Added a check for forward slash in a directory path in makeMovieFromInitialFile
#		This check should work with os.altsep, but it does not work with Jython 2.2.
#		This should be fixed again at a later date.
# 27 June 2008: Added optional input to setMediaFolder and setMediaPath.
#		Added showMediaFolder and showMediaPath methods.
# 11 July 2007: Removed showMediaFolder and showMediaPath for no-arg version of getMediaPath/getMediaFolder.
#		Added generic explore method. 
# 15 July 2007: Added no-arg option for setLibPath

# TODO:
## Fix HSV/RGB conversions -- getting a divide by zero error when max=min

import sys
import os
import math
import traceback
import user
import Picture
import Pixel

#import org.python.core.PyString as String

# Support a media shortcut

#mediaFolder = JESConfig.getMediaPath()
#if ( mediaFolder == "" ):
mediaFolder = os.getcwd() + os.sep
    
# Store last pickAFile() opening

_lastFilePath = ""

true = 1
false = 0

def setMediaPath(file=None):
    global mediaFolder
    #if(file == None):
    #    FileChooser.pickMediaPath()
    #else:	
    #    FileChooser.setMediaPath( file )
    #mediaFolder = getMediaPath()
    #return mediaFolder
    #TODO

def getMediaPath( filename = "" ):
    #return FileChooser.getMediaPath( filename )
    pass #TODO

#Done
def setMediaFolder(file=None):
    return setMediaPath(file)

#Done
def setTestMediaFolder():
    global mediaFolder
    mediaFolder = os.getcwd() + os.sep

#Done
def getMediaFolder( filename = "" ):
    return getMediaPath(filename)

#Done
def showMediaFolder():
    global mediaFolder
    print "The media path is currently: ",mediaFolder

#Done
def getShortPath(filename):
    dirs = filename.split(os.sep)
    if len(dirs) < 1:
        return "."
    elif len(dirs) == 1:
        return dirs[0]
    else:
        return (dirs[len(dirs) - 2] + os.sep + dirs[len(dirs) - 1])

#Done
def setLibPath(directory=None):
    if(directory == None):
        directory = pickAFolder()
    if(os.path.isdir(directory)):
    	sys.path.append(directory)
    else:
        print "Note: There is no directory at ",directory
        raise ValueError
    return directory
    
##
## Global sound functions
##
def makeSound(filename):
    global mediaFolder
    if not os.path.isabs(filename):
        filename = mediaFolder + filename
    if not os.path.isfile(filename):
        print "There is no file at "+filename
        raise ValueError
    #return Sound(filename)
    #TODO

# MMO (1 Dec 2005): capped size of sound to 600
# Brian O (29 Apr 2008): changed first argument to be number of samples, added optional 2nd argument of sampling rate
def makeEmptySound(numSamples, samplingRate = Sound.SAMPLE_RATE):
    if numSamples <= 0 or samplingRate <= 0:
        print "makeEmptySound(numSamples[, samplingRate]): numSamples and samplingRate must each be greater than 0"
        raise ValueError
    if (numSamples/samplingRate) > 600:
        print "makeEmptySound(numSamples[, samplingRate]): Created sound must be less than 600 seconds"
        raise ValueError
    #return Sound(numSamples, samplingRate)
    #TODO
#    if size > 600:
#        print "makeEmptySound(size): size must be 600 seconds or less"
#        raise ValueError
#    return Sound(size * Sound.SAMPLE_RATE)

# Brian O (5 May 2008): Added method for creating sound by duration
def makeEmptySoundBySeconds(seconds, samplingRate = Sound.SAMPLE_RATE):
    if seconds <= 0 or samplingRate <= 0:
        print "makeEmptySoundBySeconds(numSamples[, samplingRate]): numSamples and samplingRate must each be greater than 0"
        raise ValueError
    if seconds > 600:
        print "makeEmptySoundBySeconds(numSamples[, samplingRate]): Created sound must be less than 600 seconds"
        raise ValueError
    #return Sound(seconds * samplingRate, samplingRate)
    #TODO

# PamC: Added this function to duplicate a sound
def duplicateSound(sound):
  if not isinstance(sound, Sound):
        print "duplicateSound(sound): Input is not a sound"
        raise ValueError
  #return Sound(sound)
  #TODO

def getSamples(sound):
    if not isinstance(sound, Sound):
        print "getSamples(sound): Input is not a sound"
        raise ValueError
#    return Samples(sound)
    #return Samples.getSamples(sound)
    #TODO

def play(sound):
    #if not isinstance(sound,Sound):
    #    print "play(sound): Input is not a sound"
    #    raise ValueError
    #sound.play()
    pass #TODO

def blockingPlay(sound):
    #if not isinstance(sound,Sound):
    #    print "blockingPlay(sound): Input is not a sound"
    #    raise ValueError
    #sound.blockingPlay()
    pass #TODO

# Buck Scharfnorth (27 May 2008): Added method for stopping play of a sound
def stopPlaying(sound):
    #if not isinstance(sound,Sound):
    #    print "stopPlaying(sound): Input is not a sound"
    #    raise ValueError
    #sound.stopPlaying()
    pass #TODO

def playAtRate(sound,rate):
    #if not isinstance(sound, Sound):
    #    print "playAtRate(sound,rate): First input is not a sound"
    #    raise ValueError
    ## sound.playAtRate(rate)
    #sound.playAtRateDur(rate,sound.getLength())
    pass #TODO

def playAtRateDur(sound,rate,dur):
    #if not isinstance(sound,Sound):
    #    print "playAtRateDur(sound,rate,dur): First input is not a sound"
    #    raise ValueError
    #sound.playAtRateDur(rate,dur)
    pass #TODO

#20June03 new functionality in JavaSound (ellie)
def playInRange(sound,start,stop):
        #if not isinstance(sound, Sound):
        #        print "playInRange(sound,start,stop): First input is not a sound"
        #        raise ValueError
        ## sound.playInRange(start,stop)
        #sound.playAtRateInRange(1,start-Sound._SoundIndexOffset,stop-Sound._SoundIndexOffset)
        pass #TODO

#20June03 new functionality in JavaSound (ellie)
def blockingPlayInRange(sound,start,stop):
        #if not isinstance(sound, Sound):
        #        print "blockingPlayInRange(sound,start,stop): First input is not a sound"
        #        raise ValueError
        ## sound.blockingPlayInRange(start,stop)
        #sound.blockingPlayAtRateInRange(1,start-Sound._SoundIndexOffset,stop-Sound._SoundIndexOffset)
        pass #TODO

#20June03 new functionality in JavaSound (ellie)
def playAtRateInRange(sound,rate,start,stop):
        #if not isinstance(sound,Sound):
        #        print "playAtRateInRAnge(sound,rate,start,stop): First input is not a sound"
        #        raise ValueError
        #sound.playAtRateInRange(rate,start - Sound._SoundIndexOffset,stop - Sound._SoundIndexOffset)
        pass #TODO

#20June03 new functionality in JavaSound (ellie)
def blockingPlayAtRateInRange(sound,rate,start,stop):
        #if not isinstance(sound, Sound):
        #        print "blockingPlayAtRateInRange(sound,rate,start,stop): First input is not a sound"
        #        raise ValueError
        #sound.blockingPlayAtRateInRange(rate, start - Sound._SoundIndexOffset,stop - Sound._SoundIndexOffset)
        pass #TODO

def getSamplingRate(sound):
    #if not isinstance(sound, Sound):
    #    print "getSamplingRate(sound): Input is not a sound"
    #    raise ValueError
    #return sound.getSamplingRate()
    pass #TODO

def setSampleValueAt(sound,index,value):
    #if not isinstance(sound, Sound):
    #    print "setSampleValueAt(sound,index,value): First input is not a sound"
    #    raise ValueError
    #if index < Sound._SoundIndexOffset:
    #    print "You asked for the sample at index: " + str( index ) + ".  This number is less than " + str(Sound._SoundIndexOffset) + ".  Please try" + " again using an index in the range [" + str(Sound._SoundIndexOffset) + "," + str ( getLength( sound ) - 1 + Sound._SoundIndexOffset ) + "]."
    #    raise ValueError
    #if index > getLength(sound) - 1 + Sound._SoundIndexOffset:
    #    print "You are trying to access the sample at index: " + str( index ) + ", but the last valid index is at " + str( getLength( sound ) - 1 + Sound._SoundIndexOffset )
    #    raise ValueError
    #sound.setSampleValue(index-Sound._SoundIndexOffset,int(value))
    pass #TODO

def getSampleValueAt(sound,index):
    #if not isinstance(sound,Sound):
    #    print "getSampleValueAt(sound,index): First input is not a sound"
    #    raise ValueError
    #if index < Sound._SoundIndexOffset:
    #    print "You asked for the sample at index: " + str( index ) + ".  This number is less than " + str(Sound._SoundIndexOffset) + ".  Please try" + " again using an index in the range [" + str(Sound._SoundIndexOffset) + "," + str ( getLength( sound ) - 1 + Sound._SoundIndexOffset ) + "]."
    #    raise ValueError
    #if index > getLength(sound) - 1 + Sound._SoundIndexOffset:
    #    print "You are trying to access the sample at index: " + str( index ) + ", but the last valid index is at " + str( getLength( sound ) - 1 + Sound._SoundIndexOffset )
    #    raise ValueError
    #return sound.getSampleValue(index-Sound._SoundIndexOffset)
    pass #TODO

def getSampleObjectAt(sound,index):
    #if not isinstance(sound, Sound):
    #    print "getSampleObjectAt(sound,index): First input is not a sound"
    #    raise ValueError
    # return sound.getSampleObjectAt(index-Sound._SoundIndexOffset)
    #if index < Sound._SoundIndexOffset:
    #    print "You asked for the sample at index: " + str( index ) + ".  This number is less than " + str(Sound._SoundIndexOffset) + ".  Please try" + " again using an index in the range [" + str(Sound._SoundIndexOffset) + "," + str ( getLength( sound ) - 1 + Sound._SoundIndexOffset ) + "]."
    #    raise ValueError
    #if index > getLength(sound) - 1 + Sound._SoundIndexOffset:
    #    print "You are trying to access the sample at index: " + str( index ) + ", but the last valid index is at " + str( getLength( sound ) - 1 + Sound._SoundIndexOffset )
    #    raise ValueError
    #return Sample(sound, index-Sound._SoundIndexOffset)
    pass #TODO

def setSample(sample,value):
    #if not isinstance(sample,Sample):
    #    print "setSample(sample,value): First input is not a sample"
    #    raise ValueError
    #if value > 32767:
    #    value = 32767
    #elif value < -32768:
    #    value = -32768
    ## Need to coerce value to integer
    #return sample.setValue( int(value) )
    pass #TODO

# PamC: Added this function to be a better name than setSample
#Done
def setSampleValue(sample, value):
  setSample(sample, value)

def getSample(sample):
    #if not isinstance(sample, Sample):
    #    print "getSample(sample): Input is not a sample"
    #    raise ValueError
    #return sample.getValue()
    #TODO

# PamC: Added this to be a better name for getSample
#Done
def getSampleValue(sample):
  return getSample(sample)

def getSound(sample):
    #if not isinstance(sample,Sample):
    #    print "getSound(sample): Input is not a sample"
    #    raise ValueError
    #return sample.getSound()
    pass #TODO

def getLength(sound):
    #if not isinstance(sound, Sound):
    #    print "getLength(sound): Input is not a sound"
    #    raise ValueError
    #return sound.getLength()
    pass #TODO

# PamC: Added this function as a more meaningful name for getLength
#Done
def getNumSamples(sound):
    return getLength(sound)

# PamC: Added this function to return the number of seconds
# in a sound
def getDuration(sound):
  #if not isinstance(sound, Sound):
  #  print "getDuration(sound): Input is not a sound"
  #  raise ValueError
  #return sound.getLength()/sound.getSamplingRate()
  pass #TODO

def writeSoundTo(sound,filename):
    #global mediaFolder
    #if not os.path.isabs(filename):
    #    filename = mediaFolder + filename
    #if not isinstance(sound, Sound):
    #    print "writeSoundTo(sound,filename): First input is not a sound"
    #    raise ValueError
    #sound.writeToFile(filename)
    pass #TODO

##
# Globals for styled text
##
def makeStyle(fontName,emph,size):
    #return awt.Font(fontName,emph,size)
    pass #TODO

sansSerif = "SansSerif"
serif = "Serif"
mono = "Monospaced"
#italic = awt.Font.ITALIC TODO
#bold = awt.Font.BOLD TODO
#plain = awt.Font.PLAIN TODO

##
## Global color functions
##

# Buck Scharfnorth (28 May 2008): if bool == 1 colors will be (value % 256)
# 				  if bool == 0 colors will be truncated to 0 or 255
# updated (13 May 2009): 
# THIS GLOBAL FUNCTION CHANGES JES SETTINGS - this value overwrites
# the value in the JES options menu.
def setColorWrapAround(bool):
    #JESConfig.getInstance().setSessionWrapAround( bool )
    pass #TODO

# Buck Scharfnorth (28 May 2008): Gets the current ColorWrapAround Value
def getColorWrapAround():
    #return JESConfig.getInstance().getSessionWrapAround()
    pass #TODO

# Buck Scharfnorth (28 May 2008): Modified to no longer assume the value is 0-255
#Done
def _checkPixel(raw):
    value = int(raw)
    if getColorWrapAround():
        value = (value % 256)
    else:
        if value < 0:
            value = 0
        if value > 255:
            value = 255
    return value

# this class is solely for the purpose of
# making makeLighter makeDarker work.
# both of these functions destructively modify a color
# and a color in java is a constant value so we have to put
# this python interface here
#
# Buck Scharfnorth (28 May 2008): Modified to no longer assume the value is 0-255
# and the gray Color constructor to allow only 1 color parameter (will take 2, but ignores the second)
class Color:
    #TODO mess with this
    def __init__(self,r,g=None,b=None):
        if b == None:
            #if isinstance( r, awt.Color ) or isinstance( r, Color ):
            #    self.color = r
            #else:
            #    val = _checkPixel(r)
            #    self.color = awt.Color( val, val, val )
        else:
            # self.color = awt.Color(r,g,b)
            #self.color = awt.Color( _checkPixel(r), _checkPixel(g), _checkPixel(b) )
            #TODO

    def __str__(self):
        return "color r="+str(self.getRed())+" g="+str(self.getGreen())+" b="+str(self.getBlue())

    def __repr__(self):
        return "Color("+str(self.getRed())+", "+str(self.getGreen())+", "+str(self.getBlue())+")"

    def __eq__(self,newcolor):
        return ((self.getRed() == newcolor.getRed()) and (self.getGreen() == newcolor.getGreen()) and (self.getBlue() == newcolor.getBlue()))

    def __ne__(self,newcolor):
        return (not self.__eq__(newcolor))

    #def __tojava__(self, javaclass):
    #    if javaclass == awt.Color:
    #        return self.color
    #    else:
    #        return self

    #Added by BrianO
    def __add__(self, other):
        r = self.getRed() + other.getRed()
        g = self.getGreen() + other.getGreen()
        b = self.getBlue() + other.getBlue()

	# if(wrapAroundPixelValues):
	#    r = r % 256
	#    g = g % 256
	#    b = b % 256

	# return Color(r,g,b)
        return Color( _checkPixel(r), _checkPixel(g), _checkPixel(b) )

    #Added by BrianO
    def __sub__(self, other):
        r = self.getRed() - other.getRed()
        g = self.getGreen() - other.getGreen()
        b = self.getBlue() - other.getBlue()

	# if(wrapAroundPixelValues):
	#    r = r % 256
	#    g = g % 256
	#    b = b % 256

	# return Color(r,g,b)
        return Color( _checkPixel(r), _checkPixel(g), _checkPixel(b) )

    def setRGB(self, r, g, b):
    #    # self.color = awt.Color(r,g,b)
    #    self.color = awt.Color(_checkPixel(r), _checkPixel(g), _checkPixel(b))
        pass #TODO
    

    def getRed(self):
        return self.color.getRed()

    def getGreen(self):
        return self.color.getGreen()

    def getBlue(self):
        return self.color.getBlue()

    def distance(self, othercolor):
        r = pow((self.getRed() - othercolor.getRed()),2)
        g = pow((self.getGreen() - othercolor.getGreen()),2)
        b = pow((self.getBlue() - othercolor.getBlue()) ,2)
        return math.sqrt(r+g+b)

    def makeDarker(self):
      return self.color.darker()

    def makeLighter(self):
      return self.color.brighter()

def pickAColor():
    ## Dorn 5/8/2009:  Edited to be thread safe since this code is executed from an
    ## interpreter JESThread and will result in an update to the main JES GUI due to 
    ## it being a modal dialog.
    #from java.lang import Runnable

    #class pickAColorRunner(Runnable):
	#color = Color(0,0,0)
	#def run(self):
	#    retValue = swing.JColorChooser().showDialog(swing.JFrame(),"Choose a color", awt.Color(0,0,0))
	#    if retValue != None:
	#        self.color = Color(retValue.getRed(),retValue.getGreen(),retValue.getBlue())

    #runner = pickAColorRunner()
    #swing.SwingUtilities.invokeAndWait(runner)
    
    #return runner.color
    pass #TODO



#Constants
black = Color(0,0,0)
white = Color(255,255,255)
blue = Color(0,0,255)
red = Color(255,0,0)
green = Color(0,255,0)
gray = Color(128,128,128)
darkGray = Color(64,64,64)
lightGray = Color(192,192,192)
yellow = Color(255,255,0)
orange = Color(255,200,0)
pink = Color(255,175,175)
magenta = Color(255,0,255)
cyan = Color(0,255,255)

##
## Global picture functions
##
def makePicture(filename):
    global mediaFolder
    if not os.path.isabs(filename):
        filename = mediaFolder + filename
    if not os.path.isfile(filename):
        print "makePicture(filename): There is no file at "+filename
        raise ValueError
    #picture = Picture()
    #picture.loadOrFail(filename)
    #return picture
    #TODO

# MMO (1 Dec 2005): Capped width/height to max 10000 and min 1
# alexr (6 Sep 2006): fixed to work without the Python classes.
# PamC (6 July 2007): added new optional param to allow for empty pictures
# with different background colors.
def makeEmptyPicture(width, height, acolor = white):
    if width > 10000 or height > 10000:
        print "makeEmptyPicture(width, height[, acolor]): height and width must be less than 10000 each"
        raise ValueError
    if width <= 0 or height <= 0:
        print "makeEmptyPicture(width, height[, acolor]): height and width must be greater than 0 each"
        raise ValueError
    #picture = Picture(width, height, acolor) TODO
    # picture.createImage(width, height)
    # picture.filename = ''
    # careful here; do we want empty strings or "None"?
    return picture

def getPixels(picture):
    #if not isinstance(picture, Picture):
    #    print "getPixels(picture): Input is not a picture"
    #    raise ValueError
    #return picture.getPixels()
    #TODO

#Done
def getAllPixels(picture):
    return getPixels(picture)

def getWidth(picture):
    #if not isinstance(picture, Picture):
    #    print "getWidth(picture): Input is not a picture"
    #    raise ValueError
    #return picture.getWidth()
    pass #TODO

def getHeight(picture):
    #if not isinstance(picture,Picture):
    #    print "getHeight(picture): Input is not a picture"
    #    raise ValueError
    #return picture.getHeight()
    pass #TODO

def show(picture, title=None):
    ##picture.setTitle(getShortPath(picture.filename))
    ##if title <> None:
    #        #picture.setTitle(title)
    #if not isinstance(picture, Picture):
    #    print "show(picture): Input is not a picture"
    #    raise ValueError
    #picture.show()
    pass #TODO

def repaint(picture):
    #if not (isinstance(picture, World) or isinstance(picture,Picture)):
    #    print "repaint(picture): Input is not a picture or a world"
    #    raise ValueError
    #picture.repaint()
    pass #TODO

## adding graphics to your pictures! ##
def addLine(picture, x1, y1, x2, y2, acolor=black):
    #if not isinstance(picture, Picture):
    #    print "addLine(picture, x1, y1, x2, y2[, color]): First input is not a picture"
    #    raise ValueError
    #if not isinstance(acolor, Color):
    #    print "addLine(picture, x1, y1, x2, y2[, color]): Last input is not a color"
    #    raise ValueError
    ##g = picture.getBufferedImage().createGraphics()
    ##g.setColor(acolor.color)
    ##g.drawLine(x1 - 1,y1 - 1,x2 - 1,y2 - 1)
    #picture.addLine(acolor,x1,y1,x2,y2)
    pass #TODO

def addText(picture, x, y, string, acolor=black):
    #if not isinstance(picture, Picture):
    #    print "addText(picture, x, y, string[, color]): First input is not a picture"
    #    raise ValueError
    #if not isinstance(acolor, Color):
    #    print "addText(picture, x, y, string[, color]): Last input is not a color"
    #    raise ValueError
    ##g = picture.getBufferedImage().getGraphics()
    ##g.setColor(acolor.color)
    ##g.drawString(string, x - 1, y - 1)
    #picture.addText(acolor,x,y,string)
    pass #TODO

# PamC: Added this function to allow different font styles
def addTextWithStyle(picture, x, y, string, style, acolor=black):
    #if not isinstance(picture, Picture):
    #    print "addTextWithStyle(picture, x, y, string, style[, color]): First input is not a picture"
    #    raise ValueError
    #if not isinstance(style, awt.Font):
    #    print "addTextWithStyle(picture, x, y, string, style[, color]): Input is not a style (see makeStyle)"
    #    raise ValueError
    #if not isinstance(acolor, Color):
    #    print "addTextWithStyle(picture, x, y, string, style[, color]): Last input is not a color"
    #    raise ValueError
    #picture.addTextWithStyle(acolor,x,y,string,style)
    pass #TODO

def addRect(picture, x,y,w,h, acolor=black):
    #if not isinstance(picture, Picture):
    #    print "addRect(picture, x, y, w, h[, color]): First input is not a picture"
    #    raise ValueError
    #if not isinstance(acolor, Color):
    #    print "addRect(picture, x, y, w, h[, color]): Last input is not a color"
    #    raise ValueError
    ##g = picture.getBufferedImage().getGraphics()
    ##g.setColor(acolor.color)
    ##g.drawRect(x - 1,y - 1,w,h)
    #picture.addRect(acolor,x,y,w,h)
    pass #TODO

def addRectFilled(picture,x,y,w,h, acolor=black):
    #if not isinstance(picture,Picture):
    #    print "addRectFilled(picture, x, y, w, h[, color]): First input is not a picture"
    #    raise ValueError
    #if not isinstance(acolor, Color):
    #    print "addRectFilled(picture, x, y, w, h[, color]): Last input is not a color"
    #    raise ValueError
    ##g = picture.getBufferedImage().getGraphics()
    ##g.setColor(acolor.color)
    ##g.fillRect(x - 1,y - 1,w,h)
    #picture.addRectFilled(acolor,x,y,w,h)
    pass #TODO

# PamC: Added the following addOval, addOvalFilled, addArc, and addArcFilled
# functions to add more graphics to pictures.
def addOval(picture, x,y,w,h, acolor=black):
    #if not isinstance(picture, Picture):
    #    print "addOval(picture, x, y, w, h[, color]): First input is not a picture"
    #    raise ValueError
    #if not isinstance(acolor, Color):
    #    print "addOval(picture, x, y, w, h[, color]): Last input is not a color"
    #    raise ValueError
    ##g = picture.getBufferedImage().getGraphics()
    ##g.setColor(acolor.color)
    ##g.drawRect(x - 1,y - 1,w,h)
    #picture.addOval(acolor,x,y,w,h)
    pass #TODO

def addOvalFilled(picture,x,y,w,h,acolor=black):
    #if not isinstance(picture,Picture):
    #    print "addOvalFilled(picture, x, y, w, h[, color]): First input is not a picture"
    #    raise ValueError
    #if not isinstance(acolor, Color):
    #    print "addOvalFilled(picture, x, y, w, h[, color]): Last input is not a color"
    #    raise ValueError
    #picture.addOvalFilled(acolor,x,y,w,h)
    pass #TODO

def addArc(picture,x,y,w,h,start,angle,acolor=black):
    #if not isinstance(picture,Picture):
    #    print "addArc(picture, x, y, w, h, start, angle[, color]): First input is not a picture"
    #    raise ValueError
    #if not isinstance(acolor, Color):
    #    print "addArc(picture, x, y, w, h[, color]): Last input is not a color"
    #    raise ValueError
    #picture.addArc(acolor,x,y,w,h,start,angle)
    pass #TODO

def addArcFilled(picture,x,y,w,h,start,angle,acolor=black):
    #if not isinstance(picture,Picture):
    #    print "addArcFilled(picture, x, y, w, h[, color]): First First input is not a picture"
    #    raise ValueError
    #if not isinstance(acolor, Color):
    #    print "addArcFill(picture, x, y, w, h[, color]): Last input is not a color"
    #    raise ValueError
    #picture.addArcFilled(acolor,x,y,w,h,start,angle)
    pass #TODO

## note the -1; in JES we think of pictures as starting at (1,1) but not
## in the Java.
##
## 29 Oct 2008: -1 changed to Picture._PictureIndexOffset
def getPixel(picture,x,y):
    #if not isinstance(picture, Picture):
    #    print "getPixel(picture,x,y): First input is not a picture"
    #    raise ValueError
    #if ( x < Picture._PictureIndexOffset ) or ( x > getWidth(picture) - 1 + Picture._PictureIndexOffset ):
    #    print "getPixel(picture,x,y): x (= %s) is less than %s or bigger than the width (= %s)" % (x,Picture._PictureIndexOffset,getWidth(picture) - 1 + Picture._PictureIndexOffset)
    #    raise ValueError
    #if ( y < Picture._PictureIndexOffset ) or ( y > getHeight(picture) - 1 + Picture._PictureIndexOffset ):
    #    print "getPixel(picture,x,y): y (= %s) is less than %s or bigger than the height (= %s)" % (y,Picture._PictureIndexOffset,getHeight(picture) - 1 + Picture._PictureIndexOffset)
    #    raise ValueError

    #return picture.getPixel(x - Picture._PictureIndexOffset, y - Picture._PictureIndexOffset)
    pass #TODO

#Added as a better name for getPixel
#Done
def getPixelAt(picture,x,y):
    return getPixel(picture,x,y)

def setRed(pixel,value):
    #value = _checkPixel(value)
    #if not isinstance(pixel, Pixel):
    #    print "setRed(pixel,value): Input is not a pixel"
    #    raise ValueError
    #pixel.setRed(value)
    pass #TODO

def getRed(pixel):
    #if not isinstance(pixel, Pixel):
    #    print "getRed(pixel): Input is not a pixel"
    #    raise ValueError
    #return pixel.getRed()
    pass #TODO

def setBlue(pixel,value):
    #value = _checkPixel(value)
    #if not isinstance(pixel, Pixel):
    #    print "setBlue(pixel,value): Input is not a pixel"
    #    raise ValueError
    #pixel.setBlue(value)
    pass #TODO

def getBlue(pixel):
    #if not isinstance(pixel,Pixel):
    #    print "getBlue(pixel): Input is not a pixel"
    #    raise ValueError
    #return pixel.getBlue()
    pass #TODO

def setGreen(pixel,value):
    #value = _checkPixel(value)
    #if not isinstance(pixel, Pixel):
    #    print "setGreen(pixel,value): Input is not a pixel"
    #    raise ValueError
    #pixel.setGreen(value)
    pass #TODO

def getGreen(pixel):
    #if not isinstance(pixel, Pixel):
    #    print "getGreen(pixel): Input is not a pixel"
    #    raise ValueError
    #return pixel.getGreen()
    pass #TODO

def getColor(pixel):
    #if not isinstance(pixel, Pixel):
    #    print "getColor(pixel): Input is not a pixel"
    #    raise ValueError
    #return Color(pixel.getColor())
    pass #TODO

def setColor(pixel,color):
    #if not isinstance(pixel, Pixel):
    #    print "setColor(pixel,color): First input is not a pixel"
    #    raise ValueError
    #if not isinstance(color, Color):
    #    print "setColor(pixel,color): Second input is not a color"
    #    raise ValueError
    #pixel.setColor(color.color)
    pass #TODO

def getX(pixel):
    #if not isinstance(pixel, Pixel):
    #    print "getX(pixel): Input is not a pixel"
    #    raise ValueError
    #return pixel.getX() + Picture._PictureIndexOffset
    pass #TODO

def getY(pixel):
    #if not isinstance(pixel,Pixel):
    #    print "getY(pixel): Input is not a pixel"
    #    raise ValueError
    #return pixel.getY() + Picture._PictureIndexOffset
    pass #TODO

#Done
def distance(c1,c2):
    if not isinstance(c1, Color):
        print "distance(c1,c2): First input is not a color"
        raise ValueError
    if not isinstance(c2, Color):
        print "distance(c1,c2): Second input is not a color"
        raise ValueError
    return c1.distance(c2)

def writePictureTo(picture,filename):
    #global mediaFolder
    #if not os.path.isabs(filename):
    #    filename = mediaFolder + filename
    #if not isinstance(picture, Picture):
    #    print "writePictureTo(picture,filename): First input is not a picture"
    #    raise ValueError
    #picture.writeOrFail(filename)
    pass #TODO
#   if not os.path.exists(filename):
#       print "writePictureTo(pict,filename): Path is not valid"
#       raise ValueError



# not to be confused with setColor, totally different, don't document/export
def _setColorTo(color, other):
    color.setRGB(other.getRed(), other.getGreen(), other.getBlue())
    return color

#def makeDarker(color):
    #"""This function has side effects on purpose, see p49 """
    #return _setColorTo(color, color.darker())

def makeDarker(color):
  if not isinstance(color,Color):
      print "makeDarker(color): Input is not a color"
      raise ValueError
  return Color( color.makeDarker() )
  #TODO maybe done?

#def makeLighter(color):
  #"""This function has side effects on purpose, see p49"""
  #return _setColorTo(color,color.brighter())

def makeLighter(color):
  if not isinstance(color,Color):
      print "makeLighter(color): Input is not a color"
      raise ValueError
  return Color( color.makeLighter() )
  #TODO maybe done?

def makeBrighter(color): #This is the same as makeLighter(color)
  if not isinstance(color,Color):
      print "makeBrighter(color): Input is not a color"
      raise ValueError
  return Color( color.makeLighter() )
  #TODO maybe done?

#Done
def makeColor(red,green=None,blue=None):
    return Color( red, green, blue)

def setAllPixelsToAColor(picture,color):
    ##"""This function sets the picture to one color"""
    #if not isinstance(picture, Picture):
    #    print "setAllPixelsToAColor(picture,color): First input is not a picture"
    #    raise ValueError
    #if not isinstance(color,Color):
    #    print "setAllPixelsToAColor(picture,color): Second input is not a color"
    #    raise ValueError
    #picture.setAllPixelsToAColor(color.color)
    #TODO maybe done?


def copyInto(smallPicture, bigPicture, startX, startY):
    ##like copyInto(butterfly, jungle, 20,20)
    #if not smallPicture.__class__ == Picture:
    #    print "copyInto(smallPicture, bigPicture, startX, startY): smallPicture must be a picture"
    #    raise ValueError
    #if not bigPicture.__class__ == Picture:
    #    print "copyInto(smallPicture, bigPicture, startX, startY): bigPicture must be a picture"
    #    raise ValueError
    #if (startX < Picture._PictureIndexOffset) or (startX > getWidth(bigPicture) - 1 + Picture._PictureIndexOffset):
    #    print "copyInto(smallPicture, bigPicture, startX, startY): startX must be within the bigPicture"
    #    raise ValueError
    #if (startY < Picture._PictureIndexOffset) or (startY > getHeight(bigPicture) - 1 + Picture._PictureIndexOffset):
    #    print "copyInto(smallPicture, bigPicture, startX, startY): startY must be within the bigPicture"
    #    raise ValueError
    #if (startX + getWidth(smallPicture) - 1) > (getWidth(bigPicture) - 1 + Picture._PictureIndexOffset) or \
    #        (startY + getHeight(smallPicture) - 1) > (getHeight(bigPicture) - 1 + Picture._PictureIndexOffset):
    #    print "copyInto(smallPicture, bigPicture, startX, startY): smallPicture won't fit into bigPicture"
    #    raise ValueError

    #xOffset = startX - Picture._PictureIndexOffset
    #yOffset = startY - Picture._PictureIndexOffset

    #for x in range(0, getWidth(smallPicture)):
    #    for y in range(0, getHeight(smallPicture)):
    #        bigPicture.setBasicPixel(x + xOffset, y + yOffset, smallPicture.getBasicPixel(x,y))

    #return bigPicture
    pass #TODO

# Alyce Brady's version of copyInto, with additional error-checking on the upper-left corner
# Will copy as much of the original picture into the destination picture as will fit.
#def copyInto(origPict, destPict, upperLeftX, upperLeftY):
#  if not isinstance(origPict, Picture):
#    print "copyInto(origPict, destPict, upperLeftX, upperLeftY): First parameter is not a picture"
#    raise ValueError
#  if not isinstance(destPict, Picture):
#    print "copyInto(origPict, destPict, upperLeftX, upperLeftY): Second parameter is not a picture"
#    raise ValueError
#  if upperLeftX < 1 or upperLeftX > getWidth(destPict):
#    print "copyInto(origPict, destPict, upperLeftX, upperLeftY): upperLeftX must be within the destPict"
#    raise ValueError
#  if upperLeftY < 1 or upperLeftY > getHeight(destPict):
#    print "copyInto(origPict, destPict, upperLeftX, upperLeftY): upperLeftY must be within the destPict"
#    raise ValueError
#  return origPict.copyInto(destPict, upperLeftX-1, upperLeftY-1)

def duplicatePicture(picture):
    #"""returns a copy of the picture"""
    #if not isinstance(picture, Picture):
    #    print "duplicatePicture(picture): Input is not a picture"
    #    raise ValueError
    #return Picture(picture)
    pass #TODO

# Alyce Brady/ Pam Cutter: Function that crops a picture
#def cropPicture(picture, upperLeftX, upperLeftY, width, height):
#  if not isinstance(picture, Picture):
#    print "crop(picture, upperLeftX, upperLeftY, width, height): First parameter is not a picture"
#    raise ValueError
#  if upperLeftX < 1 or upperLeftX > getWidth(picture):
#    print "crop(picture, upperLeftX, upperLeftY, width, height): upperLeftX must be within the picture"
#    raise ValueError
#  if upperLeftY < 1 or upperLeftY > getHeight(picture):
#    print "crop(picture, upperLeftX, upperLeftY, width, height): upperLeftY must be within the picture"
#    raise ValueError
#  return picture.crop(upperLeftX-1, upperLeftY-1, width, height)

##
# Input and Output interfaces
#
# Note: These calls must be done in a threadsafe manner since the JESThread will be
# executing them rather than the GUI's event dispatch thread.  See SimpleInput/Output.java
# for the threadsafe execution.
##

#  radius = SimpleInput.getNumber("Enter the radius of the cylinder")
#  SimpleOutput.showInformation("The volume of the cylinder is %.02f " % volume)

def requestNumber(message):
    #return SimpleInput.getNumber(message)
    pass #TODO

def requestInteger(message):
    #return SimpleInput.getIntNumber(message)
    pass #TODO

def requestIntegerInRange(message, min, max):
    if min >= max:
        print "requestIntegerInRange(message, min, max): min >= max not allowed"
        raise ValueError

    #return SimpleInput.getIntNumber(message, min, max)
    #TODO

def requestString(message):
    #return SimpleInput.getString(message)
    pass #TODO


#5/15/09 Dorn: Updated input and raw_input to read from the console
#def input(message=None):
#    im = JESInputManager()
#    return eval(im.readInput(message))

#def raw_input(message=None):
#    im = JESInputManager()
#    return im.readInput(message)
    

def showWarning(message):
    #return SimpleOutput.showWarning(message)
    pass #TODO

def showInformation(message):
    #return SimpleOutput.showInformation(message)
    pass #TODO

def showError(message):
    #return SimpleOutput.showError(message)
    pass #TODO


##
# Java Music Interface
##
def playNote(note, duration, intensity=64):
    #JavaMusic.playNote(note, duration, intensity)
    pass #TODO


##
# General user tools
#

def pickAFile():
    ## Note: this needs to be done in a threadsafe manner, see FileChooser
    ## for details how this is accomplished.
    #return FileChooser.pickAFile()
    pass #TODO

def pickAFolder():
    ## Note: this needs to be done in a threadsafe manner, see FileChooser
    ## for details how this is accomplished.
    #dir = FileChooser.pickADirectory() TODO
    if ( dir != None ):
        return dir + os.sep
    return None

def quit():
    sys.exit(0)

##
# MediaTools interface
#
# TODO modify viewer.changeToBaseOne

def openPictureTool(picture):
    #import PictureExplorer
    #thecopy = duplicatePicture(picture)
    #viewer = PictureExplorer(thecopy)

#    viewer.changeToBaseOne();
    #viewer.setTitle(getShortPath(picture.getFileName() ))
    pass #TODO

def openFrameSequencerTool(movie):
    #FrameSequencerTool.FrameSequencerTool(movie)
    pass #TODO

def openSoundTool(sound):
    #import SoundExplorer
    #thecopy = Sound(sound)
    #viewer = SoundExplorer(thecopy, 0)
    #try:
    #    viewer.setTitle(getShortPath(sound.getFileName()))
    #except:
    #    viewer.setTitle("No File Name")
    pass #TODO

#Done
def explore(someMedia):
    if isinstance(someMedia, Picture):
	openPictureTool(someMedia)
    elif isinstance(someMedia, Sound):
	openSoundTool(someMedia)
    elif isinstance(someMedia, Movie):
	openFrameSequencerTool(someMedia)
    else:
	print "explore(someMedia): Input is not a Picture, Sound, or Movie"
	raise ValueError

# let's try the turtles...
#import Turtle
#import World
#TODO use turtle package

def turn(turtle, degrees=90):
    #if not isinstance(turtle, Turtle):
    #    print "turn(turtle[, degrees]): Input is not a turtle"
    #    raise ValueError
    #else:
    #    turtle.turn(degrees)
    pass #TODO

def turnRight(turtle):
    #if not isinstance(turtle,Turtle):
    #    print "turnRight(turtle): Input is not a turtle"
    #    raise ValueError
    #else:
    #    turtle.turnRight()
    pass #TODO

def turnToFace(turtle, x, y=None):
    #if y == None:
    #    if not (isinstance(turtle, Turtle) and isinstance(x, Turtle)):
    #        print "turnToFace(turtle, turtle): First input is not a turtle"
    #        raise ValueError
    #    else:
    #        turtle.turnToFace(x)
    #else:
    #    if not isinstance(turtle, Turtle):
    #        print "turnToFace(turtle, x, y): Input is not a turtle"
    #        raise ValueError
    #    else:
    #        turtle.turnToFace(x, y)
    pass #TODO

def turnLeft(turtle):
    #if not isinstance(turtle, Turtle):
    #    print "turnLeft(turtle): Input is not a turtle"
    #    raise ValueError
    #else:
    #    turtle.turnLeft()
    pass #TODO

def forward(turtle, pixels=100):
    #if not isinstance(turtle,Turtle):
    #    print "forward(turtle[, pixels]): Input is not a turtle"
    #    raise ValueError
    #else:
    #    turtle.forward(pixels)
    pass #TODO

def backward(turtle, pixels=100):
    #if not isinstance(turtle, Turtle):
    #    print "backward(turtle[, pixels]): Input is not a turtle"
    #    raise ValueError
    #if (None == pixels):
    #    turtle.backward()
    #else:
    #    turtle.backward(pixels)
    pass #TODO

def moveTo(turtle, x, y):
    #if not isinstance(turtle,Turtle):
    #    print "moveTo(turtle, x, y): Input is not a turtle"
    #    raise ValueError
    #turtle.moveTo(x,y)
    pass #TODO

def makeTurtle(world):
    #if not (isinstance(world, World) or isinstance(world, Picture)):
    #    print "makeTurtle(world): Input is not a world or picture"
    #    raise ValueError
    #turtle = Turtle(world)
    #return turtle
    pass #TODO

def penUp(turtle):
    #if not isinstance(turtle, Turtle):
    #    print "penUp(turtle): Input is not a turtle"
    #    raise ValueError
    #turtle.penUp()
    pass #TODO

def penDown(turtle):
    #if not isinstance(turtle, Turtle):
    #    print "penDown(turtle): Input is not a turtle"
    #    raise ValueError
    #turtle.penDown()
    pass #TODO

def drop(turtle, picture):
    #if not isinstance(turtle, Turtle):
    #    print "drop(turtle, picture): First input is not a turtle"
    #    raise ValueError
    #if not isinstance(picture,Picture):
    #    print "drop(turtle, picture): Second input is not a picture"
    #    raise ValueError
    #turtle.drop(picture)
    pass #TODO

def getXPos(turtle):
    #if not isinstance(turtle, Turtle):
    #    print "getXPos(turtle): Input is not a turtle"
    #    raise ValueError
    #return turtle.getXPos()
    pass #TODO

def getYPos(turtle):
    #if not isinstance(turtle,Turtle):
    #    print "getYPos(turtle): Input is not a turtle"
    #    raise ValueError
    #return turtle.getYPos()
    pass #TODO

def getHeading(turtle):
    #if not isinstance(turtle,Turtle):
    #    print "getHeading(turtle): Input is not a turtle"
    #    raise ValueError
    #return turtle.getHeading()
    pass #TODO

## add these things: turnToFace(turtle, another turtle)
## getHeading, getXPos, getYPos

## world methods
def makeWorld(width=None, height=None):
    #if(width and height):
    #    w = World(width, height)
    #else:
    #    w = World()
    #return w
    pass #TODO

def getTurtleList(world):
    #if not isinstance(world, World):
    #    print "getTurtleList(world): Input is not a world"
    #    raise ValueError
    #return world.getTurtleList()
    pass #TODO

# end of stuff imported for worlds and turtles

# used in the book
def printNow(text):
    #sys.stdout.printNow("%s\n" % text)
    pass #TODO

class Movie:
    #TODO probably needs major overhaul
    def __init__(self): # frames are filenames
        self.frames = []
        self.dir = None

    def addFrame(self, frame):
        self.frames.append(frame)
        self.dir = None

    def __len__(self):
        return len(self.frames)

    def __str__(self):
        return "Movie, frames: "+str(len(self))

    def __repr__(self):
        return "Movie, frames: "+str(len(self))

    def __getitem__(self,item):
        return self.frames[item]

    def writeFramesToDirectory(self, directory):
        import FrameSequencer
        fs = FrameSequencer(directory)
        #for frameindex in range(0, self.listModel.size()):
            #fs.addFrame(Picture(self.listModel.get(frameindex)))
            #fs.play(self.fps)
        for frameindex in range(0, len(self.frames)):
            fs.addFrame(Picture(self.frames[frameindex]))
        self.dir = directory

    def play(self):
        import java.util.ArrayList as ArrayList
        list = ArrayList()
        for f in self.frames:
            list.add( makePicture(f) )
        MoviePlayer(list).playMovie()

    def writeQuicktime(self, destPath, framesPerSec = 16):
        global mediaFolder
        if not os.path.isabs(destPath):
            destPath = mediaFolder + destPath
        destPath = "file://"+destPath
        if framesPerSec <= 0:
            print "writeQuicktime(path[, framesPerSec]): Frame Rate must be a positive number"
            raise ValueError
        if self.frames == []: #Is movie empty?
            print "writeQuicktime(path[, framesPerSec]): Movie has no frames. Cannot write empty Movie"
            raise ValueError
        elif self.dir == None and len(self.frames) == 1: #Is movie only 1 frame but never written out
            frame = self.frames[0]
            self.dir = frame[:(frame.rfind(os.sep))]
        elif self.dir == None and len(self.frames) > 1: #Are movie frames all in the same directory? 
            sameDir = 1
            frame = self.frames[0]
            frame = frame.replace('/', os.sep)
            framesDir = frame[:(frame.rfind(os.sep))] #Parse directory of first frame
            thisDir = framesDir
            frameNum = 1
            while(sameDir and frameNum < len(self.frames)):
                frame = self.frames[frameNum]
                frame = frame.replace('/', os.sep) #Eliminate possibility of / vs. \ causing problems
                thisDir = frame[:(frame.rfind(os.sep))]
                frameNum = frameNum+1
                if(framesDir <> thisDir):
                    sameDir = 0
            if(sameDir): #Loop ended because we ran out of frames
                self.dir = framesDir
            else: #Loop ended because sameDir became false
                print "writeQuicktime(path[, framesPerSec]): Your frames are in different directories. Call writeFramesToDirectory() first, then try again."
                raise ValueError
        writer = MovieWriter(self.dir, framesPerSec, destPath)
        writer.writeQuicktime()
        
    def writeAVI(self, destPath, framesPerSec = 16):
        global mediaFolder
        if not os.path.isabs(destPath):
            destPath = mediaFolder + destPath
        destPath = "file://"+destPath
        if framesPerSec <= 0:
            print "writeAVI(path[, framesPerSec]): Frame Rate must be a positive number"
            raise ValueError
        if self.frames == []: #Is movie empty?
            print "writeAVI(path[, framesPerSec]): Movie has no frames. Cannot write empty Movie"
            raise ValueError
        elif self.dir == None and len(self.frames) == 1: #Is movie only 1 frame but never written out
            frame = self.frames[0]
            self.dir = frame[:(frame.rfind(os.sep))]
        elif self.dir == None and len(self.frames) > 1: #Are movie frames all in the same directory? 
            sameDir = 1
            frame = self.frames[0]
            frame = frame.replace('/', os.sep)
            framesDir = frame[:(frame.rfind(os.sep))] #Parse directory of first frame
            thisDir = framesDir
            frameNum = 1
            while(sameDir and frameNum < len(self.frames)):
                frame = self.frames[frameNum]
                frame = frame.replace('/', os.sep)
                thisDir = frame[:(frame.rfind(os.sep))]
                frameNum = frameNum+1
                if(framesDir <> thisDir):
                    sameDir = 0
            if(sameDir): #Loop ended because we ran out of frames
                self.dir = framesDir
            else: #Loop ended because sameDir became false
                print "writeAVI(path[, framesPerSec]): Your frames are in different directories. Call writeFramesToDirectory() first, then try again."
                raise ValueError
        writer = MovieWriter(self.dir, framesPerSec, destPath)
        writer.writeAVI()
#Done
def playMovie( movie ):
    if isinstance( movie, Movie ):
        movie.play()
    else:
        print "playMovie( movie ): Input is not a Movie"
        raise ValueError

#Done
def writeQuicktime(movie, destPath, framesPerSec = 16):
    if not (isinstance(movie, Movie)):
        print "writeQuicktime(movie, path[, framesPerSec]): First input is not a Movie"
        raise ValueError
    if framesPerSec <= 0:
        print "writeQuicktime(movie, path[, framesPerSec]): Frame rate must be a positive number"
        raise ValueError
    movie.writeQuicktime(destPath, framesPerSec)

#Done
def writeAVI(movie, destPath, framesPerSec = 16):
    if not (isinstance(movie, Movie)):
        print "writeAVI(movie, path[, framesPerSec]): First input is not a Movie"
        raise ValueError
    if framesPerSec <= 0:
        print "writeAVI(movie, path[, framesPerSec]): Frame rate must be a positive number"
        raise ValueError
    movie.writeAVI(destPath, framesPerSec)

#Done
def makeMovie():
    return Movie()

#Done
def makeMovieFromInitialFile(filename):
    import re
    movie = Movie()

    #filename = filename.replace(os.altsep, os.sep)
    filename = filename.replace('/',os.sep) #Hack fix because os.altsep is not defined for Windows as of Python 2.2
    sep_location = filename.rfind(os.sep)
    if(-1 == sep_location):
        filename = mediaFolder + filename

    movie.directory = filename[:(filename.rfind(os.sep))]
    movie.init_file = filename[(filename.rfind(os.sep))+1:]
    regex = re.compile('[0-9]+')
    file_regex = regex.sub('.*', movie.init_file)

    for item in os.listdir(movie.directory):
        if re.match(file_regex, item):
            movie.addFrame(movie.directory + os.sep + item)

    return movie

#Done
def addFrameToMovie(a, b):
    frame = None
    movie = None
    if a.__class__ == Movie:
        movie = a
        frame = b
    else:
        movie = b
        frame = a

    if not (isinstance(movie,Movie) and isinstance(frame,String)):
   # if movie.__class__ != Movie or frame.__class__ != String:
        print "addFrameToMovie(frame, movie): frame is not a string or movie is not a Movie object"
        raise ValueError

    movie.addFrame(frame)

#Done
def writeFramesToDirectory(movie, directory=None):
    if not isinstance(movie, Movie):
        print "writeFramesToDirectory(movie[, directory]): movie is not a Movie object"
        raise ValueError

    if directory == None:
        directory = user.home

    movie.writeFramesToDirectory(directory)

#def playMovie(movie):
#    if not isinstance(movie, Movie):
#        print "playMovie(movie): movie is not a Movie object."
#        raise ValueError
#    movie.play()
