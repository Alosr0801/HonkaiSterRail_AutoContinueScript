import sys
import threading

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QProgressBar
import autoContinue  # 导入你的脚本模块
from PyQt6.QtGui import QIcon

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自动继续战斗（WIP）")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, 
                                        stop: 0 #1F1F1F, stop: 1 #2E2E2E);
            color: #FFFFFF;
            border-radius: 15px;
        """)

        # 创建布局
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 状态标签
        self.status_label = QLabel("点击下面的按钮运行脚本")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # 创建开始按钮
        self.start_button = QPushButton("运行脚本")
        self.start_button.setFixedHeight(40)
        self.start_button.clicked.connect(self.start_script)

        # 创建输出文本框
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        # 创建进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)

        layout.addWidget(self.start_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.output_text)
        self.setLayout(layout)

        # 设置按钮样式
        self.setup_button_animation()

    def setup_button_animation(self):
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D4; 
                color: white; 
                font-size: 16px; 
                border-radius: 10px; 
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #005BB5; 
                padding-left: 12px; 
                padding-top: 12px;
            }
            QPushButton:pressed {
                background-color: #004A8A; 
                padding-left: 8px; 
                padding-top: 8px;
            }
        """)

    def start_script(self):
        self.start_button.setEnabled(False)
        self.status_label.setText("脚本正在运行...")
        self.output_text.clear()
        self.progress_bar.setVisible(True)

        # 直接在主线程中调用
        self.run_script()

    def run_script(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_label.setText("脚本运行中...")

        try:
            output = autoContinue.main()  # 调用autoContinue的main函数
            if isinstance(output, str):
                self.output_text.setPlainText(output)  # 如果是错误信息
            else:
                self.output_text.setPlainText("\n".join(map(str, output)))  # 输出结果列表
        except Exception as e:
            self.output_text.setPlainText(f"运行出错: {e}")
        finally:
            self.start_button.setEnabled(True)
            self.progress_bar.setVisible(False)
            self.status_label.setText("脚本运行完毕")

if __name__ == "__main__":
    app = QApplication(sys.argv)
        # 设置窗口图标
    app.setWindowIcon(QIcon("icon.ico"))

    main_window = App()  # 替换为你的主窗口类
    main_window.show()

    sys.exit(app.exec())


