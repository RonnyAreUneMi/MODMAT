import sys
import numpy as np
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QSpinBox, QTextEdit, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QMessageBox,QGridLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal


class MatrixCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧮 Calculadora Visual de Matrices")
        self.setGeometry(100, 100, 1000, 720)
        self.setWindowIcon(QIcon("img/icon.png"))

        self.setStyleSheet("""
QWidget {
    background-color: #f9f9f9;
    color: #333;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}

QLabel {
    font-weight: bold;
    padding: 4px 6px;
}

QSpinBox, QComboBox {
    background-color: #ffffff;
    border: 2px solid #e53935;  /* rojo */
    padding: 6px 8px;
    border-radius: 6px;
    min-width: 60px;
}

QComboBox {
    min-width: 110px;
}

QPushButton {
    background-color: #003366;  /* azul marino */
    color: white;
    border: none;
    padding: 8px 16px;
    margin: 4px;
    border-radius: 6px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

QPushButton:hover {
    background-color: #002244;  /* más oscuro al pasar el mouse */
}

QPushButton#btn_exit {
    background-color: #e74c3c;
}

QPushButton#btn_exit:hover {
    background-color: #c0392b;
}

QTextEdit {
    background-color: #ffffff;
    border: 2px solid #e53935;  /* rojo */
    padding: 10px;
    border-radius: 8px;
    color: #2c3e50;
    min-height: 120px;
    font-size: 15px;
    font-family: 'Courier New', monospace;
}

QTableWidget {
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 8px;
    gridline-color: #d0d0d0;
}

QTableWidget::item {
    padding: 6px;
}

QHeaderView::section {
    background-color: #e0e0e0;
    color: #333;
    border: none;
    padding: 6px;
    font-weight: bold;
}

QHeaderView::section:horizontal {
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QHeaderView::section:vertical {
    border-top-left-radius: 6px;
    border-bottom-left-radius: 6px;
}
""")

        layout = QVBoxLayout()
        self.setLayout(layout)

        control_layout = QHBoxLayout()
        for label, spin in [("FILAS A:", "rows1"), ("COLUMNAS A:", "cols1"),
                            ("FILAS B:", "rows2"), ("COLUMNAS B:", "cols2")]:
            control_layout.addWidget(QLabel(label))
            setattr(self, spin, QSpinBox())
            getattr(self, spin).setValue(2)
            control_layout.addWidget(getattr(self, spin))

        self.combo_orden = QComboBox()
        self.combo_orden.addItems(["A ⭢ B", "B ⭢ A"])
        self.combo_orden.currentIndexChanged.connect(self.cambiar_orden)
        control_layout.addWidget(QLabel("Orden:"))
        control_layout.addWidget(self.combo_orden)

        self.btn_gen = QPushButton("Generar")
        self.btn_gen.clicked.connect(self.generar_tablas)
        self.btn_clear = QPushButton("Limpiar")
        self.btn_clear.clicked.connect(self.limpiar)
        self.btn_exit = QPushButton("Salir")
        self.btn_exit.setObjectName("btn_exit")
        self.btn_exit.clicked.connect(self.salir)

        for btn in [self.btn_gen, self.btn_clear, self.btn_exit]:
            control_layout.addWidget(btn)

        layout.addLayout(control_layout)

        self.matrices_layout = QHBoxLayout()
        layout.addLayout(self.matrices_layout)

        layout.addWidget(QLabel("Resultado:"))
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.operaciones_layout = QHBoxLayout()
        layout.addLayout(self.operaciones_layout)
        self.agregar_boton("Sumar", self.sumar)
        self.agregar_boton("Restar", self.restar)
        self.agregar_boton("Multiplicar", self.multiplicar)
        self.agregar_boton("Determinante", self.determinantes)
        self.agregar_boton("Inversas", self.inversas)
        # Agregar botón para abrir sistemas lineales
        self.agregar_boton("Sistemas Lineales", self.abrir_sistemas_lineales)

        self.generar_tablas()

    def agregar_boton(self, texto, funcion):
        btn = QPushButton(texto)
        btn.clicked.connect(funcion)
        self.operaciones_layout.addWidget(btn)

    def generar_tablas(self):
        for i in reversed(range(self.matrices_layout.count())):
            widget = self.matrices_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.tabla1 = QTableWidget(self.rows1.value(), self.cols1.value())
        self.tabla2 = QTableWidget(self.rows2.value(), self.cols2.value())
        for tabla in [self.tabla1, self.tabla2]:
            tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tabla.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.matrices_layout.addWidget(self.tabla1)
        self.matrices_layout.addWidget(self.tabla2)

    def leer_matriz(self, tabla):
        filas = tabla.rowCount()
        columnas = tabla.columnCount()
        matriz = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                item = tabla.item(i, j)
                try:
                    fila.append(float(item.text()) if item else 0.0)
                except:
                    raise ValueError(f"Error en la celda ({i+1}, {j+1}): Valor no válido.")
                tabla.setItem(i, j, QTableWidgetItem(str(fila[-1])))
            matriz.append(fila)
        return np.array(matriz)

    def mostrar_error(self, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error en la Operación")
        msg.setText(mensaje)
        msg.setInformativeText("Por favor, revisa los datos ingresados.")
        msg.exec_()

    def obtener_ordenadas(self):
        orden = self.combo_orden.currentText()
        a = self.leer_matriz(self.tabla1)
        b = self.leer_matriz(self.tabla2)
        return (a, b) if orden == "A ⭢ B" else (b, a)

    def format_result(self, resultado):
        if isinstance(resultado, np.ndarray):
            return f"<pre>{np.array2string(resultado, precision=2, suppress_small=True)}</pre>"
        elif isinstance(resultado, float):
            return str(int(resultado)) if resultado.is_integer() else str(round(resultado, 2))
        return str(resultado)

    def mostrar_resultado(self, resultado, titulo="Resultado"):
        html = f"<b>{titulo}:</b><br>{self.format_result(resultado)}"
        self.resultado.setHtml(html)

    def sumar(self):
        try:
            a, b = self.obtener_ordenadas()
            if a.shape != b.shape:
                raise ValueError("Las matrices deben tener las mismas dimensiones para sumar.")
            res = a + b
            self.mostrar_resultado(res, "Suma")
        except Exception as e:
            self.mostrar_error(str(e))

    def restar(self):
        try:
            a, b = self.obtener_ordenadas()
            if a.shape != b.shape:
                raise ValueError("Las matrices deben tener las mismas dimensiones para restar.")
            res = a - b
            self.mostrar_resultado(res, "Resta")
        except Exception as e:
            self.mostrar_error(str(e))

    def multiplicar(self):
        try:
            a, b = self.obtener_ordenadas()
            if a.shape[1] != b.shape[0]:
                raise ValueError("Columnas de la primera deben coincidir con filas de la segunda.")
            res = np.dot(a, b)
            self.mostrar_resultado(res, "Multiplicación")
        except Exception as e:
            self.mostrar_error(str(e))

    def determinantes(self):
        try:
            a = self.leer_matriz(self.tabla1)
            b = self.leer_matriz(self.tabla2)
            if a.shape[0] != a.shape[1] or b.shape[0] != b.shape[1]:
                raise ValueError("Ambas matrices deben ser cuadradas.")
            det_a = round(np.linalg.det(a), 2)
            det_b = round(np.linalg.det(b), 2)
            html = f"<b>Determinante A:</b> {self.format_result(det_a)}<br><br>" \
                   f"<b>Determinante B:</b> {self.format_result(det_b)}"
            self.resultado.setHtml(html)
        except Exception as e:
            self.mostrar_error(str(e))

    def inversas(self):
        mensajes = []
        try:
            a = self.leer_matriz(self.tabla1)
            if a.shape[0] == a.shape[1]:
                inv_a = np.linalg.inv(a)
                mensajes.append(f"<b>Inversa A:</b><br>{self.format_result(inv_a)}")
            else:
                mensajes.append("<b>Matriz A no es cuadrada.</b>")
        except np.linalg.LinAlgError:
            mensajes.append("<b>Matriz A es singular.</b>")
        except Exception as e:
            mensajes.append(f"<b>Error A:</b> {str(e)}")

        try:
            b = self.leer_matriz(self.tabla2)
            if b.shape[0] == b.shape[1]:
                inv_b = np.linalg.inv(b)
                mensajes.append(f"<b>Inversa B:</b><br>{self.format_result(inv_b)}")
            else:
                mensajes.append("<b>Matriz B no es cuadrada.</b>")
        except np.linalg.LinAlgError:
            mensajes.append("<b>Matriz B es singular.</b>")
        except Exception as e:
            mensajes.append(f"<b>Error B:</b> {str(e)}")

        self.resultado.setHtml("<br><br>".join(mensajes))

    def limpiar(self):
        self.resultado.clear()
        self.generar_tablas()

    def cambiar_orden(self):
        self.resultado.clear()

    def abrir_sistemas_lineales(self):
        self.sistema = SistemasLineales()
        self.sistema.show()
        self.hide()

    def salir(self):
        from menu import MenuPrincipal
        self.menu = MenuPrincipal()
        self.menu.show()
        self.close()

import sys
import re
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QTextEdit, QPushButton, QMessageBox, QGridLayout,
                            QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SistemasLineales(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resolver sistema de ecuaciones lineales")
        self.setGeometry(100, 100, 900, 700)
        
        self.setStyleSheet("""
QWidget {
    background-color: #f9f9f9;
    color: #333;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}

QLabel {
    font-weight: bold;
    padding: 4px 6px;
}

QSpinBox, QComboBox {
    background-color: #ffffff;
    border: 2px solid #e53935;
    padding: 6px 8px;
    border-radius: 6px;
    min-width: 60px;
}

QComboBox {
    min-width: 110px;
}

QPushButton {
    background-color: #003366;
    color: white;
    border: none;
    padding: 8px 16px;
    margin: 4px;
    border-radius: 6px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #002244;
}

QPushButton#btn_exit {
    background-color: #e74c3c;
}

QPushButton#btn_exit:hover {
    background-color: #c0392b;
}

QPushButton.tecla {
    background-color: #2c3e50;
    color: white;
    font-size: 14px;
    padding: 0;
    margin: 2px;
}

QPushButton.tecla:hover {
    background-color: #34495e;
}

QPushButton.tecla_operacion {
    background-color: #e53935;
}

QPushButton.tecla_operacion:hover {
    background-color: #c62828;
}

QPushButton.tecla_variable {
    background-color: #1e88e5;
}

QPushButton.tecla_variable:hover {
    background-color: #1565c0;
}

QTextEdit {
    background-color: #ffffff;
    border: 2px solid #e53935;
    padding: 10px;
    border-radius: 8px;
    color: #2c3e50;
    min-height: 120px;
    font-size: 15px;
    font-family: 'Courier New', monospace;
}

QFrame#teclado_frame {
    border: 1px solid #bdc3c7;
    border-radius: 8px;
    background-color: #ecf0f1;
    padding: 5px;
}
""")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.instrucciones = QLabel("Escribe un sistema de ecuaciones lineales (una por línea):")
        layout.addWidget(self.instrucciones)

        self.editor_ecuaciones = QTextEdit()
        self.editor_ecuaciones.setPlaceholderText(
            "Ejemplo:\nx - 3y + 2z = -3\n5x + 6y - z = 13\n4x - y + 3z = 8"
        )
        layout.addWidget(self.editor_ecuaciones)
        
        self.crear_teclado_matematico(layout)

        self.boton_resolver = QPushButton("Resolver sistema")
        self.boton_resolver.clicked.connect(self.resolver)
        layout.addWidget(self.boton_resolver)

        layout.addWidget(QLabel("Resultado:"))

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        botones_extras = QHBoxLayout()

        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.clicked.connect(self.limpiar_campos)
        botones_extras.addWidget(self.boton_limpiar)

        self.boton_volver = QPushButton("Volver a Calculadora")
        self.boton_volver.clicked.connect(self.volver_a_calculadora)
        self.boton_volver.setObjectName("btn_exit")
        botones_extras.addWidget(self.boton_volver)

        layout.addLayout(botones_extras)
    
    def crear_teclado_matematico(self, layout_principal):
        teclado_frame = QFrame()
        teclado_frame.setObjectName("teclado_frame")
        teclado_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        teclado_frame.setMinimumHeight(230)
        teclado_layout = QVBoxLayout(teclado_frame)
        teclado_layout.setContentsMargins(5, 5, 5, 5)
        teclado_layout.setSpacing(5)
        
        teclado_titulo = QLabel("Teclado Matemático")
        teclado_titulo.setAlignment(Qt.AlignCenter)
        teclado_titulo.setFont(QFont("Segoe UI", 11, QFont.Bold))
        teclado_layout.addWidget(teclado_titulo)
        
        grid = QGridLayout()
        grid.setSpacing(3)
        grid.setContentsMargins(2, 2, 2, 2)
        
        variables = ['x', 'y', 'z', 'a', 'b', 'c']
        for i, var in enumerate(variables):
            btn = QPushButton(var)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setProperty("class", "tecla tecla_variable")
            btn.clicked.connect(lambda checked, v=var: self.insertar_texto(v))
            grid.addWidget(btn, 0, i)
        
        for i in range(1, 7):
            btn = QPushButton(str(i))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setProperty("class", "tecla")
            btn.clicked.connect(lambda checked, num=str(i): self.insertar_texto(num))
            grid.addWidget(btn, 1, i-1)
        
        numeros = ['7', '8', '9', '0', '+', '-']
        for i, num in enumerate(numeros):
            btn = QPushButton(num)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if num in ['+', '-']:
                btn.setProperty("class", "tecla tecla_operacion")
            else:
                btn.setProperty("class", "tecla")
            btn.clicked.connect(lambda checked, n=num: self.insertar_texto(n))
            grid.addWidget(btn, 2, i)
            
        operaciones = ['*', '/', '(', ')', '=', '.']
        for i, op in enumerate(operaciones):
            btn = QPushButton(op)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setProperty("class", "tecla tecla_operacion")
            btn.clicked.connect(lambda checked, o=op: self.insertar_texto(o))
            grid.addWidget(btn, 3, i)
        
        funciones = [('x²', lambda: self.insertar_texto("²")),
                    ('√', lambda: self.insertar_texto("√")),
                    ('π', lambda: self.insertar_texto("π")),
                    ('←', self.borrar_caracter),
                    ('Limpiar', self.limpiar_actual),
                    ('Espacio', lambda: self.insertar_texto(" "))]
        
        for i, (texto, funcion) in enumerate(funciones):
            btn = QPushButton(texto)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if texto in ['←', 'Limpiar']:
                btn.setProperty("class", "tecla tecla_operacion")
            else:
                btn.setProperty("class", "tecla tecla_variable")
            btn.clicked.connect(funcion)
            grid.addWidget(btn, 4, i)
        
        teclado_layout.addLayout(grid)
        
        toggle_container = QHBoxLayout()
        self.toggle_teclado_btn = QPushButton("Ocultar Teclado")
        self.toggle_teclado_btn.clicked.connect(self.toggle_teclado)
        self.toggle_teclado_btn.setFixedWidth(150)
        toggle_container.addStretch(1)
        toggle_container.addWidget(self.toggle_teclado_btn)
        toggle_container.addStretch(1)
        teclado_layout.addLayout(toggle_container)
        
        layout_principal.addWidget(teclado_frame)
        self.teclado_frame = teclado_frame
        
    def toggle_teclado(self):
        if self.teclado_frame.isVisible():
            self.teclado_frame.hide()
            self.toggle_teclado_btn.setText("Mostrar Teclado")
        else:
            self.teclado_frame.show()
            self.toggle_teclado_btn.setText("Ocultar Teclado")
            
    def insertar_texto(self, texto):
        self.editor_ecuaciones.insertPlainText(texto)
        self.editor_ecuaciones.setFocus()
        
    def borrar_caracter(self):
        cursor = self.editor_ecuaciones.textCursor()
        cursor.deletePreviousChar()
        
    def limpiar_actual(self):
        cursor = self.editor_ecuaciones.textCursor()
        cursor.movePosition(cursor.StartOfLine)
        cursor.movePosition(cursor.EndOfLine, cursor.KeepAnchor)
        cursor.removeSelectedText()
        self.editor_ecuaciones.setTextCursor(cursor)
        self.editor_ecuaciones.setFocus()

    def limpiar_campos(self):
        self.editor_ecuaciones.clear()
        self.resultado.clear()
        
    def volver_a_calculadora(self):
        from menu import MenuMatrices
        self.calc = MenuMatrices()
        self.calc.show()
        self.close()

    def analizar_sistema(self, texto):
        lineas = texto.strip().split('\n')
        variables = sorted(list(set(re.findall(r'[a-zA-Z]', texto))))
        A = []
        B = []

        for linea in lineas:
            coeficientes = [0] * len(variables)
            izquierda, derecha = linea.split('=')
            izquierda = izquierda.replace(' ', '')
            terminos = re.findall(r'[\+\-]?\d*\.?\d*[a-zA-Z]', izquierda)

            for termino in terminos:
                match = re.match(r'([\+\-]?\d*\.?\d*)([a-zA-Z])', termino)
                if match:
                    coef_str, var = match.groups()
                    if coef_str in ['', '+', '-']:
                        coef_str += '1'
                    coef = float(coef_str)
                    idx = variables.index(var)
                    coeficientes[idx] = coef

            A.append(coeficientes)
            B.append(float(derecha.strip()))
        
        return np.array(A), np.array(B), variables

    def resolver_sistema(self, A, B):
        try:
            if A.shape[0] != A.shape[1]:
                return "Error: La matriz A no es cuadrada."
            if A.shape[0] != B.shape[0]:
                return "Error: Dimensiones incompatibles entre A y B."
            x = np.linalg.solve(A, B)
            return x
        except np.linalg.LinAlgError as e:
            return f"Error al resolver el sistema: {e}"
        except Exception as e:
            return f"Error inesperado: {e}"

    def resolver(self):
        texto = self.editor_ecuaciones.toPlainText()
        if not texto.strip():
            QMessageBox.warning(self, "Advertencia", "Por favor escribe un sistema de ecuaciones.")
            return

        try:
            A, B, variables = self.analizar_sistema(texto)
            resultado = self.resolver_sistema(A, B)

            if isinstance(resultado, str):
                self.resultado.setText(resultado)
            else:
                texto_resultado = "\n".join(f"{var} = {round(valor, 2)}" for var, valor in zip(variables, resultado))
                self.resultado.setText(texto_resultado)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al analizar el sistema:\nIngrese bien el Sistema de Ecuaciones.\nDetalles: {str(e)}")
