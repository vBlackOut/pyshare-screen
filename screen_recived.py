import socket
import base64
import time


TCP_IP = '127.0.0.1'
TCP_PORT = 16000

BUFFER_SIZE = 9999999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
#s.send(MESSAGE)
while True:
#On récupère les 8 premier octets
    tailleImage = s.recv(8)
#On convertit la taille de l'image en entier (en octets)
    tailleImage = int(tailleImage.decode())
#Contenu téléchargé en octets
    contenuTelecharge = 0
#Le fichier qui va contenir l'image
    fichierImage = open("image.jpg","wb")
 
#On a la taille de l'image, jusqu'à ce qu'on ait tout téléchargé
    while contenuTelecharge < tailleImage:
    #On lit les 1024 octets suivant
        contenuRecu = s.recv(5000)
    #On enregistre dans le fichier
        fichierImage.write(contenuRecu)
    #On ajoute la taille du contenu reçu au contenu téléchargé
        contenuTelecharge += len(contenuRecu)
fichierImage.close()

s.close()