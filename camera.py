import cv2

cap = cv2.VideoCapture(0)  # Use 1 for an external camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture frame. Check the camera connection.")
        break
    cv2.imshow("Camera Test", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
