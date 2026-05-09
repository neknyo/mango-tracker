import numpy as np
import cv2

cap = cv2.VideoCapture(0)

def empty(a):
    pass

def resize_final_img(x, y, axis, *argv):
    images = cv2.resize(argv[0], (x, y))
    for i in argv[1:]:
        resize = cv2.resize(i, (x, y))
        images = np.concatenate((images, resize), axis=axis)
    return images

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 300, 300)

# Reasonable default values for HSV ranges (adjust as needed)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 50, 255, empty)  # Min saturation set to 50
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 50, 255, empty)  # Min value set to 50
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

cv2.namedWindow('F')
cv2.resizeWindow('F', 700, 600)

while True:
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    img = cv2.flip(img, 1)
    
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    # Convert to HSV
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    
    # Create mask
    mask = cv2.inRange(hsv_img, lower, upper)
    kernel = np.ones((3, 3), 'uint8')

    # Apply morphological operations
    d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=5)

    # Convert mask and processed image to 3-channel (BGR) to match the original image
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    d_img_bgr = cv2.cvtColor(d_img, cv2.COLOR_GRAY2BGR)

    # Concatenate original image, mask, and processed mask horizontally
    final_img = resize_final_img(300, 300, 1, img, mask_bgr, d_img_bgr)
    
    cv2.imshow('F', final_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()
