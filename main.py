import sys
import subprocess
import hashlib
import requests
import zipfile
import os
import qtawesome as qta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QWidget, QGridLayout, QMessageBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QFont
import ctypes
import socket

class LoaderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Centric Client')
        self.setGeometry(100, 100, 500, 200)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(self.get_stylesheet())
        self.current_version = '0.3'
        self.initUI()
        self._startPos = None

        self.create_folder_if_not_exists("C:\\Centric")
        self.download_files()
        self.check_for_updates(self.current_version)
        self.check_injectors()
        self.check_for_debugger()

    def create_folder_if_not_exists(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def download_and_unzip(self, url, target_folder):
        assets_folder = os.path.join(target_folder, url.split('/')[-1].split('.')[0])
        if os.path.exists(assets_folder):
            return
        filename = url.split('/')[-1]
        target_path = os.path.join(target_folder, filename)
        try:
            self.download_file(url, target_path)
            with zipfile.ZipFile(target_path, 'r') as zip_ref:
                zip_ref.extractall(target_folder)
            os.remove(target_path)
        except Exception as e:
            pass

    def download_file(self, url, target_path, timeout=60):
        try:
            response = requests.get(url, stream=True, timeout=timeout)
            with open(target_path, 'wb') as file:
                for data in response.iter_content(1024):
                    file.write(data)
        except Exception as e:
            pass

    def delete_files_except(self, directory, filename):
        for file in os.listdir(directory):
            if file != filename:
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    def download_file_if_not_exists(self, url, target_folder):
        filename = url.split('/')[-1]
        target_path = os.path.join(target_folder, filename)
        if not os.path.exists(target_path):
            self.download_file(url, target_path)

    def check_for_updates(self, current_version):
        try:
            url = 'ссылка'
            response = requests.get(url, params={'version': current_version})
            update_info = response.json()
            if update_info['update']:
                target_folder = "C:\\Centric\\"
                url = "ссылка"
                directory_to_clean = r"C:\Centric"
                filename = "client.jar"
                self.delete_files_except(directory_to_clean, filename)
                self.download_file_if_not_exists(url, target_folder)
                self.show_message("Обновление", "Клиент был обновлен до последней версии.")
        except Exception as e:
            pass

    def download_files(self):
        target_folder = "C:\\Centric\\"
        java_url = "ссылка"
        lib_url = "ссылка"

        self.download_and_unzip(java_url, target_folder)
        self.download_and_unzip(lib_url, target_folder)
        self.show_message("Готово!", "Приятной игры!")

    def check_injectors(self):
        if ctypes.windll.kernel32.IsDebuggerPresent():
            self.show_message("Ошибка", "Обнаружен отладчик.")
            sys.exit()

    def check_for_debugger(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("localhost", 0))
            s.listen(1)
            s.settimeout(5)
            s.accept()
            self.show_message("Ошибка", "Обнаружен сетевой отладчик.")
            sys.exit()
        except socket.timeout:
            pass

    def get_file_hash(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def initUI(self):
        main_layout = QGridLayout()

        self.title_label = QLabel("Мой отец крашдами")
        self.title_label.setFont(QFont("Arial", 30, QFont.Bold))
        self.title_label.setStyleSheet("color: #FFFFFF;")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label, 0, 0, 1, 2, Qt.AlignCenter)

        self.play_button = QPushButton()
        self.play_button.setIcon(qta.icon('fa.play'))
        self.play_button.setText('Start')
        self.play_button.setStyleSheet("border-radius: 15px; background-color: #28a745; color: white; padding: 15px 30px; font-size: 18px;")
        self.play_button.clicked.connect(self.play_game)
        main_layout.addWidget(self.play_button, 2, 0, Qt.AlignLeft)

        self.exit_button = QPushButton()
        self.exit_button.setIcon(qta.icon('fa.times'))
        self.exit_button.setText('Exit')
        self.exit_button.setStyleSheet("background-color: #dc3545; color: white; border: none; border-radius: 15px; padding: 15px 30px; font-size: 18px;")
        self.exit_button.clicked.connect(self.close)
        main_layout.addWidget(self.exit_button, 2, 1, Qt.AlignRight)
    
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.animate_button(self.play_button)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._startPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._startPos:
            self.move(event.globalPos() - self._startPos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._startPos = None
        event.accept()

    def animate_button(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(QRect(button.x(), button.y(), button.width(), button.height()))
        animation.setEndValue(QRect(button.x(), button.y() + 10, button.width(), button.height()))
        animation.setLoopCount(-1)
        animation.setEasingCurve(QEasingCurve.InOutBounce)
        animation.start()

    def play_game(self):
        command = [
            r"C:\Centric\java\bin\java.exe",
            "-noverify",
            "-Xmx4G",
            "-Djava.library.path=.\natives",
            "-cp",
            r"C:\Centric\client.jar;C:\Centric\libraries\*",
            "net.minecraft.client.main.Main",
            "--username", "huesos",
            "--password", "testexosware8",
            "--width", "854",
            "--height", "480",
            "--version", "Optifine 1.16.5",
            "--gameDir", r"C:\Centric\game",
            "--assetsDir", r"C:\Centric\game\assets",
            "--assetIndex", "1.16",
            "--uuid", "N/A",
            "--accessToken", "0",
            "--userType", "mojang"
        ]

        subprocess.run(command)
        self.show_message("Информация", "Игра успешно запущена!")

    def get_stylesheet(self):
        return """
        QWidget {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #1e1e1e, stop: 1 #3a3a3a);
            color: #F0F0F0;
            font-family: 'Arial', sans-serif;
        }
        QLabel {
            font-size: 30px;
            color: #61dafb;
            background: transparent;
            border-radius: 15px
        }
        QPushButton {
            background-color: #61dafb;
            color: #20232a;
            border: none;
            border-radius: 15px;
            padding: 10px 20px;
        }
        QPushButton:pressed {
            background-color: #4fa3b6;
        }
        """

    def show_message(self, title, message):
        QMessageBox.information(self, title, message, QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoaderWindow()
    window.show()
    sys.exit(app.exec_())
