AI Whiteboard
This project is a Virtual Whiteboard application built using Python, OpenCV, and MediaPipe. The application utilizes hand tracking to detect hand gestures and allows users to draw on a virtual canvas. It combines the power of computer vision with an intuitive user experience to provide an interactive and seamless drawing tool.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Features
1. Hand Tracking with MediaPipe:
   Uses MediaPipe's Hand module for real-time hand landmark detection.
   Tracks finger positions and identifies gestures.
   
3. Drawing on a Virtual Canvas:
   Allows users to draw by moving their hands in front of the camera.
   Recognizes gestures like finger pointing for more precise control.
   
5. Customizable Parameters:
   Adjust detection confidence, tracking confidence, and maximum hands for better performance on different systems.
   
7. Real-Time Frame Display:
   Captures live video feed and overlays the detected hand landmarks and drawings.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------

Usage Instructions
Clone the repository:
bash
Copy code
git clone https://github.com/viraj-lakshitha/ai-whiteboard-using-opencv.git
Install the required libraries:
bash
Copy code
pip upgrade --user pip
pip install opencv-python numpy mediapipe
Run the application:
Use PyCharm or a similar IDE to run the main script (e.g., VirtualPainter.py).
Or run it directly from the command line:
bash
Copy code
python VirtualPainter.py
