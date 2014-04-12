import cv2

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

cam = cv2.VideoCapture(0)

winName = "Movement Indicator"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

global_index = 1000
best_im = None
im = None

while True:
    diff_img = diffImg(t_minus, t, t_plus)
    for i in range(len(diff_img)):
        sorted_img = sorted(diff_img[i], reverse=True)
        if sorted_img[9] > 20:
            highest_index = i
            if highest_index < global_index:
                global_index = highest_index
                best_im = im
                print global_index
            break

    cv2.imshow(winName, t_plus)

    # Read next image
    t_minus = t
    t = t_plus
    im = cam.read()[1]
    t_plus = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winName)
        break

cv2.imwrite('test.png', best_im)

print "Goodbye"