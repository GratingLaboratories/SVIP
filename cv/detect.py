import cv2

face_cascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("resources/haarcascade_eye.xml")

cap = cv2.VideoCapture(0)
cv2.namedWindow('small')


while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 1, minSize=(150, 150))
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.rectangle(img, (x, int(y + 0.25 * h)), (x + w, y + int(0.52 * h)), (0, 255, 255), 2)
        roi_gray = gray[int(y + 0.25 * h):y + int(0.52 * h), x:x + w]
        roi_color = img[int(y + 0.25 * h):y + int(0.52 * h), x:x + w]
        cv2.imshow('small', roi_color)
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 4, minSize=(20, 20), maxSize=(50, 50))
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    img = cv2.resize(img, None, fx=2, fy=2)
    img = cv2.flip(img, 1)
    cv2.imshow('img', img)
    if cv2.waitKey(10) & 0xFF == 27:
        break

cv2.destroyAllWindows()
cap.release()
