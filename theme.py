"""Neutral dark theme: near-black surfaces, soft grey text, one muted
slate-blue accent used sparingly for interactive/active states."""

BG_ROOT = "#141416"
BG_CARD = "#1b1c20"
BORDER = "#26272c"
TEXT_PRIMARY = "#ececed"
TEXT_SECONDARY = "#9a9aa0"
ACCENT = "#7c8fa6"
MUTED_RED = "#b5555f"

STYLE_SHEET = f"""
QWidget#MixerWindowRoot {{
    background: transparent;
}}

QFrame#RootCard {{
    background: {BG_ROOT};
    border-radius: 16px;
}}

QWidget#TitleBar {{
    background: transparent;
}}

QLabel#AppTitle {{
    color: {TEXT_PRIMARY};
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2px;
}}

QPushButton#TitleBtn {{
    background: transparent;
    color: {TEXT_SECONDARY};
    border: none;
    font-size: 15px;
    border-radius: 6px;
}}
QPushButton#TitleBtn:hover {{
    background: #26272c;
    color: {TEXT_PRIMARY};
}}
QPushButton#CloseBtn:hover {{
    background: {MUTED_RED};
    color: #ffffff;
}}

QFrame#SinkCard {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}

QLabel#SinkTitle {{
    color: {TEXT_PRIMARY};
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1px;
}}

QLabel#VolumeLabel {{
    color: {TEXT_SECONDARY};
    font-size: 11px;
}}

QLabel#AppLabel {{
    color: #c7c8cc;
    font-size: 12px;
}}

QPushButton#MuteButton {{
    background: transparent;
    color: {TEXT_SECONDARY};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 5px 14px;
    font-size: 11px;
}}
QPushButton#MuteButton:hover {{
    border-color: {ACCENT};
    color: {TEXT_PRIMARY};
}}
QPushButton#MuteButton:checked {{
    background: rgba(181, 85, 95, 0.15);
    border-color: {MUTED_RED};
    color: #e08a92;
}}

QSlider::groove:horizontal {{
    height: 4px;
    background: #2a2b30;
    border-radius: 2px;
}}
QSlider::sub-page:horizontal {{
    background: {ACCENT};
    border-radius: 2px;
}}
QSlider::add-page:horizontal {{
    background: #2a2b30;
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {TEXT_PRIMARY};
    width: 12px;
    height: 12px;
    margin: -5px 0;
    border-radius: 6px;
    border: 2px solid {ACCENT};
}}
QSlider::handle:horizontal:hover {{
    background: #ffffff;
}}

QComboBox {{
    background: #202126;
    color: #c7c8cc;
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 3px 8px;
    font-size: 11px;
}}
QComboBox:hover {{
    border-color: {ACCENT};
}}
QComboBox::drop-down {{
    border: none;
}}
QComboBox QAbstractItemView {{
    background: #1e1f23;
    color: {TEXT_PRIMARY};
    selection-background-color: #2a2b30;
    border: 1px solid {BORDER};
    outline: none;
}}

QListWidget {{
    background: transparent;
    border: none;
}}
QListWidget::item {{
    border-bottom: 1px solid #202126;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #2a2b30;
    border-radius: 3px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{
    background: #3a3b42;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""
