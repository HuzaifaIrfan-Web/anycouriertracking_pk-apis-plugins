try:
    from PIL import Image
except ImportError:
    import Image


import imutils

import cv2
import numpy as np



def captcha_solver(image_path,):

    print(image_path)
    # image= Image.open('18.png')
    image = cv2.imread(image_path)
    # print(image.shape)

    frame = image[0:40, 20:100] 

    # cv2.imshow('frame',frame)

    # 28 40 82
    # 154 165 193

    # lower_black = np.array([28,0,20],dtype = "uint16" )
    # upper_black = np.array([230,230,230], dtype = "uint16")
    # black_mask = cv2.inRange(frame, lower_black, upper_black)


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # lower_range = np.array([120,0,0])
    # upper_range = np.array([150,255,255])

    # 231 61 22
    # 226 21 72


    # mask = cv2.inRange(hsv, lower_range, upper_range)


        # Blue color
    low_blue = np.array([100, 10, 20])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv, low_blue, high_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    black_pixels = np.where(
        (blue[:, :, 0] == 0) & 
        (blue[:, :, 1] == 0) & 
        (blue[:, :, 2] == 0)
    )

    # set those pixels to white
    blue[black_pixels] = [255, 255, 255]




    gray = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)

    invet_gray  = 255- gray

    img_bw = 255*(invet_gray).astype('uint8')

    element = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    mask = cv2.erode(img_bw, element, iterations = 1)
    mask = cv2.dilate(mask, element, iterations = 1)
    mask = cv2.erode(mask, element)

    mask = np.dstack([mask, mask, mask]) / 255

    masked =  (hsv* mask)





    cv2.imwrite(image_path, masked)

    temp = 255- cv2.imread(image_path)

    img_grey = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)




    # define a threshold, 128 is the middle of black and white in grey scale
    thresh = 250

    # threshold the image
    img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]





    cv2.imwrite(image_path, img_binary)



    # image_frame=threshed


    # gray = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # for c in cnts:
    #     if cv2.contourArea(c) < 50:
    #         cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

    # result = 255 - thresh
    # cv2.imshow('result', result)









    image_frame = cv2.imread(image_path)


    # cv2.imshow('mask0',black_mask)

    # Simple image to string




    # cv2.imshow('result', image_frame)


    import pytesseract
    detected=pytesseract.image_to_string(image_frame, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz')
    # print('Detected: ', detected)

    import re
    onlytextnumber = re.sub('[\W_]+', '', detected)
    
    result = onlytextnumber[-4:]


    return result







