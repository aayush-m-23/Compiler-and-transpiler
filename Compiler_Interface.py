import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel,
    QFileDialog, QComboBox, QMessageBox, QFrame
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt
import os
from interpreter import run_compiler
from transpiler_backend import transpile_to_python, transpile_to_cpp, transpile_to_c, transpile_to_java


class TranspilerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Transpiler")
        self.resize(1200, 750)
        self.set_elegant_theme()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        header = QLabel("Code Transpiler")
        header.setStyleSheet("color: #E0E0E0; font-size: 30px; font-weight: 700;")
        subheader = QLabel("Transpile your code seamlessly between multiple languages")
        subheader.setStyleSheet("color: #A0A0A0; font-size: 14px;")
        main_layout.addWidget(header)
        main_layout.addWidget(subheader)

        lang_layout = QHBoxLayout()
        lang_label = QLabel("Select Language:")
        lang_label.setStyleSheet("color: #E0E0E0; font-size: 14px; font-weight: 600;")
        self.language_selector = QComboBox()
        self.language_selector.addItems(["Select Language", "Python", "Java", "C", "C++"])
        self.language_selector.setStyleSheet("""
            QComboBox {
                padding: 8px 14px;
                background-color: #2D2D2D;
                color: #E0E0E0;
                border-radius: 6px;
                font-size: 14px;
            }
            QComboBox:hover {
                background-color: #3A3A3A;
            }
            QComboBox:focus {
                border: 2px solid #4CAF50;
            }
        """)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.language_selector)
        lang_layout.addStretch()
        main_layout.addLayout(lang_layout)

        self.tips_box = QLabel("💡 Select a language to get code tips and hints here.")
        self.tips_box.setStyleSheet("""
            color: #B0B0B0;
            background-color: #222222;
            border-radius: 6px;
            padding: 10px 12px;
            font-size: 12px;
            font-style: italic;
        """)
        main_layout.addWidget(self.tips_box)

        editor_layout = QHBoxLayout()

        input_layout = QVBoxLayout()
        input_label = QLabel("Source Code")
        input_label.setStyleSheet("color: #E0E0E0; font-size: 16px; font-weight: 600;")
        self.input_editor = QTextEdit()
        self.input_editor.setFont(QFont("Consolas", 11))
        self.input_editor.setStyleSheet("background-color: #1B1B1B; color: #FFFFFF; border-radius: 8px; padding: 10px;")
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_editor)

        input_buttons = QHBoxLayout()
        self.add_button("Transpile", self.transpile_code, "#00BFA6", input_buttons)
        self.add_button("Clear Input", self.clear_input, "#D32F2F", input_buttons)
        self.add_button("Load File", self.load_file, "#1976D2", input_buttons)
        input_layout.addLayout(input_buttons)
        editor_layout.addLayout(input_layout)

        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setStyleSheet("color: #444444;")
        editor_layout.addWidget(divider)

        output_layout = QVBoxLayout()
        outputs_side_by_side = QHBoxLayout()

        transpiled_layout = QVBoxLayout()
        output_label = QLabel("Transpiled Output")
        output_label.setStyleSheet("color: #E0E0E0; font-size: 16px; font-weight: 600;")
        self.output_editor = QTextEdit()
        self.output_editor.setFont(QFont("Consolas", 11))
        self.output_editor.setReadOnly(True)
        self.output_editor.setStyleSheet("background-color: #1B1B1B; color: #A0FFA0; border-radius: 8px; padding: 10px;")
        transpiled_layout.addWidget(output_label)
        transpiled_layout.addWidget(self.output_editor)

        outputs_side_by_side.addLayout(transpiled_layout)

        compiled_layout = QVBoxLayout()
        compiled_label = QLabel("Compiled Output")
        compiled_label.setStyleSheet("color: #E0E0E0; font-size: 16px; font-weight: 600;")
        self.compiled_output = QTextEdit()
        self.compiled_output.setFont(QFont("Consolas", 11))
        self.compiled_output.setReadOnly(True)
        self.compiled_output.setStyleSheet("background-color: #1B1B1B; color: #FFFF99; border-radius: 8px; padding: 10px;")
        compiled_layout.addWidget(compiled_label)
        compiled_layout.addWidget(self.compiled_output)

        outputs_side_by_side.addLayout(compiled_layout)
        output_layout.addLayout(outputs_side_by_side)

        output_buttons = QHBoxLayout()
        self.add_button("Clear Output", self.clear_output, "#C62828", output_buttons)
        self.add_button("Save Output", self.save_output, "#F9A825", output_buttons)
        self.add_button("Compile and Run", self.compile_and_run, "#283593", output_buttons)
        output_layout.addLayout(output_buttons)

        editor_layout.addLayout(output_layout)
        main_layout.addLayout(editor_layout)
        self.setLayout(main_layout)

    def set_elegant_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                font-weight: 600;
                font-size: 14px;
                border-radius: 6px;
            }
        """)
