"""Main mixer window: one panel per managed sink, each with volume, mute,
and a live list of app streams that can be moved to another managed sink."""
from __future__ import annotations

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from mixer_backend import AudioMixerBackend

REFRESH_MS = 1500


class SinkPanel(QGroupBox):
    def __init__(self, sink_name: str, other_sink_names: list[str], on_volume, on_mute, on_move):
        super().__init__(sink_name)
        self.sink_name = sink_name
        self.other_sink_names = other_sink_names
        self.on_volume = on_volume
        self.on_mute = on_mute
        self.on_move = on_move
        self._suppress_volume_signal = False

        layout = QVBoxLayout(self)

        vol_row = QHBoxLayout()
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 150)
        self.slider.valueChanged.connect(self._slider_changed)
        self.vol_label = QLabel("--%")
        self.vol_label.setFixedWidth(40)
        self.mute_button = QPushButton("Mute")
        self.mute_button.setCheckable(True)
        self.mute_button.toggled.connect(lambda checked: self.on_mute(self.sink_name, checked))
        vol_row.addWidget(self.slider)
        vol_row.addWidget(self.vol_label)
        vol_row.addWidget(self.mute_button)
        layout.addLayout(vol_row)

        self.app_list = QListWidget()
        layout.addWidget(self.app_list)

    def _slider_changed(self, value: int):
        self.vol_label.setText(f"{value}%")
        if not self._suppress_volume_signal:
            self.on_volume(self.sink_name, value)

    def update_state(self, volume: int, muted: bool, apps: list[dict]):
        self._suppress_volume_signal = True
        if self.slider.value() != volume:
            self.slider.setValue(volume)
        self.vol_label.setText(f"{volume}%")
        self._suppress_volume_signal = False

        if self.mute_button.isChecked() != muted:
            self.mute_button.blockSignals(True)
            self.mute_button.setChecked(muted)
            self.mute_button.blockSignals(False)

        self.app_list.clear()
        for app in apps:
            item = QListWidgetItem()
            self.app_list.addItem(item)
            self.app_list.setItemWidget(item, self._build_app_row(app))

    def _build_app_row(self, app: dict) -> QWidget:
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(4, 2, 4, 2)
        row_layout.addWidget(QLabel(app["label"]))
        row_layout.addStretch()

        if self.other_sink_names:
            combo = QComboBox()
            combo.addItem("Move to...")
            combo.addItems(self.other_sink_names)
            combo.currentIndexChanged.connect(
                lambda idx, app_index=app["index"], combo=combo: self._move_selected(idx, app_index, combo)
            )
            row_layout.addWidget(combo)
        return row

    def _move_selected(self, idx: int, app_index: int, combo: QComboBox):
        if idx <= 0:
            return
        target = combo.itemText(idx)
        self.on_move(app_index, target)
        combo.setCurrentIndex(0)


class MixerWindow(QWidget):
    def __init__(self, backend: AudioMixerBackend):
        super().__init__()
        self.backend = backend
        self.setWindowTitle("Audio Mixer")
        self.resize(420, 500)

        layout = QVBoxLayout(self)
        self.panels: dict[str, SinkPanel] = {}
        for name in backend.sink_names:
            others = [n for n in backend.sink_names if n != name]
            panel = SinkPanel(name, others, self._set_volume, self._set_mute, self._move_app)
            self.panels[name] = panel
            layout.addWidget(panel)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(REFRESH_MS)
        self.refresh()

    def refresh(self):
        sinks = self.backend.get_sinks()
        apps_by_sink = self.backend.get_apps_by_sink()
        for sink in sinks:
            panel = self.panels.get(sink["name"])
            if panel is None:
                continue
            apps = apps_by_sink.get(sink["index"], [])
            panel.update_state(sink["volume"], sink["muted"], apps)

    def _set_volume(self, sink_name: str, percent: int):
        self.backend.set_volume(sink_name, percent)

    def _set_mute(self, sink_name: str, muted: bool):
        self.backend.set_mute(sink_name, muted)

    def _move_app(self, app_index: int, target_sink_name: str):
        self.backend.move_app(app_index, target_sink_name)
        self.refresh()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
