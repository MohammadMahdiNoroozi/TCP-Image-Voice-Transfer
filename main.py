import sys  # Importing the sys module for system-specific parameters and functions
# Importing classes for building the GUI application using PySide6
from PySide6.QtWidgets import *
from PySide6.QtCore import *  # Importing core functionality from PySide6
# Importing QtGui module from PySide6 for graphical features
from PySide6.QtGui import *
import cv2  # Importing the OpenCV library for computer vision tasks
import numpy as np  # Importing NumPy for numerical computing
# Importing QThread and Signal from PySide6 for multithreading
from PySide6.QtCore import QThread, Signal
from functools import partial  # Importing partial function from functools module

# Global flag for image change
global_flag = True  # Declaring a global flag to control image updates

capture_image_flg = 0  # Declaring a global flag to control capture image

# CSS-like button styles for various functionalities
button_style_r = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/play2b.png);
    }
    
    QPushButton:pressed {
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/play2b2.png);
    }
"""

button_style_si = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/capb.png);
    }
    
    QPushButton:pressed {
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/capb2.png);
    }
"""

button_style_sv = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/mic2b2.png);
    }
    
    QPushButton:pressed {
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/mic2b.png);
    }
"""

button_style_sav = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/dirb.png);
    }
    
    QPushButton:pressed {
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/dirb2.png);
    }
"""

button_style_send = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/sv7.png);
    }
    
    QPushButton:pressed {
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/sv7b.png);
    }
"""

button_style_sub = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        font-size: 16px;
        border-radius: 10px;
        color: #2eff04;
        border: 1px solid #2eff04;
    }
    
    QPushButton:pressed {
        border-radius: 12px;
        color: #fffd0a;
        border: 1px solid #fffd0a;
    }
"""


class ImageThread(QThread):
    # Define a signal to emit the image array
    change_image_signal = Signal(np.ndarray)

    def run(self):
        global global_flag  # Access the global flag for controlling image updates
        while True:
            if global_flag:  # Check if the flag is set for image update
                # Load and process the new image (can be replaced with custom logic)
                image = cv2.imread("imgs/no_image2.jpg")
                image = cv2.resize(image, (500, 400))
                # Emit the signal with the updated image
                self.change_image_signal.emit(image)
                # Reset the flag after updating the image to prevent continuous updates
                global_flag = False
            else:
                pass  # If the flag is not set, do nothing
            # Sleep to avoid busy wait and reduce CPU usage
            self.sleep(1)


class WebcamThread(QThread):
    # Define a signal to emit the webcam frame
    change_pixmap_signal = Signal(np.ndarray)

    def run(self):
        cap = cv2.VideoCapture(0)  # Initialize the webcam capture
        while True:
            ret, frame = cap.read()  # Read a frame from the webcam
            if ret:  # Check if the frame is successfully captured
                # Emit the signal with the captured frame
                self.change_pixmap_signal.emit(frame)
            else:
                pass  # If frame capture fails, do nothing to handle the error


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and initial geometry
        self.setWindowTitle("TCP connection")  # Set the window title
        self.setWindowTitle("Fixed Size Window")  # Set the window title
        # Set initial geometry (position and size)
        self.setGeometry(100, 100, 1050, 670)

        # Create a central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set background color for the window
        self.setStyleSheet("background-color: #000100;")

        # Create GUI layout
        self.create_layout()

        # Create and start webcam thread
        self.webcam_thread = WebcamThread()
        self.webcam_thread.change_pixmap_signal.connect(self.update_image)
        self.webcam_thread.start()

        # Create and start image thread
        self.image_thread = ImageThread()
        self.image_thread.change_image_signal.connect(self.update_left_image)
        self.image_thread.start()

    def create_layout(self):
        # Create main layout for central widget
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        # IP layout for entering IP address and port
        ip_widget = QWidget(self)
        ip_layout = QHBoxLayout()
        ip_layout.setObjectName("ipLayout")  # Set object name for styling

        # Label for displaying "IP : Port"
        desc = QLabel("IP : Port")
        desc.setStyleSheet(
            "color: #e500e8 ;background-color: None;font-size:25px; font-family:Comic Sans MS;")

        # Line edit for entering IP address
        ip_entry1 = QLineEdit()
        ip_entry1.setPlaceholderText("  IP")
        ip_entry1.setStyleSheet(
            "color: white; background-color: black; border: 1px solid #ed1ee7; border-radius: 10px;")

        # Line edit for entering port number
        ip_entry2 = QLineEdit()
        ip_entry2.setStyleSheet(
            "color: white; background-color: black; border: 1px solid #ed1ee7; border-radius: 10px;")
        ip_entry2.setPlaceholderText("  Port")

        # Button for connecting
        ip_button = QPushButton("Connect")
        ip_button.setStyleSheet(button_style_sub)
        ip_button.clicked.connect(self.connect)

        # Set fixed sizes for the widgets
        desc.setFixedSize(80, 30)
        ip_entry1.setFixedSize(150, 30)
        ip_entry2.setFixedSize(70, 30)
        ip_button.setFixedSize(100, 30)

        # Add widgets to IP layout
        ip_layout.addWidget(desc, 1)
        ip_layout.addWidget(ip_entry1, 4)
        ip_layout.addWidget(ip_entry2, 1)
        ip_layout.addWidget(ip_button, 1)

        # Align IP layout horizontally
        ip_layout.setAlignment(Qt.AlignHCenter)

        # Set IP layout to IP widget
        ip_widget.setLayout(ip_layout)

        # Add IP widget to main layout
        main_layout.addWidget(ip_widget, 1)

        ################################### Image layout ###################################
        # Create widgets for displaying images and buttons
        image_widget = QWidget(self)
        left_vertical_widget = QWidget(image_widget)
        right_vertical_widget = QWidget(image_widget)

        # Create a horizontal layout for arranging image widgets
        image_layout = QHBoxLayout()
        image_layout.setObjectName("imageLayout")

        # Set the layout for the image widget
        image_widget.setLayout(image_layout)
        # Add the image widget to the main layout with a stretch factor of 10
        main_layout.addWidget(image_widget, 10)

        # Create QLabel instances for displaying images
        self.left_image_label = QLabel(left_vertical_widget)
        self.left_image_label.resize(500, 400)

        # Create a QPushButton instance for left side functionalities
        left_button = QPushButton(left_vertical_widget)
        left_button.setStyleSheet(button_style_r)
        left_button.move(210, 410)
        left_button.resize(70, 70)
        left_button.clicked.connect(self.play_voice)

        # Create QLabel instance for displaying images on the right side
        self.right_top_image_label = QLabel(right_vertical_widget)
        self.right_top_image_label.resize(500, 400)

        # Create QPushButton instance for image capture functionality
        right_top_button = QPushButton(right_vertical_widget)
        right_top_button.setStyleSheet(button_style_si)
        right_top_button.move(120, 410)
        right_top_button.resize(80, 80)
        right_top_button.clicked.connect(self.capture_image)

        # Create QPushButton instance for recording voice functionality
        right_bottom_button1 = QPushButton(right_vertical_widget)
        right_bottom_button1.setStyleSheet(button_style_sv)
        right_bottom_button1.move(220, 410)
        right_bottom_button1.resize(70, 70)
        right_bottom_button1.clicked.connect(self.record_voice)

        # Create QPushButton instance for selecting voice directory functionality
        right_bottom_button2 = QPushButton(right_vertical_widget)
        right_bottom_button2.setStyleSheet(button_style_sav)
        right_bottom_button2.move(320, 410)
        right_bottom_button2.resize(70, 70)
        right_bottom_button2.clicked.connect(self.choose_voice_path)

        # Add left and right widgets to the image layout
        image_layout.addWidget(left_vertical_widget)
        image_layout.addWidget(right_vertical_widget)

        ################################### Send layout ###################################
        # Create a QPushButton instance for sending functionalities
        send_button = QPushButton(self)
        send_button.setStyleSheet(button_style_send)
        send_button.move(500, 600)
        send_button.resize(70, 70)

    def update_image(self, cv_img):
        """
        Update the image displayed on the right side of the window.

        Args:
            cv_img (numpy.ndarray): Image data in OpenCV format.

        Returns:
            None
        """
        global capture_image_flg

        # capture image and save it
        if capture_image_flg == 1:
            cv2.imwrite("./capture/myimg.png", cv_img)
            capture_image_flg = 0

        # Resize the image to fit the QLabel
        cv_img = cv2.resize(cv_img, (500, 400))
        # Convert the OpenCV image to a Qt image
        qt_img = QImage(
            cv_img.data, cv_img.shape[1], cv_img.shape[0], QImage.Format_RGB888).rgbSwapped()
        # Create a QPixmap from the Qt image and set it to the QLabel
        pixmap = QPixmap.fromImage(qt_img)
        self.right_top_image_label.setPixmap(pixmap)

    def update_left_image(self, cv_img):
        """
        Update the image displayed on the left side of the window.

        Args:
            cv_img (numpy.ndarray): Image data in OpenCV format.

        Returns:
            None
        """
        # Extract height, width, and channels from the image
        height, width, channel = cv_img.shape
        # Calculate bytes per line
        bytesPerLine = 3 * width
        # Convert the OpenCV image to a Qt image
        qt_img = QImage(cv_img.data, width, height,
                        bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        # Create a QPixmap from the Qt image and set it to the QLabel
        pixmap = QPixmap.fromImage(qt_img)
        self.left_image_label.setPixmap(pixmap)

    def connect(self):
        """
        Handle the functionality for connecting to a server.
        """
        pass

    def play_voice(self):
        """
        Handle the functionality for playing voice.
        """
        pass

    def capture_image(self):
        """
        Handle the functionality for capturing an image.
        """
        global capture_image_flg
        capture_image_flg = 1
        pass

    def record_voice(self):
        """
        Handle the functionality for recording voice.
        """
        pass

    def choose_voice_path(self):
        """
        Handle the functionality for choosing a voice path.
        """
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
