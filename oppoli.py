import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QGridLayout,
    QFrame, QHBoxLayout, QLineEdit, QTextEdit, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sympy as sp

class MenuPolinomios(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📈 Calculadora de Polinomios")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet(self.estilos())

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(30)

        # Título
        titulo = QLabel("📈 Operaciones con Polinomios")
        titulo.setObjectName("titulo")
        layout_principal.addWidget(titulo)

        # Grid de tarjetas
        grid = QGridLayout()
        grid.setSpacing(30)
        grid.setAlignment(Qt.AlignCenter)

        operaciones = [
            ("Sumar", self.abrir_suma),
            ("Multiplicar", self.abrir_multiplicacion),
            ("Derivadas", self.abrir_derivada),
            ("Integrales", self.abrir_integracion),
            ("Evaluar", self.abrir_evaluacion),
            ("Salir", self.volver, "botonVolver")
        ]

        row, col = 0, 0
        for operacion in operaciones:
            if len(operacion) == 3:
                texto, funcion, objeto_nombre = operacion
            else:
                texto, funcion = operacion
                objeto_nombre = "botonTarjeta"
                
            tarjeta = self.crear_tarjeta(texto, funcion, objeto_nombre)
            grid.addWidget(tarjeta, row, col)
            
            col += 1
            if col >= 3:
                row += 1
                col = 0

        layout_principal.addLayout(grid)

    def crear_tarjeta(self, texto, funcion, objeto_nombre="botonTarjeta"):
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")
        tarjeta.setFixedSize(240, 160)

        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignCenter)

        # Imagen correspondiente al módulo (excepto para el botón volver)
        if objeto_nombre != "botonVolver":
            imagen_label = QLabel()
            ruta_imagen = f"images/{texto.lower()}.png"
            pixmap = QPixmap(ruta_imagen).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            imagen_label.setPixmap(pixmap)
            imagen_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(imagen_label)

        # Botón de la tarjeta
        boton = QPushButton(texto)
        boton.setObjectName(objeto_nombre)
        boton.setCursor(Qt.PointingHandCursor)
        boton.setFixedSize(180, 60)
        boton.clicked.connect(funcion)
        layout.addWidget(boton)

        return tarjeta

    def estilos(self):
        return """
        QWidget {
            background-color: #ffffff;
            color: #000000;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 15px;
        }

        QLabel#titulo {
            font-size: 30px;
            font-weight: bold;
            padding: 20px;
            background-color: #ffffff;
            border-bottom: 3px solid #000080;
            color: #000000;
            qproperty-alignment: AlignCenter;
        }

        QFrame#tarjeta {
            background-color: #ffffff;
            border-radius: 20px;
            border: 2px solid #ff0000;
        }

        QPushButton#botonTarjeta {
            background-color: #000080;
            border: none;
            border-radius: 12px;
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
            color: white;
        }

        QPushButton#botonTarjeta:hover {
            background-color: #0000b3;
            border: none;
        }

        QPushButton#botonVolver {
            background-color: #ff0000;
            color: white;
            font-size: 15px;
            border: none;
            padding: 10px 20px;
            border-radius: 12px;
        }

        QPushButton#botonVolver:hover {
            background-color: #cc0000;
        }
        
        QLineEdit {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #000080;
            border-radius: 5px;
            padding: 5px;
        }
        
        QTextEdit {
            background-color: #ffffff;
            color: #000080;
            border: 1px solid #000080;
            border-radius: 5px;
            padding: 5px;
        }
        
        QPushButton {
            background-color: #000080;
            color: white;
            border-radius: 5px;
            padding: 8px 16px;
        }
        
        QPushButton:hover {
            background-color: #0000b3;
        }
        """

    def abrir_suma(self):
        self.abrir_operacion("Sumar")

    def abrir_multiplicacion(self):
        self.abrir_operacion("Multiplicar")

    def abrir_derivada(self):
        self.abrir_operacion("Derivadas")

    def abrir_integracion(self):
        self.abrir_operacion("Integrales")

    def abrir_evaluacion(self):
        self.abrir_operacion("Evaluar")

    def abrir_operacion(self, operacion):
        self.ventana = CalculadoraPolinomios(operacion)
        self.ventana.show()
        self.close()

    def volver(self):
        from menu import MenuPrincipal
        self.menu = MenuPrincipal()
        self.menu.show()
        self.close()
        
class CalculadoraPolinomios(QWidget):
    def __init__(self, operacion):
        super().__init__()
        self.operacion = operacion
        self.setWindowTitle(f"Operación: {self.operacion}")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
        QWidget {
            background-color: #ffffff;
            color: #000000;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 15px;
        }
        
        QLineEdit {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #000080;
            border-radius: 5px;
            padding: 5px;
        }
        
        QPushButton {
            background-color: #000080;
            color: white;
            border-radius: 5px;
            padding: 8px 16px;
        }
        
        QPushButton:hover {
            background-color: #0000b3;
        }
        
        QPushButton#botonVolver {
            background-color: #ff0000;
            color: white;
        }
        
        QPushButton#botonVolver:hover {
            background-color: #cc0000;
        }
        """)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel(f"Operación seleccionada: {self.operacion}"))

        # Entrada para polinomios
        self.polynomial_a_label = QLabel("Polinomio A:")
        self.polynomial_a_input = QLineEdit()
        self.polynomial_a_input.setPlaceholderText("Ejemplo: 3x^2 + 2x + 1")
        self.layout.addWidget(self.polynomial_a_label)
        self.layout.addWidget(self.polynomial_a_input)

        self.polynomial_b_label = QLabel("Polinomio B:")
        self.polynomial_b_input = QLineEdit()
        self.polynomial_b_input.setPlaceholderText("Ejemplo: 3x^2 + 2x + 1 ")

        # Solo mostrar el campo B si la operación lo necesita
        if self.operacion in ["Sumar", "Multiplicar"]:
            self.layout.addWidget(self.polynomial_b_label)
            self.layout.addWidget(self.polynomial_b_input)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("""
            font-size: 20px;
            color: #000080;
            background-color: #ffffff;
            border: 1px solid #000080;
            border-radius: 10px;
            padding: 10px;
        """)
        self.layout.addWidget(QLabel("Resultado:"))
        self.layout.addWidget(self.resultado)

        botones_layout = QHBoxLayout()
        self.boton_calcular = QPushButton("Calcular")
        self.boton_calcular.clicked.connect(self.calcular)
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.clicked.connect(self.limpiar_campos)
        self.boton_volver = QPushButton("Volver al menú")
        self.boton_volver.setObjectName("botonVolver")
        self.boton_volver.clicked.connect(self.volver_al_menu)

        botones_layout.addWidget(self.boton_calcular)
        botones_layout.addWidget(self.boton_limpiar)
        botones_layout.addWidget(self.boton_volver)
        self.layout.addLayout(botones_layout)
        

    def calcular(self):
        polinomio_a = self.polynomial_a_input.text().strip()
        polinomio_b = self.polynomial_b_input.text().strip()

        def formatear_polinomio(entrada):
            entrada = entrada.replace('^', '**')
            entrada = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', entrada)
            entrada = re.sub(r'([a-zA-Z])\(', r'\1*(', entrada)
            return entrada
        
        def presentar_polinomio(expr):
            texto = str(expr)
            texto = texto.replace('**', '^')
            texto = re.sub(r'\b1\*', '', texto)                   
            texto = re.sub(r'(\d)\*x', r'\1x', texto)             
            texto = re.sub(r'(?<!\^)(?<!\*)\bx\b', 'x', texto)   
            texto = texto.replace('*', '')                      
            return texto

        # Si el campo necesario está vacío, mostrar advertencia
        if self.operacion in ["Sumar", "Multiplicar"]:
            if not polinomio_a or not polinomio_b:
                QMessageBox.warning(self, "Campos vacíos", "Debes completar ambos polinomios para esta operación.")
                return
        else:
            if not polinomio_a:
                QMessageBox.warning(self, "Campo vacío", "Debes ingresar al menos el Polinomio A para esta operación.")
                return

        x = sp.Symbol('x')

        try:
            entrada_a = formatear_polinomio(polinomio_a if polinomio_a else "0")
            entrada_b = formatear_polinomio(polinomio_b if polinomio_b else "0")

            if self.operacion == "Sumar":
                x = sp.Symbol('x')
                poly_a = sp.Poly(sp.sympify(entrada_a), x).as_expr()
                poly_b = sp.Poly(sp.sympify(entrada_b), x).as_expr()
                resultado_expr = sp.simplify(poly_a + poly_b)
                resultado_str = presentar_polinomio(resultado_expr)
                self.resultado.setText(f"Resultado:\n{resultado_str}")

            elif self.operacion == "Multiplicar":
                x = sp.Symbol('x')
                poly_a = sp.Poly(sp.sympify(entrada_a), x).as_expr()
                poly_b = sp.Poly(sp.sympify(entrada_b), x).as_expr()
                resultado_expr = sp.simplify(poly_a * poly_b)
                resultado_str = presentar_polinomio(resultado_expr)
                self.resultado.setText(f"Resultado:\n{resultado_str}")

            elif self.operacion == "Derivadas":
                var_str, ok = QInputDialog.getText(self, "Variable", "¿Respecto a qué variable quieres derivar? (por ejemplo: x, y, z)")
                if not ok or not var_str.isalpha():
                    QMessageBox.warning(self, "Variable inválida", "Debes ingresar una variable válida (una letra como x, y, z).")
                    return

                variable = sp.Symbol(var_str.strip())
                poly_a = sp.sympify(entrada_a)
                resultado_expr = sp.diff(poly_a, variable)
                resultado_str = presentar_polinomio(resultado_expr)
                self.resultado.setText(f"Resultado:\n{resultado_str}")

            elif self.operacion == "Integrales":
                var_str, ok = QInputDialog.getText(self, "Variable", "¿Respecto a qué variable quieres integrar? (por ejemplo: x, y, z)")
                if not ok or not var_str.isalpha():
                    QMessageBox.warning(self, "Variable inválida", "Debes ingresar una variable válida (una letra como x, y, z).")
                    return

                variable = sp.Symbol(var_str.strip())
                poly_a = sp.sympify(entrada_a)
                resultado_expr = sp.integrate(poly_a, variable)
                resultado_str = presentar_polinomio(resultado_expr) + " + C"
                self.resultado.setText(f"Resultado:\n{resultado_str}")

            elif self.operacion == "Evaluar":
                valor, ok = QInputDialog.getDouble(self, "Evaluar", "¿En qué valor deseas evaluar el polinomio?")
                if ok:
                    x = sp.Symbol('x')  # Puedes hacer esto dinámico también si quieres
                    poly_a = sp.sympify(entrada_a)
                    resultado_eval = poly_a.subs(x, valor)
                    resultado_str = presentar_polinomio(resultado_eval)
                    self.resultado.setText(f"Resultado:\n{resultado_str}")
                else:
                    self.resultado.setText("Evaluación cancelada.")

        except Exception as e:
            self.resultado.setText("Error en el procesamiento del polinomio.\nVerifica la sintaxis.")

    def limpiar_campos(self):
        self.polynomial_a_input.clear()
        self.polynomial_b_input.clear()
        self.resultado.clear()

    def volver_al_menu(self):
        self.menu = MenuPolinomios()
        self.menu.show()
        self.close()