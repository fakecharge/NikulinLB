# import the necessary modules
import freenect
import cv2
import numpy as np
import math


# function to get RGB image from kinect
def get_video():
    array, _ = freenect.sync_get_video()
    array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    return array, gray


# function to get depth image from kinect
def get_depth():
    array, _ = freenect.sync_get_depth()
    #print(x)
    array = array.astype(np.uint8)
    return array



if __name__ == "__main__":
    full_body_cascade = cv2.CascadeClassifier("haarcascade_upperbody.xml")
    #test = get_depth()
    #freenect.set_depth_mode(test, freenect.RESOLUTION_MEDIUM, freenect.DEPTH_REGISTERED)
    while 1:
        # get a frame from RGB camera
        frame, gray = get_video()
        depth = get_depth()
        full_body = full_body_cascade.detectMultiScale(gray, 1.05, 3)
        for (x,y,h,w) in full_body:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            x_g, y_g = int(x + w/2), int(y + h/2)
            print("Глубина: ", 0.1236 * math.tan(depth[x_g][y_g]/2842.5 + 1.1863))
        # get a frame from depth sensor
        # display RGB image
        cv2.imshow('RGB image', frame)
        # display depth image
        #cv2.imshow('Depth image', depth)

        # quit program when 'esc' key is pressed
        k = cv2.waitKey(10)
        if k == 27:
            break
    cv2.destroyAllWindows()