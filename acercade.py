from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class AcercaDe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeuroMate - Acerca de")
        self.setGeometry(250, 250, 600, 500)
        self.setWindowIcon(QIcon("img/acerd.png"))

        self.setStyleSheet("""
            QWidget {
                background-color: #fdfaf6;
                color: #2e2e2e;
                font-family: 'Segoe UI';
            }
            QLabel#titulo {
                font-weight: bold;
                font-size: 28px;
                color: #1a3c73;
                margin-bottom: 30px;
            }
            QLabel#info_label {
                font-weight: bold;
                font-size: 16px;
                color: #1a3c73;
            }
            QLabel#info_value {
                font-size: 16px;
                color: #333;
            }
            QFrame#tabla {
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 12px;
                padding: 30px;
            }
            QPushButton {
                background-color: #3dbff3;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #63cdf9;
            }
        """)

        # Layout principal vertical
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

        # Título
        titulo = QLabel("Acerca de")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo)

        # Frame tipo tabla centrada
        frame_tabla = QFrame()
        frame_tabla.setObjectName("tabla")
        tabla_layout = QGridLayout()
        tabla_layout.setHorizontalSpacing(40)
        tabla_layout.setVerticalSpacing(15)
        frame_tabla.setLayout(tabla_layout)

        datos = [
            ("Autor:", "Ronny Arellano Urgiles"),
            ("Carrera:", "Ingeniería de Software"),
            ("Semestre:", "Sexto"),
            ("Año Académico:", "2025"),
            ("Profesor:", "Morales Torres Fabricio"),
            ("Materia:", "Modelos Matemáticos"),
        ]

        for i, (etiqueta, valor) in enumerate(datos):
            label_etiqueta = QLabel(etiqueta)
            label_etiqueta.setObjectName("info_label")
            label_valor = QLabel(valor)
            label_valor.setObjectName("info_value")

            tabla_layout.addWidget(label_etiqueta, i, 0, alignment=Qt.AlignRight)
            tabla_layout.addWidget(label_valor, i, 1, alignment=Qt.AlignLeft)

        main_layout.addWidget(frame_tabla)

        # Botón centrado
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_cerrar)

        main_layout.addLayout(btn_layout)
