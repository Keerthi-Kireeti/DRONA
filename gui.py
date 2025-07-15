import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt

class AIInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Assistant GUI")
        self.setGeometry(100, 100, 800, 450)  # Window size
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Background Label
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 800, 450)

        # Load and set the futuristic interface image
        pixmap = QPixmap("Capture2.PNG")  # Ensure this image exists
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setScaledContents(True)

        # Center Animation (GIF for glow effect)
        self.center_animation = QLabel(self)
        movie = QMovie("motion.gif")  # Ensure this GIF exists
        self.center_animation.setMovie(movie)
        movie.start()

        # Adjust GIF position dynamically
        self.adjust_gif_position()

        self.show()

    def adjust_gif_position(self):
        """Dynamically center the GIF based on window size."""
        gif_width = 300  # Adjust according to your GIF size
        gif_height = 300  
        x = (self.width() - gif_width) // 2
        y = (self.height() - gif_height) // 2
        self.center_animation.setGeometry(x, y, gif_width, gif_height)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIInterface()
    sys.exit(app.exec_())
