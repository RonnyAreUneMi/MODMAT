from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class CalculadoraVectores(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora de Vectores Neuromate")
        self.setGeometry(100, 100, 600, 400)

        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f4;
                color: #333333;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 15px;
            }

            QLabel {
                font-weight: bold;
                margin: 10px 0 5px;
                color: #003366;
            }

            QLineEdit {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #ff0000;
                border-radius: 8px;
                padding: 8px;
                width: 150px;
            }

            QTextEdit {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #ff0000;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton {
                background-color: #003366;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
            }

            QPushButton:hover {
                background-color: #004c99;
            }

            QPushButton#salir_button {
                background-color: #ff0000;
                color: white;
            }

            QPushButton#salir_button:hover {
                background-color: #ff6666;
            }
        """)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.operacion_label = QLabel("Calculadora de Vectores Neuromate")
        self.layout.addWidget(self.operacion_label)

        input_layout = QHBoxLayout()
        self.layout.addLayout(input_layout)

        self.vector_a_label = QLabel("Vector A (x, y, z):")
        self.vector_a_input = QLineEdit()
        self.vector_a_input.setPlaceholderText("Ejemplo: (1, 2, 3)")

        self.vector_b_label = QLabel("Vector B (x, y, z):")
        self.vector_b_input = QLineEdit()
        self.vector_b_input.setPlaceholderText("Ejemplo: (4, 5, 6)")

        input_layout.addWidget(self.vector_a_label)
        input_layout.addWidget(self.vector_a_input)
        input_layout.addWidget(self.vector_b_label)
        input_layout.addWidget(self.vector_b_input)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.layout.addWidget(self.resultado)

        botones_layout = QGridLayout()
        self.layout.addLayout(botones_layout)

        operaciones = [
            ("Sumar", self.sumar_vectores),
            ("Restar", self.restar_vectores),
            ("Producto Punto", self.producto_punto),
            ("Producto Cruzado", self.producto_cruzado),
            ("Magnitud de A", self.magnitud),
        ]

        row, col = 0, 0
        for texto, funcion in operaciones:
            boton = QPushButton(texto)
            boton.clicked.connect(funcion)
            botones_layout.addWidget(boton, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        self.salir_button = QPushButton("Salir")
        self.salir_button.setObjectName("salir_button")
        self.salir_button.clicked.connect(self.salir)
        botones_layout.addWidget(self.salir_button, row, col)

    def validar_entrada(self, texto):
        try:
            texto = texto.strip("()")
            lista = [float(coord.strip()) for coord in texto.split(",")]
            if len(lista) == 3:
                return lista
            else:
                return None
        except ValueError:
            return None

    def sumar_vectores(self):
        a = self.vector_a_input.text()
        b = self.vector_b_input.text()

        a = self.validar_entrada(a)
        b = self.validar_entrada(b)

        if a and b:
            resultado = [a[i] + b[i] for i in range(3)]
            self.resultado.setText(f"Resultado de la suma: {tuple(resultado)}")
        else:
            self.resultado.setText("Error: Ingrese vectores válidos.")

    def restar_vectores(self):
        a = self.vector_a_input.text()
        b = self.vector_b_input.text()

        a = self.validar_entrada(a)
        b = self.validar_entrada(b)

        if a and b:
            resultado = [a[i] - b[i] for i in range(3)]
            self.resultado.setText(f"Resultado de la resta: {tuple(resultado)}")
        else:
            self.resultado.setText("Error: Ingrese vectores válidos.")

    def producto_punto(self):
        a = self.vector_a_input.text()
        b = self.vector_b_input.text()

        a = self.validar_entrada(a)
        b = self.validar_entrada(b)

        if a and b:
            resultado = sum([a[i] * b[i] for i in range(3)])
            self.resultado.setText(f"Resultado del producto punto: {resultado}")
        else:
            self.resultado.setText("Error: Ingrese vectores válidos.")

    def producto_cruzado(self):
        a = self.vector_a_input.text()
        b = self.vector_b_input.text()

        a = self.validar_entrada(a)
        b = self.validar_entrada(b)

        if a and b:
            resultado = [
                a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0],
            ]
            self.resultado.setText(f"Resultado del producto cruzado: {tuple(resultado)}")
        else:
            self.resultado.setText("Error: Ingrese vectores válidos.")

    def magnitud(self):
        a = self.vector_a_input.text()
        a = self.validar_entrada(a)

        if a:
            resultado = (sum([coord ** 2 for coord in a])) ** 0.5
            self.resultado.setText(f"Magnitud de A: {resultado}")
        else:
            self.resultado.setText("Error: Ingrese un vector válido.")

    def salir(self):
        from menu import MenuPrincipal
        self.menu = MenuPrincipal()
        self.menu.show()
        self.close()
