import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QGridLayout, QFrame, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from oppoli import MenuPolinomios
from calculadora import MatrixCalculator, SistemasLineales
from opvect import CalculadoraVectores
from acercade import AcercaDe 
from fun2d import Graficas_2d_3d
class MenuMatrices(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeuroMate - Menú Matrices")
        self.setGeometry(200, 200, 500, 400)
        self.setWindowIcon(QIcon("icon.png"))

        self.setStyleSheet("""
            QWidget {
                background-color: #fdfaf6;
                color: #2e2e2e;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLabel#title {
                font-weight: bold;
                font-size: 24px;
                color: #1a3c73;
                margin: 20px 0;
            }
            QFrame#card {
                background-color: #ffffff;
                border: 1px solid #d0d7e3;
                border-radius: 16px;
                padding: 20px;
                margin: 10px;
            }
            QPushButton {
                background-color: #3dbff3;
                border: none;
                padding: 10px 16px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 14px;
                margin-top: 12px;
            }
            QPushButton:hover {
                background-color: #63cdf9;
            }
            QPushButton#btn_exit {
                background-color: #e74c3c;
            }
            QPushButton#btn_exit:hover {
                background-color: #c0392b;
            }
        """)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --- Título con ícono e imagen ---
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel()
        icon_pixmap = QPixmap("img/matrices.png")
        icon_pixmap = icon_pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignCenter)

        title = QLabel(" Operaciones con Matrices")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        title_layout.addWidget(icon_label)
        title_layout.addWidget(title)

        main_layout.addLayout(title_layout)
        grid = QGridLayout()
        main_layout.addLayout(grid)

        grid.addWidget(self.crear_card("Calculadora de Matrices", "img/matrices.png", self.abrir_matrices), 0, 0)
        grid.addWidget(self.crear_card("Sistemas de Ecuaciones Lineales", "img/sl.png",  self.abrir_msl), 0, 1)
        grid.addWidget(self.crear_card("Volver al Menú Principal", "img/salir.png", self.volver_menu, exit=True), 1, 0, 1, 2)

    def crear_card(self, titulo, ruta_imagen, funcion, exit=False):
        frame = QFrame()
        frame.setObjectName("card")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        frame.setLayout(layout)

        # Imagen
        icono = QLabel()
        pixmap = QPixmap(ruta_imagen)
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icono.setPixmap(pixmap)
        icono.setAlignment(Qt.AlignCenter)

        # Título
        label = QLabel(titulo)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 12px; margin-bottom: 6px;")

        # Botón
        boton = QPushButton("Abrir" if not exit else "Volver")
        if exit:
            boton.setObjectName("btn_exit")
        boton.clicked.connect(funcion)

        layout.addWidget(icono)
        layout.addWidget(label)
        layout.addWidget(boton)

        return frame

    def abrir_matrices(self):
        self.calc = MatrixCalculator()
        self.calc.show()
        self.close()

    def abrir_msl(self):
        self.calc = SistemasLineales()
        self.calc.show()
        self.close()
        
    def sistemas_no_implementado(self):
        self.mensaje_no_listo("Sistemas de ecuaciones lineales")
        
    def mensaje_no_listo(self, titulo):
        msg = QMessageBox()
        msg.setWindowTitle("Funcionalidad no disponible")
        msg.setText(f"{titulo} aún no está implementada.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        
    def volver_menu(self):
        from menu import MenuPrincipal
        self.menu = MenuPrincipal()
        self.menu.show()
        self.close()

# Clase MenuPrincipal modificada
class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeuroMate - Menú Principal")
        self.setGeometry(200, 200, 600, 500)
        self.setWindowIcon(QIcon("icon.png"))

        self.setStyleSheet("""
            QWidget {
                background-color: #fdfaf6;
                color: #2e2e2e;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLabel#title {
                font-weight: bold;
                font-size: 24px;
                color: #1a3c73;
                margin: 20px 0;
            }
            QFrame#card {
                background-color: #ffffff;
                border: 1px solid #d0d7e3;
                border-radius: 16px;
                padding: 20px;
                margin: 10px;
            }
            QPushButton {
                background-color: #3dbff3;
                border: none;
                padding: 10px 16px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 14px;
                margin-top: 12px;
            }
            QPushButton:hover {
                background-color: #63cdf9;
            }
            QPushButton#btn_exit {
                background-color: #e74c3c;
            }
            QPushButton#btn_exit:hover {
                background-color: #c0392b;
            }
        """)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --- Título con ícono e imagen ---
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel()
        icon_pixmap = QPixmap("icon.png")
        icon_pixmap = icon_pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignCenter)

        title = QLabel(" NeuroMate - Menu")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        title_layout.addWidget(icon_label)
        title_layout.addWidget(title)

        main_layout.addLayout(title_layout)

        # --- Grid de tarjetas ---
        grid = QGridLayout()
        main_layout.addLayout(grid)

        grid.addWidget(self.crear_card("Matrices", "img/matrices.png", self.abrir_matrices), 0, 0)
        grid.addWidget(self.crear_card("Operaciones con Polinomios", "img/polinomios.png", self.abrir_polinomios), 0, 1)
        grid.addWidget(self.crear_card("Operaciones con Vectores", "img/vectores.png", self.abrir_vectores), 0, 2)
        grid.addWidget(self.crear_card("Funciones", "img/funcion.webp", self.abrir_funciones), 1, 0)
        grid.addWidget(self.crear_card("Acerca de", "img/acerd.png", self.abrir_acerca_de), 1, 1)
        grid.addWidget(self.crear_card("Salir", "img/salir.png", sys.exit, exit=True), 1, 2)

    def crear_card(self, titulo, ruta_imagen, funcion, exit=False):
        frame = QFrame()
        frame.setObjectName("card")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        frame.setLayout(layout)

        # Imagen
        icono = QLabel()
        pixmap = QPixmap(ruta_imagen)
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icono.setPixmap(pixmap)
        icono.setAlignment(Qt.AlignCenter)

        # Título
        label = QLabel(titulo)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 12px; margin-bottom: 6px;")

        # Botón
        boton = QPushButton("Abrir" if not exit else "Salir")
        if exit:
            boton.setObjectName("btn_exit")
        boton.clicked.connect(funcion)

        layout.addWidget(icono)
        layout.addWidget(label)
        layout.addWidget(boton)

        return frame

    # Método modificado para abrir el menú intermedio de matrices
    def abrir_matrices(self):
        self.menu_matrices = MenuMatrices()
        self.menu_matrices.show()
        self.hide()  # Oculta el menú principal

    def abrir_polinomios(self):
        self.poli = MenuPolinomios()
        self.poli.show()

    def abrir_funciones(self):
        self.poli = Graficas_2d_3d()
        self.poli.show()

    def abrir_vectores(self):
        self.calculadora_vectores = CalculadoraVectores()
        self.calculadora_vectores.show()

    def abrir_acerca_de(self):
        self.acerca = AcercaDe()
        self.acerca.show()

    def funciones_no_implementado(self):
        self.mensaje_no_listo("Esta función")

    def mensaje_no_listo(self, titulo):
        msg = QMessageBox()
        msg.setWindowTitle("Funcionalidad no disponible")
        msg.setText(f"{titulo} aún no está implementada.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MenuPrincipal()
    menu.show()
    sys.exit(app.exec_())