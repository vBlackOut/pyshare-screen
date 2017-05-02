from __future__ import print_function
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
    import io

from random import randint
from PIL import Image, ImageDraw
from Xlib import display, X
import pyscreenshot
import collections
import asyncore
import logging
import socket
import base64
from base64 import encodestring, b64encode
import numpy as np
import time
import cv2
import pyscreeze
import concurrent.futures
import resource
from mss import mss
import os

from gi.repository import Gdk
s = Gdk.Screen.get_default()
W = s.get_width()
H = s.get_height()


MAX_MESSAGE_LENGTH = 999999

class RemoteClient(asyncore.dispatcher):

    """Wraps a remote client socket."""

    def __init__(self, host, socket, address):
        asyncore.dispatcher.__init__(self, socket)
        self.host = host
        self.outbox = collections.deque()

    def say(self, message):
        self.outbox.append(message)

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError('Message too long')
        self.send(message)

class Client(asyncore.dispatcher):

    def __init__(self, host_address, name):
        asyncore.dispatcher.__init__(self)
        self.log = logging.getLogger('Client (%7s)' % name)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.name = name
        self.log.info('Connecting to host at %s', host_address)
        self.connect(host_address)
        self.outbox = collections.deque()

    def say(self, loop):
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
                buffer_in_memory = StringIO()
                img.save('monitor-{0}.jpg'.format(num))

                data = (data["root_x"], data["root_y"])

                im = Image.open("monitor-1.jpg")

                x, y =  data
                eX, eY = 5, 5 #Size of Bounding Box for ellipse

                bbox =  (x - eX/2, y - eY/2, x + eX/2, y + eY/2)
                draw = ImageDraw.Draw(im)
                draw.ellipse(bbox, fill=128)
                del draw

                im.save("output.jpg", optimize=True, quality=100)
                time.sleep(0.10)
                with open("output.jpg", "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                #im.show()
        #Chemin vers l'image
        cheminImage = "output.jpg"
        fichierImage = open(cheminImage, "rb")
 
        #On récupère la taille du fichier image en octets que l'on convertit en chaine de caractères
        tailleImage = str(os.path.getsize(cheminImage))
        #On rajoute des 0 devant la taille jusqu'à que la chaine fasse 8 caractères
        for i in range(8-len(tailleImage)):
            tailleImage = "0"+ tailleImage
 
        #On a la taille de l'image, on l'envoie au client
        self.send(tailleImage.encode())
 
        #On envoit le contenu du fichier
        self.send(fichierImage.read())
        #self.send("images:"+fichierImage.read())

    def handle_error(self):
        print("Serveur is down.")
        exit()

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError('Message too long')
        self.send(message)

if __name__ == '__main__':
	print('Creating clients')
	client = Client(("127.0.0.1", 16000), 'User_'+str(randint(0,500)))
	count = 0
	while True:
		count = count + 1
		client.say(count)
		time.sleep(0.02)
