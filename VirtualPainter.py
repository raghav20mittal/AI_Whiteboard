import cv2
import numpy as np
import os
import HandTrackingModule as htm

# Brush and eraser thickness
brushThickness = 15
eraserThickness = 50

# Header dimensions
headerHeight = 137
headerWidth = 1280

# Load UI images for the header
folderPath = "UI"
if not os.path.exists(folderPath):
    raise FileNotFoundError(f"The folder '{folderPath}' does not exist.")
myList = os.listdir(folderPath)
print("UI Images:", myList)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    if image is None:
        raise FileNotFoundError(f"Unable to load image '{imPath}' from folder '{folderPath}'.")
    # Resize each header to match the canvas size
    image = cv2.resize(image, (headerWidth, headerHeight))
    overlayList.append(image)

print(f"Number of UI Images Loaded: {len(overlayList)}")
header = overlayList[0]
drawColor = (255, 0, 255)  # Default drawing color (purple)

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot access the camera. Check the camera index or connection.")

cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Initialize hand detector
detector = htm.handDetector(detectionCon=0.85, maxHands=1)

# Canvas for drawing
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
xp, yp = 0, 0  # Previous points for drawing

while True:
    # Read frame from camera
    success, img = cap.read()
    if not success:
        print("Failed to capture frame from camera. Retrying...")
        continue

    img = cv2.flip(img, 1)  # Flip horizontally for natural interaction

    # Find hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Get positions of index and middle finger tips
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check which fingers are up
        fingers = detector.fingersUp()

        # Selection mode (two fingers up)
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0  # Reset previous points
            if y1 < headerHeight:  # If finger is in header region
                if 350 < x1 < 440:
                    header = overlayList[0]
                    drawColor = (0, 0, 255)  # Red
                elif 530 < x1 < 650:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)  # Blue
                elif 700 < x1 < 820:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)  # Green
                elif 880 < x1 < 1000:
                    header = overlayList[3]
                    drawColor = (255, 255, 0)  # Yellow
                elif 1050 < x1 < 1170:
                    header = overlayList[4]
                    drawColor = (0, 0, 0)  # Eraser

        # Drawing mode (only index finger up)
        elif fingers[1] and not fingers[2]:
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # Draw on the canvas
            if drawColor == (0, 0, 0):  # Eraser
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness, cv2.LINE_AA)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness, cv2.LINE_AA)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness, cv2.LINE_AA)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness, cv2.LINE_AA)

            xp, yp = x1, y1

    # Combine the drawing with the video feed
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Add header to the image
    img[0:headerHeight, 0:headerWidth] = header

    # Show the final image
    cv2.imshow("Virtual Painter", img)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
