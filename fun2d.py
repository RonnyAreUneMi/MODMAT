import numpy as np
import sympy as sp
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QListWidget, QMessageBox, QFileDialog, QCheckBox, QGridLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

class Graficas_2d_3d(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gráficas Avanzadas 2D y 3D")
        self.setStyleSheet("background-color: #F5F8FA; color: #333333; font-family: 'Helvetica Neue', sans-serif;")
        self.setGeometry(100, 100, 1200, 800)

        self.funciones_guardadas = []

        main_layout = QHBoxLayout(self)
        panel_izquierdo = QVBoxLayout()

        panel_titulo = QVBoxLayout()
        titulo = QLabel("📊 Graficador de Funciones 2D/3D")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 30px; font-weight: bold; color: #2D3E50; margin-bottom: 20px;")
        panel_titulo.addWidget(titulo)

        self.input_funcion = QLineEdit()
        self.input_funcion.setPlaceholderText("Escribe una función, por ejemplo: x**2 * exp(x) o sin(x)")
        self.input_funcion.setStyleSheet("padding: 14px; border-radius: 8px; background-color: #E4F0F6; color: #333333; border: 1px solid #B0D2E0; margin-bottom: 10px;")
        panel_titulo.addWidget(self.input_funcion)

        self.crear_teclado_simbolos(panel_titulo)

        etiqueta_lista = QLabel("Funciones guardadas:")
        etiqueta_lista.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 15px;")
        panel_titulo.addWidget(etiqueta_lista)
        
        self.lista_funciones = QListWidget()
        self.lista_funciones.setStyleSheet("background-color: #E4F0F6; color: #333333; border-radius: 8px; border: 1px solid #B0D2E0; margin-bottom: 15px;")
        panel_titulo.addWidget(self.lista_funciones)

        boton_agregar = QPushButton("➕ Agregar función")
        boton_agregar.setCursor(Qt.PointingHandCursor)
        boton_agregar.setStyleSheet("background-color: #0077B6; color: white; font-weight: bold; border-radius: 8px; padding: 12px; margin-bottom: 15px;")
        boton_agregar.clicked.connect(self.agregar_funcion)
        panel_titulo.addWidget(boton_agregar)

        self.check_grid = QCheckBox("Mostrar cuadrícula")
        self.check_grid.setChecked(True)
        self.check_grid.setStyleSheet("font-size: 14px; margin: 5px 0;")
        panel_titulo.addWidget(self.check_grid)

        botones_layout = QHBoxLayout()
        self.boton_2d = QPushButton("Mostrar Gráfica 2D")
        self.boton_2d.setCursor(Qt.PointingHandCursor)
        self.boton_2d.setStyleSheet("background-color: #0077B6; font-weight: bold; color: white; border-radius: 8px; padding: 10px;")
        self.boton_2d.clicked.connect(self.mostrar_grafica_2d)
        botones_layout.addWidget(self.boton_2d)

        self.boton_3d = QPushButton("Mostrar Gráfica 3D")
        self.boton_3d.setCursor(Qt.PointingHandCursor)
        self.boton_3d.setStyleSheet("background-color: #0077B6; font-weight: bold; color: white; border-radius: 8px; padding: 10px;")
        self.boton_3d.clicked.connect(self.mostrar_grafica_3d)
        botones_layout.addWidget(self.boton_3d)

        panel_titulo.addLayout(botones_layout)

        botones_layout2 = QHBoxLayout()
        
        self.boton_guardar = QPushButton("Guardar Imagen")
        self.boton_guardar.setCursor(Qt.PointingHandCursor)
        self.boton_guardar.setStyleSheet("background-color: #28a745; font-weight: bold; color: white; border-radius: 8px; padding: 10px;")
        self.boton_guardar.clicked.connect(self.guardar_imagen)
        botones_layout2.addWidget(self.boton_guardar)

        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.setCursor(Qt.PointingHandCursor)
        self.boton_limpiar.setStyleSheet("background-color: #FF6B6B; font-weight: bold; color: white; border-radius: 8px; padding: 10px;")
        self.boton_limpiar.clicked.connect(self.limpiar_campos)
        botones_layout2.addWidget(self.boton_limpiar)

        self.boton_volver = QPushButton("Volver")
        self.boton_volver.setCursor(Qt.PointingHandCursor)
        self.boton_volver.setStyleSheet("background-color: #0077B6; font-weight: bold; color: white; border-radius: 8px; padding: 10px;")
        self.boton_volver.clicked.connect(self.volver)
        botones_layout2.addWidget(self.boton_volver)

        panel_titulo.addLayout(botones_layout2)
        panel_izquierdo.addLayout(panel_titulo)

        self.figura = Figure(figsize=(8, 6), facecolor='white')
        self.canvas = FigureCanvas(self.figura)
        main_layout.addLayout(panel_izquierdo, 1)
        main_layout.addWidget(self.canvas, 2)

    def crear_teclado_simbolos(self, layout):
        simbolos_frame = QVBoxLayout()
        
        etiqueta_teclado = QLabel("Símbolos matemáticos:")
        etiqueta_teclado.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        simbolos_frame.addWidget(etiqueta_teclado)
        
        simbolos_grid = QGridLayout()
        simbolos_grid.setSpacing(5)
        
        simbolos = [
            ("+", "Suma"),
            ("-", "Resta"),
            ("*", "Multiplicación"),
            ("/", "División"),
            ("**", "Potencia"),
            ("sqrt()", "Raíz cuadrada"),
            ("sin()", "Seno"),
            ("cos()", "Coseno"),
            ("tan()", "Tangente"),
            ("log()", "Logaritmo natural"),
            ("exp()", "Exponencial"),
            ("pi", "Pi"),
            ("e", "Número de Euler"),
            ("abs()", "Valor absoluto"),
            ("()", "Paréntesis")
        ]
        
        pos = 0
        for simbolo, tooltip in simbolos:
            boton = QPushButton(simbolo)
            boton.setToolTip(tooltip)
            boton.setStyleSheet("""
                QPushButton {
                    background-color: #E4F0F6;
                    color: #333333;
                    border: 1px solid #B0D2E0;
                    border-radius: 6px;
                    padding: 8px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #B0D2E0;
                }
            """)
            boton.setCursor(Qt.PointingHandCursor)
            boton.clicked.connect(lambda checked, s=simbolo: self.insertar_simbolo(s))
            
            fila, columna = divmod(pos, 5)
            simbolos_grid.addWidget(boton, fila, columna)
            pos += 1
        
        simbolos_frame.addLayout(simbolos_grid)
        layout.addLayout(simbolos_frame)

    def insertar_simbolo(self, simbolo):
        texto_actual = self.input_funcion.text()
        posicion_cursor = self.input_funcion.cursorPosition()
        
        if simbolo.endswith("()"):
            nuevo_texto = texto_actual[:posicion_cursor] + simbolo + texto_actual[posicion_cursor:]
            nueva_posicion = posicion_cursor + len(simbolo) - 1
        else:
            nuevo_texto = texto_actual[:posicion_cursor] + simbolo + texto_actual[posicion_cursor:]
            nueva_posicion = posicion_cursor + len(simbolo)
        
        self.input_funcion.setText(nuevo_texto)
        self.input_funcion.setFocus()
        self.input_funcion.setCursorPosition(nueva_posicion)

    def agregar_funcion(self):
        texto = self.input_funcion.text()
        if texto.strip() == "":
            return
        self.funciones_guardadas.append(texto)
        self.lista_funciones.addItem(texto)
        self.input_funcion.clear()
        QMessageBox.information(self, "Función guardada", f"La función '{texto}' ha sido guardada correctamente.")

    def mostrar_grafica_2d(self):
        if not self.funciones_guardadas:
            QMessageBox.warning(self, "Sin funciones", "Primero agrega al menos una función.")
            return
            
        try:
            x_min = -10
            x_max = 10
            
            x = sp.symbols('x')
            x_val = np.linspace(x_min, x_max, 400)
            self.figura.clear()
            ax = self.figura.add_subplot(111)
            
            for func_str in self.funciones_guardadas:
                func_str = func_str.replace("^", "**")
                if 'y' in func_str:
                    QMessageBox.warning(self, "Error", f"La función '{func_str}' contiene 'y'. Solo se permiten funciones de x en gráficas 2D.")
                    continue
                try:
                    expr = sp.sympify(func_str)
                    
                    f = sp.lambdify(x, expr, modules=["numpy"])
                    
                    y_val = f(x_val)
                    
                    if np.isnan(y_val).all() or np.isinf(y_val).all():
                        QMessageBox.warning(self, "Error", f"La función '{func_str}' no se puede graficar en el dominio especificado.")
                        continue
                    
                    valid_indices = np.isfinite(y_val)
                    if not np.any(valid_indices):
                        QMessageBox.warning(self, "Error", f"La función '{func_str}' genera solo valores infinitos o no numéricos.")
                        continue
                    
                    ax.plot(x_val[valid_indices], y_val[valid_indices], label=f"y = {func_str}")
                    
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"No se pudo graficar: '{func_str}'\nError: {str(e)}")
                    continue
            
            ax.grid(self.check_grid.isChecked())
            ax.legend(loc='upper left')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('Gráfica 2D')
            self.canvas.draw()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar la gráfica: {str(e)}")

    def mostrar_grafica_3d(self):
        if not self.funciones_guardadas:
            QMessageBox.warning(self, "Sin funciones", "Primero agrega al menos una función para graficar en 3D.")
            return
        
        try:
            x_min, x_max = -5, 5
            y_min, y_max = -5, 5
            
            x, y = sp.symbols('x y')
            x_val = np.linspace(x_min, x_max, 100)
            y_val = np.linspace(y_min, y_max, 100)
            X, Y = np.meshgrid(x_val, y_val)

            self.figura.clear()
            ax = self.figura.add_subplot(111, projection='3d')

            for func_str in self.funciones_guardadas:
                func_str = func_str.replace("^", "**")
                try:
                    expr = sp.sympify(func_str)
                    free_symbols = [str(sym) for sym in expr.free_symbols]
                    
                    if 'y' not in free_symbols:
                        f = sp.lambdify(x, expr, modules=["numpy"])
                        Z = np.zeros_like(X)
                        for i in range(Z.shape[0]):
                            Z[i, :] = f(X[i, :])
                    else:
                        f = sp.lambdify((x, y), expr, modules=["numpy"])
                        Z = f(X, Y)
                    
                    if np.isnan(Z).all() or np.isinf(Z).all():
                        QMessageBox.warning(self, "Error", f"La función '{func_str}' no se puede graficar en el dominio especificado.")
                        continue
                    
                    Z = np.where(np.isfinite(Z), Z, np.nan)
                    
                    max_z = 50
                    Z = np.clip(Z, -max_z, max_z)
                    
                    colors = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
                    color_index = self.funciones_guardadas.index(func_str) % len(colors)
                    
                    surf = ax.plot_surface(X, Y, Z, cmap=colors[color_index], edgecolor='none', alpha=0.7)
                    
                    if 'y' in free_symbols:
                        func_label = f"z = {func_str}"
                    else:
                        func_label = f"z = {func_str} (extendido en y)"
                    self.figura.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label=func_label)
                    
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"No se pudo graficar en 3D: '{func_str}'\nError: {str(e)}")
                    continue

            ax.grid(self.check_grid.isChecked())
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title('Gráfica 3D')
            self.canvas.draw()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar la gráfica 3D: {str(e)}")

    def guardar_imagen(self):
        if not hasattr(self.figura, 'axes') or not self.figura.axes:
            QMessageBox.warning(self, "Sin gráfica", "Primero debes generar una gráfica.")
            return
            
        opciones = QFileDialog.Options()
        nombre_archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Gráfica", "", 
            "Imágenes PNG (*.png);;Imágenes JPG (*.jpg);;Todos los archivos (*)",
            options=opciones)
            
        if nombre_archivo:
            try:
                if not (nombre_archivo.endswith('.png') or nombre_archivo.endswith('.jpg')):
                    nombre_archivo += '.png'
                
                self.figura.savefig(nombre_archivo, dpi=150, bbox_inches='tight')
                QMessageBox.information(self, "Guardado exitoso", 
                                      f"La gráfica se ha guardado como {nombre_archivo}")
            except Exception as e:
                QMessageBox.critical(self, "Error al guardar", 
                                   f"No se pudo guardar la imagen: {str(e)}")

    def limpiar_campos(self):
        self.input_funcion.clear()
        self.lista_funciones.clear()
        self.funciones_guardadas.clear()
        self.figura.clear()
        self.canvas.draw()

    def volver(self):
        self.close()