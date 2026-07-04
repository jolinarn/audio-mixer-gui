#!/usr/bin/env python3
"""Entry point: tray icon + toggleable mixer window."""
import sys

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from mixer_backend import AudioMixerBackend
from mixer_window import MixerWindow


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    backend = AudioMixerBackend()
    window = MixerWindow(backend)

    icon = QIcon.fromTheme("audio-volume-high")
    tray = QSystemTrayIcon(icon, app)
    tray.setToolTip("Audio Mixer")

    def toggle_window():
        if window.isVisible():
            window.hide()
        else:
            window.show()
            window.raise_()
            window.activateWindow()

    menu = QMenu()
    show_action = QAction("Show/Hide")
    show_action.triggered.connect(toggle_window)
    quit_action = QAction("Quit")
    quit_action.triggered.connect(app.quit)
    menu.addAction(show_action)
    menu.addAction(quit_action)
    tray.setContextMenu(menu)

    def on_activated(reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            toggle_window()

    tray.activated.connect(on_activated)
    tray.show()
    window.show()

    exit_code = app.exec()
    backend.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
