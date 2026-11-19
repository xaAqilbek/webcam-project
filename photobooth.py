import cv2
import os
from datetime import datetime

os.makedirs("photos", exist_ok=True)

cap = cv2.VideoCapture(0)
mode = "normal"

while True:
    ret, frame = cap.read()
    if not ret:
        print("Could not read video file")
        break

    frame  = cv2.flip(frame, 1)

    if mode == "gray":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        view = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif mode == "edges":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        view = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    else:
        view = frame

    saved = view.copy()  # копия БЕЗ надписи, её и будем сохранять

    cv2.putText(view, f"Mode: {mode} | s: save | q: quit", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Photobooth", view)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('1'):
        mode = "normal"
    elif key == ord('2'):
        mode = "gray"
    elif key == ord('3'):
        mode = "edges"
    elif key == ord('s'):
        name = datetime.now().strftime("photos/photo_%Y%m%d_%H%M%S.jpg")
        cv2.imwrite(name, saved)
        print("Saved:", name)

cap.release()
cv2.destroyAllWindows()

