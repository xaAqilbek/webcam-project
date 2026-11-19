import cv2

#     For take a picture
#cap = cv2.VideoCapture(0)   # open the first camera (0 = default webcam)
#ret, frame = cap.read()     # take ONE picture

#if ret:                     # ret is True if the camera gave us a picture
#    cv2.imshow('Camera', frame)
#    cv2.waitKey(0)          # wait until you press any key
#else:
#    print("Could not read from camera")

#cap.release()               # free the camera so other programs can use it
#cv2.destroyAllWindows()     # close the window



cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):   # press q to quit
        break

cap.release()
cv2.destroyAllWindows()