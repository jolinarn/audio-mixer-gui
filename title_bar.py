"""Custom draggable title bar for the frameless window: title + minimize/close."""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class TitleBar(QWidget):
    def __init__(self, window, title: str = "AUDIO MIXER"):
        super().__init__()
        self.window = window
        self._drag_offset = None
        self.setObjectName("TitleBar")
        self.setFixedHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 8, 0)

        label = QLabel(title)
        label.setObjectName("AppTitle")
        layout.addWidget(label)
        layout.addStretch()

        min_btn = QPushButton("–")
        min_btn.setObjectName("TitleBtn")
        min_btn.setFixedSize(28, 28)
        min_btn.clicked.connect(self.window.showMinimized)

        close_btn = QPushButton("×")
        close_btn.setObjectName("CloseBtn")
        close_btn.setFixedSize(28, 28)
        close_btn.clicked.connect(self.window.hide)

        layout.addWidget(min_btn)
        layout.addWidget(close_btn)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_offset = event.globalPosition().toPoint() - self.window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_offset is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.window.move(event.globalPosition().toPoint() - self._drag_offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_offset = None
