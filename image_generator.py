import sys
import requests
import base64
import time
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QScrollArea, QMessageBox, QProgressBar,
    QFileDialog, QComboBox, QFrame, QListView, QDialog, QLineEdit
)
from PyQt5.QtGui import QPixmap, QImage, QIcon, QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize


class ArrowIcon(QIcon):
    def __init__(self, color="#00ff9d", size=28):
        super().__init__()
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(color), 3.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        
        w, h = size, size
        center_x, center_y = w // 2, h // 2
        
        painter.drawLine(center_x - 8, center_y, center_x + 8, center_y)
        painter.drawLine(center_x + 8, center_y, center_x + 2, center_y - 6)
        painter.drawLine(center_x + 8, center_y, center_x + 2, center_y + 6)
        
        painter.end()
        
        self.addPixmap(pixmap)


class ImageIcon(QIcon):
    def __init__(self, color="#6c757d", size=28):
        super().__init__()
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(color), 2.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        
        w, h = size, size
        margin = 3
        
        body_w = w - 2 * margin
        body_h = h - 2 * margin - 6
        
        painter.drawRect(margin, margin + 6, body_w, body_h)
        
        lens_cx = margin + body_w // 2
        lens_cy = margin + 6 + body_h // 2
        lens_r = min(body_w, body_h) // 2 - 2
        painter.drawEllipse(lens_cx - lens_r, lens_cy - lens_r, lens_r * 2, lens_r * 2)
        
        inner_r = lens_r // 2
        painter.drawEllipse(lens_cx - inner_r, lens_cy - inner_r, inner_r * 2, inner_r * 2)
        
        flash_w = 6
        flash_h = 4
        painter.drawRect(margin + 4, margin, flash_w, flash_h)
        
        painter.end()
        
        self.addPixmap(pixmap)


class MoonIcon(QIcon):
    def __init__(self, color="#e0e0e0", size=24):
        super().__init__()
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(color), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(QColor(color))
        
        w, h = size, size
        cx, cy = w // 2, h // 2
        r = min(w, h) // 2 - 4
        
        painter.drawArc(cx - r, cy - r, r * 2, r * 2, 45 * 16, 270 * 16)
        
        painter.end()
        
        self.addPixmap(pixmap)


class SunIcon(QIcon):
    def __init__(self, color="#f0c040", size=24):
        super().__init__()
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(color), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(QColor(color))
        
        w, h = size, size
        cx, cy = w // 2, h // 2
        r = min(w, h) // 2 - 6
        
        painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)
        
        rays = 8
        for i in range(rays):
            angle = i * (360 / rays)
            inner_r = r + 4
            outer_r = inner_r + 6
            painter.drawLine(
                int(cx + inner_r * (3.14159 * angle / 180)),
                int(cy + inner_r * (3.14159 * (angle + 90) / 180)),
                int(cx + outer_r * (3.14159 * angle / 180)),
                int(cy + outer_r * (3.14159 * (angle + 90) / 180))
            )
        
        painter.end()
        
        self.addPixmap(pixmap)


class SettingsIcon(QIcon):
    def __init__(self, color="#8a8a9e", size=24):
        super().__init__()
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(color), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        
        w, h = size, size
        cx, cy = w // 2, h // 2
        outer_r = min(w, h) // 2 - 2
        inner_r = outer_r // 2
        
        painter.drawEllipse(cx - outer_r, cy - outer_r, outer_r * 2, outer_r * 2)
        
        teeth = 12
        for i in range(teeth):
            angle = i * (360 / teeth)
            x1 = int(cx + outer_r * (3.14159 * angle / 180))
            y1 = int(cy + outer_r * (3.14159 * (angle + 90) / 180))
            x2 = int(cx + (outer_r + 4) * (3.14159 * angle / 180))
            y2 = int(cy + (outer_r + 4) * (3.14159 * (angle + 90) / 180))
            painter.drawLine(x1, y1, x2, y2)
        
        painter.drawEllipse(cx - inner_r, cy - inner_r, inner_r * 2, inner_r * 2)
        
        painter.end()
        
        self.addPixmap(pixmap)


THEMES = {
    "dark": {
        "bg_main": "#1e1e2e",
        "bg_card": "#2d2d3f",
        "bg_input": "#1e1e2e",
        "text_main": "#ffffff",
        "text_secondary": "#8a8a9e",
        "text_placeholder": "#5a5a6e",
        "text_disabled": "#5a5a6e",
        "border": "#3d3d4f",
        "border_hover": "#4a4a5e",
        "border_focus": "#00ff9d",
        "accent": "#00ff9d",
        "accent_hover": "#00e68a",
        "accent_pressed": "#00cc77",
        "scrollbar_bg": "#2d2d3f",
        "scrollbar_handle": "#4a4a5e",
        "scrollbar_handle_hover": "#5a5a6e",
        "error": "#ff6b6b",
        "error_bg": "#3f2d2d",
    },
    "light": {
        "bg_main": "#f0f4f8",
        "bg_card": "#f8fafc",
        "bg_input": "#f1f5f9",
        "text_main": "#1e1e2e",
        "text_secondary": "#5a5a6e",
        "text_placeholder": "#8a8a9e",
        "text_disabled": "#8a8a9e",
        "border": "#d1d5db",
        "border_hover": "#9ca3af",
        "border_focus": "#00c88a",
        "accent": "#00c88a",
        "accent_hover": "#00b87a",
        "accent_pressed": "#00a86a",
        "scrollbar_bg": "#e5e7eb",
        "scrollbar_handle": "#d1d5db",
        "scrollbar_handle_hover": "#9ca3af",
        "error": "#ff5b5b",
        "error_bg": "#fef2f2",
    }
}

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "api_url": "https://token.ithinkai.cn/",
    "api_key": "sk-MSLn9CSxOObm0GKmNjTtQN4j4OzbwCcyBgDTDo0Td3QbmUWA",
    "save_path": os.path.expanduser("~/Pictures/AI Images")
}


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                return {**DEFAULT_CONFIG, **config}
        except:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False


class ImageGeneratorWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, prompt, image_path=None, size="1024x1024", config=None):
        super().__init__()
        self.prompt = prompt
        self.image_path = image_path
        self.size = size
        if config is None:
            config = DEFAULT_CONFIG
        self.baseurl = config.get("api_url", DEFAULT_CONFIG["api_url"])
        self.apikey = config.get("api_key", DEFAULT_CONFIG["api_key"])
        self.max_retries = 3
        self.connect_timeout = 30
        self.read_timeout = 180

    def run(self):
        self.progress.emit(25)
        
        url = f"{self.baseurl}/v1/images/generations"
        payload = {
            "model": "gpt-image-2",
            "prompt": self.prompt,
            "n": 1,
            "size": self.size,
            "response_format": "b64_json"
        }
        
        if self.image_path:
            with open(self.image_path, "rb") as f:
                image_data = f.read()
            image_b64 = base64.b64encode(image_data).decode('utf-8')
            payload["image"] = image_b64

        headers = {
            "Authorization": f"Bearer {self.apikey}",
            "Content-Type": "application/json"
        }

        response = None
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url, 
                    headers=headers, 
                    json=payload, 
                    timeout=(self.connect_timeout, self.read_timeout), 
                    verify=False
                )
                self.progress.emit(75)
                response.raise_for_status()
                
                result = response.json()
                images = []
                if isinstance(result, dict) and "data" in result:
                    for item in result.get("data", []):
                        if isinstance(item, dict) and "b64_json" in item:
                            b64_data = item["b64_json"]
                            if b64_data.startswith("data:image/"):
                                b64_data = b64_data.split(",", 1)[-1]
                            image_data = base64.b64decode(b64_data)
                            images.append(image_data)
                
                self.progress.emit(100)
                self.finished.emit(images)
                return
            except requests.exceptions.RequestException as e:
                error_msg = f"请求失败 (尝试 {attempt + 1}/{self.max_retries}): {str(e)}"
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                
                if response is not None:
                    try:
                        err_json = response.json()
                        if "error" in err_json:
                            error_msg = err_json["error"].get("message", error_msg)
                    except:
                        pass
                
                if "insufficient_quota" in error_msg.lower() or "429" in error_msg:
                    error_msg = "API配额不足，请稍后再试或更换API密钥"
                elif "timeout" in error_msg.lower():
                    error_msg = "请求超时，请检查网络连接或稍后重试"
                elif self.image_path and "504" in error_msg:
                    error_msg = "图生图功能暂不可用，请尝试使用文生图功能"
                self.error.emit(error_msg)
                return


class ImageGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Image Generator")
        self.setGeometry(100, 100, 1000, 800)
        self.image_data = None
        self.input_image_path = None
        self.current_theme = "dark"
        self.config = load_config()
        self.init_ui()

    def init_ui(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.header_frame = QFrame()
        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.logo_label = QLabel("🎨 AI Image Generator")
        self.header_layout.addWidget(self.logo_label)
        self.header_layout.addStretch()
        
        self.settings_btn = QPushButton()
        self.settings_btn.clicked.connect(self.open_settings)
        self.header_layout.addWidget(self.settings_btn)
        
        self.theme_btn = QPushButton()
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.header_layout.addWidget(self.theme_btn)
        
        self.status_label = QLabel("Ready")
        self.header_layout.addWidget(self.status_label)
        
        self.layout.addWidget(self.header_frame)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(24, 20, 24, 20)
        self.scroll_layout.setSpacing(20)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        self.input_frame = QFrame()
        self.input_layout = QVBoxLayout(self.input_frame)
        self.input_layout.setContentsMargins(0, 0, 0, 0)
        self.input_layout.setSpacing(12)

        self.top_input_layout = QHBoxLayout()
        self.top_input_layout.setSpacing(12)

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("输入图片描述...")
        self.top_input_layout.addWidget(self.input_box)

        self.size_combo = QComboBox()
        self.size_options = {
            "16:9 宽屏": "1024x576",
            "1:1 正方形": "1024x1024",
            "9:16 竖屏": "576x1024",
            "4:3 标准": "1024x768",
            "3:4 竖版": "768x1024",
            "21:9 超宽": "1024x438",
        }
        self.size_combo.addItems(self.size_options.keys())
        self.size_combo.setMinimumWidth(100)
        self.size_combo_view = QListView()
        self.size_combo_view.setMinimumWidth(120)
        self.size_combo.setView(self.size_combo_view)
        self.top_input_layout.addWidget(self.size_combo)

        self.clear_btn = QPushButton("✕")
        self.clear_btn.clicked.connect(self.clear_context)
        self.top_input_layout.addWidget(self.clear_btn)

        self.upload_btn = QPushButton()
        self.upload_btn.clicked.connect(self.upload_image)
        self.top_input_layout.addWidget(self.upload_btn)

        self.generate_btn = QPushButton()
        self.generate_btn.clicked.connect(self.generate_image)
        self.top_input_layout.addWidget(self.generate_btn)

        self.input_layout.addLayout(self.top_input_layout)

        self.image_preview_frame = QFrame()
        self.image_preview_frame.setFixedHeight(80)
        preview_layout = QHBoxLayout(self.image_preview_frame)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(8)

        self.image_label = QLabel()
        self.image_label.setFixedSize(64, 64)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setText("")
        
        self.image_info_label = QLabel("点击图片图标上传图片（用于图生图）")
        self.image_info_label.setAlignment(Qt.AlignVCenter)

        self.remove_image_btn = QPushButton("×")
        self.remove_image_btn.clicked.connect(self.remove_image)
        self.remove_image_btn.setVisible(False)

        preview_layout.addWidget(self.image_label)
        preview_layout.addWidget(self.image_info_label)
        preview_layout.addStretch()
        preview_layout.addWidget(self.remove_image_btn)

        self.input_layout.addWidget(self.image_preview_frame)
        self.layout.addWidget(self.input_frame)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.input_layout.addWidget(self.progress_bar)

        self.apply_theme(self.current_theme)
        self.show_welcome()

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        colors = THEMES[theme_name]

        self.main_widget.setStyleSheet(f"background-color: {colors['bg_main']};")
        self.scroll_content.setStyleSheet(f"background-color: {colors['bg_main']};")

        self.header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {colors['bg_card']};
                padding: 16px 24px;
            }}
        """)
        
        self.logo_label.setStyleSheet(f"""
            font-size: 18px; 
            font-weight: bold; 
            color: {colors['text_main']};
        """)
        
        self.status_label.setStyleSheet(f"""
            font-size: 13px; 
            color: {colors['accent']};
        """)
        
        icon_color = colors['text_secondary']
        self.settings_btn.setIcon(SettingsIcon(colors['text_secondary']))
        self.settings_btn.setIconSize(QSize(20, 20))
        self.settings_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                padding: 8px;
                min-width: 40px;
            }}
            QPushButton:hover {{
                background-color: {colors['border']};
                border-radius: 8px;
            }}
        """)
        
        self.theme_btn.setIcon(MoonIcon(icon_color) if theme_name == "dark" else SunIcon("#f0c040"))
        self.theme_btn.setIconSize(QSize(20, 20))
        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                padding: 8px;
                min-width: 40px;
            }}
            QPushButton:hover {{
                background-color: {colors['border']};
                border-radius: 8px;
            }}
        """)

        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {colors['bg_main']};
                border: none;
            }}
            QScrollBar:vertical {{
                width: 0px;
                background-color: transparent;
            }}
            QScrollBar::handle:vertical {{
                background-color: transparent;
                border-radius: 0px;
            }}
            QScrollBar:horizontal {{
                height: 0px;
                background-color: transparent;
            }}
            QScrollBar::handle:horizontal {{
                background-color: transparent;
                border-radius: 0px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                height: 0px;
                width: 0px;
            }}
        """)

        self.input_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {colors['bg_card']};
                border-top: 1px solid {colors['border']};
                padding: 12px 24px;
            }}
        """)

        self.input_box.setStyleSheet(f"""
            QTextEdit {{
                background-color: {colors['bg_input']};
                color: {colors['text_main']};
                border: 1px solid {colors['border']};
                border-radius: 12px;
                padding: 12px 16px;
                font-size: 14px;
                min-height: 44px;
                max-height: 120px;
            }}
            QTextEdit:hover {{
                border-color: {colors['border_hover']};
            }}
            QTextEdit:focus {{
                border-color: {colors['border_focus']};
                outline: none;
            }}
            QTextEdit::placeholder {{
                color: {colors['text_placeholder']};
            }}
        """)

        self.size_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {colors['bg_input']};
                color: {colors['text_main']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                min-width: 100px;
            }}
            QComboBox:hover {{
                border-color: {colors['border_hover']};
            }}
            QComboBox:focus {{
                border-color: {colors['border_focus']};
                outline: none;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 24px;
            }}
            QComboBox::down-arrow {{
                image: none;
            }}
        """)
        self.size_combo_view.setStyleSheet(f"""
            QListView {{
                background-color: {colors['bg_card']};
                color: {colors['text_main']};
                selection-background-color: {colors['accent']};
                selection-color: {colors['bg_main']};
                border: 1px solid {colors['border']};
                outline: none;
            }}
            QListView::item {{
                background-color: {colors['bg_card']};
                color: {colors['text_main']};
                padding: 6px 12px;
            }}
            QListView::item:selected {{
                background-color: {colors['accent']};
                color: {colors['bg_main']};
            }}
            QListView::item:hover {{
                background-color: {colors['border']};
                color: {colors['text_main']};
            }}
        """)

        self.upload_btn.setIcon(ImageIcon(colors['text_secondary']))
        self.upload_btn.setIconSize(QSize(24, 24))
        self.upload_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['bg_input']};
                color: {colors['text_main']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 8px;
                min-width: 44px;
            }}
            QPushButton:hover {{
                border-color: {colors['border_hover']};
                background-color: {colors['border']};
            }}
            QPushButton:pressed {{
                background-color: {colors['accent']};
                border-color: {colors['accent']};
            }}
            QPushButton:disabled {{
                opacity: 0.5;
            }}
        """)

        self.clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['bg_input']};
                color: {colors['text_secondary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 8px;
                min-width: 36px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                border-color: {colors['error']};
                color: {colors['error']};
                background-color: {colors['bg_input']};
            }}
            QPushButton:pressed {{
                background-color: {colors['error']};
                color: white;
                border-color: {colors['error']};
            }}
        """)

        self.generate_btn.setIcon(ArrowIcon(colors['bg_main']))
        self.generate_btn.setIconSize(QSize(24, 24))
        self.generate_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['accent']};
                color: {colors['bg_main']};
                border: none;
                border-radius: 8px;
                padding: 8px;
                min-width: 44px;
            }}
            QPushButton:hover {{
                background-color: {colors['accent_hover']};
            }}
            QPushButton:pressed {{
                background-color: {colors['accent_pressed']};
            }}
            QPushButton:disabled {{
                background-color: {colors['border']};
                opacity: 0.7;
            }}
        """)

        self.image_preview_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {colors['bg_input']};
                border: 1px dashed {colors['border']};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        
        self.image_label.setStyleSheet(f"border-radius: 4px;")
        
        self.image_info_label.setStyleSheet(f"""
            font-size: 12px; 
            color: {colors['text_placeholder']};
        """)

        self.remove_image_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {colors['text_secondary']};
                border: none;
                font-size: 18px;
                padding: 0 8px;
            }}
            QPushButton:hover {{
                color: {colors['error']};
            }}
        """)

        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {colors['bg_input']};
                border: none;
                border-radius: 4px;
                height: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {colors['accent']};
                border-radius: 4px;
            }}
        """)

        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, QFrame):
                    self.apply_frame_theme(widget, colors)

    def apply_frame_theme(self, frame, colors):
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {colors['bg_card']};
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        for i in range(frame.layout().count()):
            item = frame.layout().itemAt(i)
            if item.widget():
                child = item.widget()
                if isinstance(child, QLabel):
                    child.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {colors['text_main']};")
                elif isinstance(child, QHBoxLayout):
                    for j in range(child.count()):
                        btn_item = child.itemAt(j)
                        if btn_item.widget() and isinstance(btn_item.widget(), QPushButton):
                            btn = btn_item.widget()
                            if btn.text() == "下载原图":
                                btn.setStyleSheet(f"""
                                    QPushButton {{
                                        background-color: {colors['accent']};
                                        color: {colors['bg_main']};
                                        padding: 8px 24px;
                                        font-size: 13px;
                                        font-weight: bold;
                                        border: none;
                                        border-radius: 8px;
                                    }}
                                    QPushButton:hover {{
                                        background-color: {colors['accent_hover']};
                                    }}
                                    QPushButton:pressed {{
                                        background-color: {colors['accent_pressed']};
                                    }}
                                """)
                            elif btn.text() == "重新生成":
                                btn.setStyleSheet(f"""
                                    QPushButton {{
                                        background-color: transparent;
                                        color: {colors['text_secondary']};
                                        padding: 8px 24px;
                                        font-size: 13px;
                                        border: 1px solid {colors['border']};
                                        border-radius: 8px;
                                    }}
                                    QPushButton:hover {{
                                        border-color: {colors['border_hover']};
                                        color: {colors['text_main']};
                                    }}
                                """)

    def toggle_theme(self):
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(new_theme)

    def show_welcome(self):
        colors = THEMES[self.current_theme]
        welcome_frame = QFrame()
        welcome_frame.is_welcome = True
        welcome_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {colors['bg_card']};
                border-radius: 16px;
                padding: 40px;
            }}
        """)
        welcome_layout = QVBoxLayout(welcome_frame)
        welcome_layout.setAlignment(Qt.AlignCenter)
        welcome_layout.setSpacing(16)

        logo_label = QLabel("🎨")
        logo_label.setStyleSheet("font-size: 48px;")
        logo_label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(logo_label)

        title_label = QLabel("AI Image Generator")
        title_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {colors['text_main']};")
        title_label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(title_label)

        desc_label = QLabel("输入描述即可生成精美图片\n也可以上传图片进行图生图")
        desc_label.setStyleSheet(f"font-size: 14px; color: {colors['text_secondary']};")
        desc_label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(desc_label)

        self.scroll_layout.addWidget(welcome_frame)
        self.scroll_layout.addStretch()

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.input_image_path = file_path
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.image_label.setText("")
            self.image_info_label.setText(file_path.split("/")[-1].split("\\")[-1])
            self.remove_image_btn.setVisible(True)

    def remove_image(self):
        self.input_image_path = None
        self.image_label.clear()
        self.image_label.setText("")
        self.image_info_label.setText("点击图片图标上传图片（用于图生图）")
        self.remove_image_btn.setVisible(False)

    def generate_image(self):
        prompt = self.input_box.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "提示", "请输入图片描述")
            return

        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'is_welcome') and widget.is_welcome:
                widget.deleteLater()

        selected_size_name = self.size_combo.currentText()
        selected_size = self.size_options[selected_size_name]
        self.worker = ImageGeneratorWorker(prompt, self.input_image_path, selected_size, self.config)
        self.worker.finished.connect(self.on_image_generated)
        self.worker.error.connect(self.on_error)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.start()

    def on_image_generated(self, images):
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)

        for i in reversed(range(self.scroll_layout.count())):
            item = self.scroll_layout.itemAt(i)
            if item and item.spacerItem():
                self.scroll_layout.removeItem(item)
                break

        if images:
            self.image_data = images[0]
            image = QImage.fromData(self.image_data)
            pixmap = QPixmap.fromImage(image)

            max_width = 800
            max_height = 600
            pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            colors = THEMES[self.current_theme]
            img_frame = QFrame()
            img_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {colors['bg_card']};
                    border-radius: 12px;
                    padding: 16px;
                }}
            """)
            img_layout = QVBoxLayout(img_frame)
            img_layout.setContentsMargins(0, 0, 0, 0)
            img_layout.setSpacing(12)

            img_label = QLabel()
            img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignCenter)
            img_layout.addWidget(img_label)

            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(8)
            btn_layout.setAlignment(Qt.AlignCenter)

            download_btn = QPushButton("下载原图")
            download_btn.clicked.connect(self.download_image)
            download_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {colors['accent']};
                    color: {colors['bg_main']};
                    padding: 8px 24px;
                    font-size: 13px;
                    font-weight: bold;
                    border: none;
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    background-color: {colors['accent_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {colors['accent_pressed']};
                }}
            """)
            btn_layout.addWidget(download_btn)

            regenerate_btn = QPushButton("重新生成")
            regenerate_btn.clicked.connect(self.generate_image)
            regenerate_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {colors['text_secondary']};
                    padding: 8px 24px;
                    font-size: 13px;
                    border: 1px solid {colors['border']};
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    border-color: {colors['border_hover']};
                    color: {colors['text_main']};
                }}
            """)
            btn_layout.addWidget(regenerate_btn)

            img_layout.addLayout(btn_layout)
            self.scroll_layout.addWidget(img_frame)
        else:
            colors = THEMES[self.current_theme]
            error_frame = QFrame()
            error_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {colors['error_bg']};
                    border-radius: 12px;
                    padding: 20px;
                }}
            """)
            error_label = QLabel("未生成图片")
            error_label.setStyleSheet(f"font-size: 14px; color: {colors['error']};")
            error_label.setAlignment(Qt.AlignCenter)
            error_frame.setLayout(QVBoxLayout())
            error_frame.layout().addWidget(error_label)
            self.scroll_layout.addWidget(error_frame)

        self.scroll_layout.addStretch()

    def on_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)
        QMessageBox.critical(self, "错误", error_msg)

    def clear_context(self):
        self.input_box.clear()
        self.image_data = None
        self.remove_image()
        for i in reversed(range(self.scroll_layout.count())):
            item = self.scroll_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        self.show_welcome()

    def download_image(self):
        if self.image_data:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"generated_image_{timestamp}.png"
            save_path = self.config.get("save_path", os.path.expanduser("~/Pictures/AI Images"))
            if not os.path.exists(save_path):
                os.makedirs(save_path, exist_ok=True)
            full_path = os.path.join(save_path, filename)
            with open(full_path, "wb") as f:
                f.write(self.image_data)
            QMessageBox.information(self, "成功", f"图片已保存为: {full_path}")

    def open_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("设置")
        dialog.setFixedSize(400, 320)
        dialog.setModal(True)
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {THEMES[self.current_theme]['bg_main']};
            }}
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        colors = THEMES[self.current_theme]

        api_url_label = QLabel("API 地址")
        api_url_label.setStyleSheet(f"font-size: 13px; color: {colors['text_secondary']};")
        layout.addWidget(api_url_label)
        
        self.api_url_input = QLineEdit()
        self.api_url_input.setText(self.config.get("api_url", ""))
        self.api_url_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {colors['bg_input']};
                color: {colors['text_main']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
            }}
            QLineEdit:hover {{
                border-color: {colors['border_hover']};
            }}
            QLineEdit:focus {{
                border-color: {colors['border_focus']};
                outline: none;
            }}
        """)
        layout.addWidget(self.api_url_input)

        api_key_label = QLabel("API Key")
        api_key_label.setStyleSheet(f"font-size: 13px; color: {colors['text_secondary']};")
        layout.addWidget(api_key_label)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setText(self.config.get("api_key", ""))
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {colors['bg_input']};
                color: {colors['text_main']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
            }}
            QLineEdit:hover {{
                border-color: {colors['border_hover']};
            }}
            QLineEdit:focus {{
                border-color: {colors['border_focus']};
                outline: none;
            }}
        """)
        layout.addWidget(self.api_key_input)

        save_path_label = QLabel("图片保存路径")
        save_path_label.setStyleSheet(f"font-size: 13px; color: {colors['text_secondary']};")
        layout.addWidget(save_path_label)

        save_path_layout = QHBoxLayout()
        save_path_layout.setSpacing(8)
        
        self.save_path_input = QLineEdit()
        self.save_path_input.setText(self.config.get("save_path", ""))
        self.save_path_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {colors['bg_input']};
                color: {colors['text_main']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
            }}
            QLineEdit:hover {{
                border-color: {colors['border_hover']};
            }}
            QLineEdit:focus {{
                border-color: {colors['border_focus']};
                outline: none;
            }}
        """)
        save_path_layout.addWidget(self.save_path_input)

        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self.browse_save_path)
        browse_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['bg_input']};
                color: {colors['text_main']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                border-color: {colors['border_hover']};
                background-color: {colors['border']};
            }}
        """)
        save_path_layout.addWidget(browse_btn)
        
        layout.addLayout(save_path_layout)

        layout.addStretch()

        save_btn = QPushButton("保存")
        save_btn.clicked.connect(lambda: self.save_settings(dialog))
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['accent']};
                color: {colors['bg_main']};
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {colors['accent_hover']};
            }}
            QPushButton:pressed {{
                background-color: {colors['accent_pressed']};
            }}
        """)
        
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

        dialog.exec_()

    def browse_save_path(self):
        path = QFileDialog.getExistingDirectory(self, "选择保存路径")
        if path:
            self.save_path_input.setText(path)

    def save_settings(self, dialog):
        api_url = self.api_url_input.text().strip()
        api_key = self.api_key_input.text().strip()
        save_path = self.save_path_input.text().strip()

        if not api_url:
            QMessageBox.warning(self, "提示", "请输入 API 地址")
            return
        
        if not api_key:
            QMessageBox.warning(self, "提示", "请输入 API Key")
            return

        self.config["api_url"] = api_url
        self.config["api_key"] = api_key
        self.config["save_path"] = save_path

        if save_config(self.config):
            QMessageBox.information(self, "成功", "配置已保存")
            dialog.accept()
        else:
            QMessageBox.warning(self, "错误", "保存配置失败")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageGeneratorApp()
    window.show()
    sys.exit(app.exec_())