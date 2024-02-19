import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QScrollArea
from pytube import YouTube
import requests
from PyQt6.QtGui import QPixmap, QPainter, QFont, QColor, QIcon
from PyQt6.QtCore import Qt
import threading




class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Download Youtube Video")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set icon
        self.setWindowIcon(QIcon("icon.ico"))
        
        # Create a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.central_widget.setLayout(QVBoxLayout())
        self.central_widget.layout().addWidget(self.scroll_area)

        # Create a widget to hold the contents
        self.scroll_content = QWidget()
        self.scroll_content.setLayout(QVBoxLayout())
        self.scroll_area.setWidget(self.scroll_content)

        # Text Area
        self.text_area = QTextEdit()
        self.text_area.setFixedHeight(30)
        self.scroll_content.layout().addWidget(self.text_area)

        # Button
        self.button = QPushButton("Search URL")
        self.button.clicked.connect(self.button_clicked)
        self.scroll_content.layout().addWidget(self.button)

    def button_clicked(self):
        text = self.text_area.toPlainText()
        if text.strip() != "":
            url = text
            try:
                yt = YouTube(url)
                yt.streams.get_highest_resolution()
                print(yt.thumbnail_url)
                self.displayImage(yt)
            except:
                print("Video not found")



    def displayImage(self, yt):
        response = requests.get(yt.thumbnail_url)
        image_data = response.content
        thumbnail_label = QLabel()
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        scaled_pixmap = pixmap.scaled(400, 200, Qt.AspectRatioMode.KeepAspectRatio)

        thumbnail_label.setPixmap(scaled_pixmap)
        thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_content.layout().addWidget(thumbnail_label)

        painter = QPainter()
        scaled_pixmap = pixmap.scaled(400, 200, Qt.AspectRatioMode.KeepAspectRatio)

        painter.begin(scaled_pixmap)
        painter.setPen(QColor(Qt.GlobalColor.white))
        painter.setFont(QFont("Arial", 12))

        duration_seconds = yt.length
        duration_str = str(int(duration_seconds // 3600)).zfill(2) + ':' + str(int((duration_seconds % 3600) // 60)).zfill(2) + ':' + str(int(duration_seconds % 60)).zfill(2)
        print(duration_str)
        if duration_str[0:2] == "00":
            duration_str = duration_str[3::]

        if len(duration_str) == 5:
            painter.drawText(220, 195, duration_str)
        else:
            painter.drawText(190, 195, duration_str)

        painter.end()

        thumbnail_label.setPixmap(scaled_pixmap)
        thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scroll_content.layout().addWidget(thumbnail_label)

        buttonDownload = QPushButton("Start Download", self)
        buttonDownload.clicked.connect(lambda: self.on_buttonDownload_click(yt, buttonDownload))
        self.scroll_content.layout().addWidget(buttonDownload)


    def on_buttonDownload_click(self, yt, button):
        button.setText("Please wait! Downloading...")
        threading.Thread(target=self.download_video, args=(yt, button)).start()

    
    def deleteInvalidCharactersFromFilename(self, filename):
        filename = filename.replace("<","")
        filename = filename.replace(">","")
        filename = filename.replace(":","")
        filename = filename.replace("\"","")
        filename = filename.replace("/","")
        filename = filename.replace("\\","")
        filename = filename.replace("|","")
        filename = filename.replace("?","")
        filename = filename.replace("*","")
        return filename

    def download_video(self, yt, button):
        print(yt.title)
        # Get the highest resolution stream
        streamVideo = yt.streams.get_highest_resolution()
        # Define the filename
        filename = yt.title + ".mp4"
        print("filename: ",filename)
        
        # Rename file
        print("filename before:",filename)
        filename = self.deleteInvalidCharactersFromFilename(filename)
        print("filename after:",filename)
        
        # Download the video
        streamVideo.download(output_path="", filename=filename)
        button.setText("Download completed!")
        
    
        

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
