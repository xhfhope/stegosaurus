from PIL import ImageTk, Image
import math
import os

def encode(image, secret, fileName):
    secret = "." + secret
    width, height = image.size
    
    if (width * height) < len(secret):
        raise ValueError
    
    imgPixels = image.load()

    #loop through letters
    for i in range(len(secret)):
        #get ascii
        asciiChar = str(ord(secret[i]))

        #get a new pixel location
        y = math.ceil(i/float(width))
        x = i%width
        pixel = imgPixels[y-1, x-1]
        #returns tuple, make into list
        myPixel = list(pixel)
        #convert pixel to strings
        myPixel[0] = str(myPixel[0])
        myPixel[1] = str(myPixel[1])
        myPixel[2] = str(myPixel[2])

        #chars starting with d in ascii
        #0's becomes 1's
        if ord(secret[i]) >= 100:
            r = list(myPixel[0])
            r[-1] = asciiChar[0]
            myPixel[0] = ''.join(r)

            r = list(myPixel[1])
            r[-1] = asciiChar[1]
            myPixel[1] = ''.join(r)

            r = list(myPixel[2])
            r[-1] = asciiChar[2]
            myPixel[2] = ''.join(r)

        #punctuation, capital chars and lower case through c
        elif ord(secret[i]) >= 10:
            #first byte always 0 for ascii chars <100
            r = list(myPixel[0])
            r[-1] = '0'
            myPixel[0] = ''.join(r)

            
            #here length of asciiChar = 2
            #2nd byte usually a 6 or a 7
            r = list(myPixel[1])
            r[-1] = asciiChar[0]
            myPixel[1] = ''.join(r)

            #
            r = list(myPixel[2])
            r[-1] = asciiChar[1]
            myPixel[2] = ''.join(r)

        else:
            r = list(myPixel[0])
            r[-1] = '0'
            myPixel[0] = ''.join(r)

            r = list(myPixel[1])
            r[-1] = '0'
            myPixel[1] = ''.join(r)

            r = list(myPixel[2])
            r[-1] = asciiChar[0]
            myPixel[2] = ''.join(r)

        #make into an int
        myPixel[0] = int(myPixel[0])
        myPixel[1] = int(myPixel[1])
        myPixel[2] = int(myPixel[2])
        imgPixels[y-1, x-1] = tuple(myPixel)
        
    y = math.ceil(len(secret)/float(width))
    x = len(secret)%width
    pixel = imgPixels[y, x]
    myPixel = list(pixel)
    myPixel[0] = str(myPixel[0])
    myPixel[1] = str(myPixel[1])
    myPixel[2] = str(myPixel[2])

    #encode a 127 to indicate end of string
    r = list(myPixel[0])
    r[-1] = '1'
    myPixel[0] = ''.join(r)
    r = list(myPixel[1])
    r[-1] = '2'
    myPixel[1] = ''.join(r)
    r = list(myPixel[2])
    r[-1] = '7'
    myPixel[2] = ''.join(r)

    myPixel[0] = int(myPixel[0])
    myPixel[1] = int(myPixel[1])
    myPixel[2] = int(myPixel[2])
    imgPixels[y-1, x-1] = tuple(myPixel)
    image.save("_" + fileName)


def decodeMessage(image):
    imgPixels = image.load()
    encodedText = ""
    width, height = image.size
    for x in range(width):
        for y in range(height):
            pixel = imgPixels[x,y]
            asciiChar = int(str(pixel[0])[-1]) * 100 + int(str(pixel[1])[-1]) * 10 + int(str(pixel[2])[-1])
            if(asciiChar == 127):
                return encodedText
            else:
                encodedText+=chr(asciiChar)
    return encodedText


inp = ''
inp = ''
fileName = ''

while True:
    if not inp == 'd' and not inp == 'e' and not inp == 'decode' and not inp == 'encode':
        inp, fileName = input("\n===Acceptable formats===\n[encode/decode] [filename.png]\n[e/d] [filename.png]\n\nInput: ").split(" ")
    else:
        inp, fileName = input("\nInput: ").split(" ")
    
    print()
    if inp == 'd' or inp == 'decode':
        print('Message:\n----------------\n' +decodeMessage(Image.open(fileName)))
    
    elif inp == 'e' or inp == 'encode':
        secret = input('Enter message to encode: ')
        try:
            encode(Image.open(fileName), secret, fileName)
            print('Message encoded. Output file created of same name prepended with \'_\'')
        except ValueError:
            print("Payload sequence too long")
