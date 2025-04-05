import sys
import platform
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QLabel,
    QHBoxLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PyPDF2 import PdfMerger


class PDFMergerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Merger")
        self.setGeometry(100, 100, 650, 550)
        self.file_list = []

        self.layout = QVBoxLayout()

        self.instruction_label = QLabel("👆👇 Drag the files to adjust their order")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.instruction_label)

        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.layout.addWidget(self.list_widget)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add PDFs")
        self.add_button.clicked.connect(self.add_files)
        button_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(self.remove_button)

        self.merge_button = QPushButton("Merge PDFs")
        self.merge_button.clicked.connect(self.merge_pdfs)
        button_layout.addWidget(self.merge_button)

        self.layout.addLayout(button_layout)

        self.version_label = QLabel("Version 1.0.3")
        self.version_label.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.version_label)

        self.setLayout(self.layout)
        self.center_window()
        self.apply_system_theme()

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select PDF Files", "", "PDF Files (*.pdf)"
        )
        for file in files:
            if file not in self.file_list:
                self.file_list.append(file)
                self.list_widget.addItem(file)

    def remove_selected(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.file_list.remove(item.text())
            self.list_widget.takeItem(self.list_widget.row(item))

    def merge_pdfs(self):
        if self.list_widget.count() == 0:
            QMessageBox.critical(self, "Error", "No PDF files selected.")
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Merged PDF", "", "PDF Files (*.pdf)"
        )

        if not output_path:
            return

        merger = PdfMerger()
        for index in range(self.list_widget.count()):
            merger.append(self.list_widget.item(index).text())

        merger.write(output_path)
        merger.close()

        QMessageBox.information(self, "Success", "PDFs merged successfully!")

    def apply_system_theme(self):
        palette = QPalette()
        if platform.system() == "Darwin":
            import subprocess

            mode = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"], capture_output=True
            )
            is_dark = mode.returncode == 0 and "Dark" in mode.stdout.decode()
        elif platform.system() == "Windows":  # Windows
            import winreg

            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize",
                )
                is_dark = winreg.QueryValueEx(key, "AppsUseLightTheme")[0] == 0
            except Exception:
                is_dark = False
        else:
            is_dark = False

        if is_dark:
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(35, 35, 35))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.Highlight, QColor(142, 45, 197))
            palette.setColor(QPalette.HighlightedText, Qt.white)
            QApplication.instance().setPalette(palette)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec())
