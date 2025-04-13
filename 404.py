import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QTabWidget, QPushButton, QMainWindow, QGraphicsOpacityEffect,
    QHBoxLayout, QGridLayout, QProgressBar, QMessageBox, QStackedWidget
)
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QBrush, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QRectF, QPropertyAnimation
import ctypes  # Para pedir permisos de administrador
from PyQt5.QtWidgets import QMessageBox
import subprocess  # Para ejecutar el archivo .bat

# Función para solicitar permisos de administrador en Windows
def pedir_permiso_administrador():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit(0)


class CircularProgress(QWidget):
    def __init__(self, label, color):
        super().__init__()
        self.value = 0
        self.label = label
        self.color = color
        self.setFixedSize(180, 180)

    def setValue(self, val):
        self.value = val
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # Fondo blur simulado
        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0.0, QColor(255, 255, 255, 30))
        gradient.setColorAt(1.0, QColor(0, 0, 0, 30))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect.adjusted(5, 5, -5, -5))

        # Círculo de progreso
        pen = QPen(QColor(self.color), 12)
        painter.setPen(pen)
        painter.drawArc(QRectF(15, 15, 150, 150), -90 * 16, -self.value * 360 / 100 * 16)

        # Texto
        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Segoe UI", 11, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, f"{self.label}\n{self.value:.0f}%")


class LimpiadorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("404 Limpiador")
        self.setGeometry(200, 100, 300, 520)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        contenedor = QWidget()
        contenedor.setStyleSheet("QWidget { background-color: rgba(30, 30, 30, 160); border-radius: 25px; }")

        layout = QVBoxLayout()

        # Añadir un contenedor de pestañas con más estilo
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(""" 
            QTabWidget::pane { border: none; background-color: rgba(30, 30, 30, 160); border-radius: 15px; }
            QTabBar::tab {
                background: rgba(255, 255, 255, 30);
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: rgba(255, 255, 255, 50);
            }
            QTabBar::tab:hover {
                background: rgba(255, 255, 255, 40);
            }
        """)

        # Pestañas con contenido
        self.tabs.addTab(self.crear_tab_inicio(), " 🌟 Inicio ")
        self.tabs.addTab(self.crear_tab_limpieza(), " 🧼 Limpieza  ")
        self.tabs.addTab(self.crear_tab_juegos(), " 🎮 Juegos  ")

        layout.addWidget(self.tabs)

        # Botón de cerrar arriba en la derecha
        self.close_button = QPushButton("❌")
        self.close_button.setStyleSheet(""" 
            QPushButton {
                background: transparent;
                color: white;
                font-size: 20px;
                border: none;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button, alignment=Qt.AlignTop | Qt.AlignRight)

        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_monitores)
        self.timer.start(1000)

        self.contador = 0  # Contador de progreso de limpieza

    def crear_tab_inicio(self):
        layout = QVBoxLayout()
        label = QLabel("404 Limpiador")
        label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)

        # Animación de opacidad
        effect = QGraphicsOpacityEffect()
        label.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(3000)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.start()

        # Agregar algo que impresione
        impresion = QLabel("🚀 ¡Listo para mejorar tu sistema!\n¡Haz clic en las pestañas para empezar!")
        impresion.setStyleSheet("color: #ffbf00; font-size: 16px; font-weight: bold;")
        impresion.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(label)
        layout.addWidget(impresion)
        layout.addStretch()
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def crear_tab_limpieza(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        def crear_boton(texto, funcion, color="#ff00c0"):
            btn = QPushButton(texto)
            btn.setStyleSheet(f""" 
                QPushButton {{
                    background-color: {color};
                    color: white;
                    font-size: 16px;
                    padding: 12px;
                    border-radius: 12px;
                    margin: 5px;
                    width: 120px;
                    transition: all 0.3s ease;
                }}
                QPushButton:hover {{
                    background-color: {self.darker_color(color)};
                    transform: scale(1.05);
                }}
                QPushButton:pressed {{
                    background-color: {self.darker_color(color)};
                    transform: scale(0.95);
                }}
            """)
            btn.clicked.connect(funcion)
            return btn

        def ejecutar_activar_bat():
            try:
                # Ruta completa al archivo .bat
                bat_path = os.path.join(os.getcwd(), "404", "activar.bat")
                subprocess.Popen(["cmd.exe", "/K", bat_path])
                QMessageBox.information(self, "Activación de Windows", "¡Windows activado exitosamente!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo ejecutar el archivo .bat.\n{e}")

        # Usar un layout en grid para acomodar los botones en 2 filas
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(10)

        grid_layout.addWidget(crear_boton("🧹 Temporales", self.limpiar_temporales), 0, 0)
        grid_layout.addWidget(crear_boton("🌐 privacidad", self.limpiar_cache), 0, 1)
        grid_layout.addWidget(crear_boton("📜 Registros", self.limpiar_errores), 1, 0)
        grid_layout.addWidget(crear_boton("🗑️ papelera", self.limpiar_papelera), 1, 1)
        grid_layout.addWidget(crear_boton("🔵 Activar Windows", ejecutar_activar_bat, "#2196F3"), 2, 0, 1, 2)

        layout.addLayout(grid_layout)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def darker_color(self, color):
        # Función para hacer un color más oscuro
        return f"{color[:-1]}D3)"

    def crear_tab_juegos(self):
        layout = QVBoxLayout()
        label = QLabel("🎮 Pestaña de Juegos")
        label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)

        # Crear el botón para ejecutar el archivo .bat
        def ejecutar_launcher():
            try:
                # Ruta completa al archivo .bat
                bat_path = os.path.join(os.getcwd(), "404", "Launcher.bat")
                subprocess.Popen(["cmd.exe", "/K", bat_path])
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo ejecutar el archivo .bat.\n{e}")

        # Botón para ejecutar el Launcher.bat
        boton_launcher = QPushButton("🚀 Lanzar Juegos")
        boton_launcher.setStyleSheet(""" 
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 12px;
                margin: 5px;
                width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #387d3b;
            }
        """)
        boton_launcher.clicked.connect(ejecutar_launcher)

        layout.addWidget(label)
        layout.addWidget(boton_launcher)  # Agregar el botón al layout
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def limpiar_temporales(self):
            try:
                # Ruta completa al archivo .bat
                bat_path = os.path.join(os.getcwd(), "404", "Limpieza.bat")
                subprocess.Popen(["cmd.exe", "/K", bat_path])
                QMessageBox.information(self, "Limpieza de Windows", "¡Windows Limpiado exitosamente!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo ejecutar el archivo .bat.\n{e}")
                
    def limpiar_cache(self):
            try:
                # Ruta completa al archivo .bat
                bat_path = os.path.join(os.getcwd(), "404", "Privacidad.bat")
                subprocess.Popen(["cmd.exe", "/K", bat_path])
                QMessageBox.information(self, "Privacidad de Windows", "¡Privacidad exitosamente!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo ejecutar el archivo .bat.\n{e}")

    def limpiar_errores(self):
            try:
                # Ruta completa al archivo .bat
                bat_path = os.path.join(os.getcwd(), "404", "Registros.cmd")
                subprocess.Popen(["cmd.exe", "/K", bat_path])
                QMessageBox.information(self, "Registros de Windows", "¡Limpieza de Registros exitosamente!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo ejecutar el archivo .bat.\n{e}")

    def limpiar_papelera(self):
            try:
                # Ruta completa al archivo .bat
                bat_path = os.path.join(os.getcwd(), "404", "Limpieza.bat")
                subprocess.Popen(["cmd.exe", "/K", bat_path])
                QMessageBox.information(self, "Limpieza Total Windows", "¡Limpieza total exitosamente!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo ejecutar el archivo .bat.\n{e}")

    def actualizar_monitores(self):
        # Actualización de monitores (se puede usar en algún tipo de barra de progreso)
        pass

    def darker_color(self, color):
        """Devuelve un color más oscuro para el efecto hover y presionado."""
        color = QColor(color)
        color.setHsv(color.hue(), color.saturation(), int(color.value() * 0.8))  # Baja el brillo
        return color.name()


if __name__ == "__main__":
    pedir_permiso_administrador()  # Pedir permisos de administrador si no tiene
    app = QApplication(sys.argv)
    ventana = LimpiadorApp()
    ventana.show()
    sys.exit(app.exec_())
