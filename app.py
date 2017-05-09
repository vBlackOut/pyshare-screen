#!/usr/bin/python2.7
# coding: utf-8
import socket
import base64
import time

import Tkinter
import random
from PIL import Image, ImageTk
import resource
import zlib

soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (1000, hard))

TCP_IP = '164.132.9.247'
TCP_PORT = 15000

BUFFER_SIZE = 9999999

#s.send(MESSAGE)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def Draw(oldframe=None):
    frame = Tkinter.Frame(top,width=100,height=100,relief='solid',bd=1)
    frame.place(x=10,y=10)
    frame.pack()

    global im
    while True:
    #On récupère les 8 premier octets
        tailleImage = s.recv(8)
    #On convertit la taille de l'image en entier (en octets)
        try:
            tailleImage = int(tailleImage.decode())
            print(tailleImage)
    #Contenu téléchargé en octets
            contenuTelecharge = 0
            totalstring = ""
    #Le fichier qui va contenir l'image
            fichierImage = open("image.jpg","wb")

    #On a la taille de l'image, jusqu'à ce qu'on ait tout téléchargé
            while contenuTelecharge < tailleImage:
        #On lit les 1024 octets suivant
                contenuRecu = s.recv(256)
        #On enregistre dans le fichier
                fichierImage.write(contenuRecu)
        #On ajoute la taille du contenu reçu au contenu téléchargé
                contenuTelecharge += len(contenuRecu)
                totalstring += contenuRecu
            fichierImage.close()
            break

        except UnicodeDecodeError:
            pass
        except ValueError:
            pass
    try:
        #totalstring = zlib.decompress(totalstring)
        try:
            gzip_compress = zlib.decompress(totalstring, zlib.MAX_WBITS)
            im = ImageTk.PhotoImage(data=gzip_compress)
            box1Label = Tkinter.Label(frame, image=im).pack()
        except:
            pass
        try:
           if oldframe is not None:
               oldframe.destroy() # cleanup
           return frame
        except:
           oldframe.destroy()
           return frame

    except IOError as e:
        print e
        return frame

def Refresher(frame=None):
    #print 'refreshing'
    frame = Draw(frame)
    try:
       frame.after(100, Refresher, frame) # refresh in 10 seconds
    except AttributeError as e:
       frame.after(100, Refresher, frame)
	

top = Tkinter.Tk()
Refresher()
Tkinter.mainloop()
s.close()
