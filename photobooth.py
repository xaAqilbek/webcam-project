import cv2
import os
from datetime import datetime

os.makedirs("photos", exist_ok=True)

# Загружаем готовую "обученную" модель для поиска лиц (один раз, до цикла)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def find_faces(frame):
    """Принимает кадр, возвращает список лиц: каждое лицо это (x, y, w, h)."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5, minSize=(60, 60)
    )


cap = cv2.VideoCapture(0)
mode = "normal"

while True:
    ret, frame = cap.read()
    if not ret:
        print("Could not read from camera")
        break

    frame = cv2.flip(frame, 1)

    if mode == "gray":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        view = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    elif mode == "edges":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        view = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif mode == "blur":                      # клавиша 4: размываем лица
        view = frame
        for (x, y, w, h) in find_faces(frame):
            face_area = view[y:y + h, x:x + w]                    # вырезаем кусок с лицом
            view[y:y + h, x:x + w] = cv2.GaussianBlur(face_area, (99, 99), 30)  # размываем и кладём обратно

    elif mode == "boxes":                     # клавиша 5: рамки и счётчик
        view = frame
        faces = find_faces(frame)
        for (x, y, w, h) in faces:
            cv2.rectangle(view, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(view, f"Faces: {len(faces)}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    else:
        view = frame

    saved = view.copy()

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
    elif key == ord('4'):
        mode = "blur"
    elif key == ord('5'):
        mode = "boxes"
    elif key == ord('s'):
        name = datetime.now().strftime("photos/photo_%Y%m%d_%H%M%S.jpg")
        cv2.imwrite(name, saved)
        print("Saved:", name)

cap.release()
cv2.destroyAllWindows()