try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
    import io
from gi.repository import Gdk
from random import randint
from PIL import Image, ImageDraw
from Xlib import display, X
from mss import mss
from socket import *
import random
import time
import cv2
import os
import datetime
import zlib
import sys
import concurrent.futures

s = Gdk.Screen.get_default()
W = s.get_width()
H = s.get_height()

quality = 50

def convert_jpg(strings, scale_img, img_quality):
    buffer_in_memory = io.BytesIO()
    img_files = img_dir
    image_file = io.BytesIO(strings.read())
    img_file = Image.open(BytesIO(image_file))
    if scale_img == 100:
        width, height = img_file.size
    else:
        width, height = (int(scale_img * img_file.size[0] / 100.0), 
                        int(scale_img * img_file.size[1] / 100.0))

    img_file = img_file.resize((width, height), Image.ANTIALIAS)
    try:
        img_file.save(buffer_in_memory, "jpeg")
        img_file.save(img_files, 
                      optimize=True, 
                      quality=img_quality, 
                      progressive=True)
    except IOError:
        ImageFile.MAXBLOCK = width * height
        img_file.save(img_files, 
                      optimize=True, 
                      quality=img_quality, 
                      progressive=True)

def main():
    global quality
    if quality > 100:
    	quality = 100
    Csocket = socket(AF_INET, SOCK_DGRAM)

    data = display.Display().screen().root.query_pointer()._data
    with mss() as sct:
# We retrieve monitors informations:
        monitors = sct.enum_display_monitors()
# Get rid of the first, as it represents the "All in One" monitor:
        for num, monitor in enumerate(monitors[1:], 1):
    # Get raw pixels from the screen.
    # This method will store screen size into `width` and `height`
    # and raw pixels into `image`.
            sct.get_pixels(monitor)

    # Create an Image:
            img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)

    # And save it!
            buffer_in_memory = io.BytesIO()

            data = (data["root_x"], data["root_y"])

            im2 = img.resize((1300, 670), Image.ANTIALIAS) 
            x, y =  data
            eX, eY = 5, 5 #Size of Bounding Box for ellipse
            x1 = img.size[0]/1300
            y1 = img.size[1]/670
            x = x/x1
            y = y/y1
            bbox =  (x - eX/2, y - eY/2, x + eX/2, y + eY/2)
            draw = ImageDraw.Draw(im2)
            draw.ellipse(bbox, fill=128)
            del draw
            im2.save(buffer_in_memory, "jpeg", quality=quality, progressive=True, optimize=True,)
            contents = buffer_in_memory.getvalue()
            buffer_in_memory.seek(0)
            #convert_jpg(buffer_in_memory, 100, quality)
            #with open("output.jpg", "rb") as image_file:
            #    encoded_string = base64.b64encode(image_file.read())
            #im.show()
    #Chemin vers l'image
    fichierImage = contents

    deflate_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS)
    gzip_compress = deflate_compress.compress(fichierImage) + deflate_compress.flush()

    #On récupère la taille du fichier image en octets que l'on convertit en chaine de caractères
    tailleImage = str(len(gzip_compress))
    #On rajoute des 0 devant la taille jusqu'à que la chaine fasse 8 caractères
    for i in range(8-len(gzip_compress)):
        tailleImage = "0"+ gzip_compress

    time.sleep(0.0001)
    #self.send(tailleImage.encode())
    Csocket.sendto(tailleImage.encode(), ("164.132.9.247", 16000))
#On envoit le contenu du fichier
    try:
        print("send quality images : " + str(quality) + " size image " + str(tailleImage))
        Csocket.sendto(gzip_compress, ("164.132.9.247", 16000))

        if int(tailleImage) < 35535 and int(tailleImage) > 10000:
            quality = quality + 1
    except OSError:
    	quality = quality - 1
    return int(tailleImage)

#self.send("images:"+fichierImage.read())


def getPercentage(unew, uold, start):
    """ 
    calculate the percentage of cpu time 
    """ 
    return 50 * (float(unew) - float(uold)) / (time.time()-float(start))
 
def looper(timeCount, percentageGoal):
    """ 
    loop over many tasks and keep the total cpu percentage 
    consumtion to a desired level 
    """ 
    start = time.time()
    keepLooping = True
    uold, sold, cold, c, e = os.times()
    percentage = 0.0
    while keepLooping:
        percentageGoalCheck = random.randint(percentageGoal-5, percentageGoal+5)
        unew, snew, cnew, c, e = os.times()
        # since we are calculating the times from before we started looping the 
        # percentages will be averaged over the duration of the script. 
        print ("user %", percentage)
 
        # This just toggles to stop looping 
        # when a time has been reached. In a real 
        # script you would check for more work and 
        # toggle off when there is no more work to 
        # be done.
        if timeCount > 0:
            if time.time()-start > timeCount:
                keepLooping = False
        else:
            pass

            
        #else: 
        #    print( time.time()-start) 
 
        # do work: 
        #   In order for this script to actually help limit 
        #   the cpu usage you would need to break your script into 
        #   sections. 
        #   For example: if you were going to iterate through a large 
        #       list of data and perform actions on the contents 
        #       of the list then you should perform on action here 
        #       and keep looping through until all the actions 
        #       are accomplished. 
        # 
        # in this case we're just eating cpu so we get some numbers 
        image = main()
        #for i in range(1,1000000):
        #    b = 8*342*i*234

        # tone back cpu usage 
        while True:
            percentage = getPercentage(unew, uold, start)
            if image > 45535:
                if percentage > percentageGoal:
                    time.sleep(0.00005)
                else:
                    break;
            else:
                break;

if __name__ == '__main__':
    # loop through work (for 4 seconds) and keep the cpu % 
    # to less than 30% 
    fred = [25]
    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        for num in fred:
    	    lineexec = executor.submit(looper, 0, num)
