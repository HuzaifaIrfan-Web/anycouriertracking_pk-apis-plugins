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

  

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        # Blue color
    low_blue = np.array([100, 10, 20])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv, low_blue, high_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

  



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

    masked_iverted = 255- cv2.imread(image_path)

    img_grey = cv2.cvtColor(masked_iverted, cv2.COLOR_BGR2GRAY)




    # define a threshold, 128 is the middle of black and white in grey scale
    thresh = 250

    # threshold the image
    img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]





    cv2.imwrite(image_path, img_binary)

    image_frame = cv2.imread(image_path)
    



    import pytesseract
    detected=pytesseract.image_to_string(image_frame, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz')
    # print('Detected: ', detected)

    import re
    onlytextnumber = re.sub('[\W_]+', '', detected)
    
    result = onlytextnumber[-4:]


    return [image_frame ,result]







