
import numpy as np
import cv2
import time  


dist = 0
focal = 1200
pixels = 30
width = 4


def get_dist(rectangle_params):

    pixels = rectangle_params[1][0]
    print("Width in pixels:", pixels)
    

    dist = (width * focal) / pixels
    
    return round(dist, 2)


cap = cv2.VideoCapture(0)


kernel = np.ones((3, 3), 'uint8')
font = cv2.FONT_HERSHEY_TRIPLEX 
color = (66, 11, 30) 
thickness = 2

cv2.namedWindow('Object Dist Measure', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Object Dist Measure', 700, 600)


last_tracking_time = time.time()
tracking_interval = 3/10  # secon


last_box = None
display_distance = None


while True:
    ret, img = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    img = cv2.flip(img, 1)


    cv2.imshow('Object Dist Measure', img)


    if time.time() - last_tracking_time >= tracking_interval:
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


        lower = np.array([0, 189, 96])
        upper = np.array([179, 255, 255])
        mask = cv2.inRange(hsv_img, lower, upper)


        d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=5)


        contours, hierarchy = cv2.findContours(d_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:

            largest_contour = max(contours, key=cv2.contourArea)


            if 100 < cv2.contourArea(largest_contour) < 306000:

                rect = cv2.minAreaRect(largest_contour)
                box = cv2.boxPoints(rect)
                box = np.int32(box)
                last_box = box  
                cv2.drawContours(img, [box], -1, (255, 0, 0), 3) 


                display_distance = get_dist(rect)


        last_tracking_time = time.time()


    if last_box is not None:
        cv2.drawContours(img, [last_box], -1, (255, 0, 0), 3) 


    if display_distance is not None:
        img = cv2.putText(img, 'tingkat sigma mangga (in cm):', (0, 55), font, 1, color, 2, cv2.LINE_AA)
        img = cv2.putText(img, str(display_distance) + " cm", (110, 120), font, 3, color, 1, cv2.LINE_AA)
    else:
        img = cv2.putText(img, 'gaada mangga.', (0, 20), font, 1, color, 2, cv2.LINE_AA)


    cv2.imshow('Object Dist Measure', img)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
