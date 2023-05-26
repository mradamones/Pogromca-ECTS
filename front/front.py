import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt, QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Tworzenie głównego widżetu i układu poziomego
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Tworzenie widgetu kolumny po lewej stronie
        column_widget = QWidget()
        column_layout = QVBoxLayout(column_widget)

        # Dodawanie napisu
        text_label = QLabel("POGROMCA ECTS")
        font = QFont("Verdana", 16)  # Ustawienie czcionki "Verdana" z rozmiarem 24
        text_label.setFont(font)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("color: WHITE")  # Ustawienie koloru napisu na czerwony
        column_layout.addWidget(text_label)

        # Dodawanie obrazu do kolumny
        image_label = QLabel()
        pixmap = QPixmap('student.png')
        scaled_pixmap = pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2)  # Skaluj obraz
        image_label.setPixmap(scaled_pixmap)
        # Dodawanie czarnego obramowania do obrazu
        image_label.setStyleSheet("border: 2px solid black")
        column_layout.addWidget(image_label)

        # Dodawanie napisu pod obrazem
        text_label = QLabel("Twoja postać: Student\n\n\n\n\n\n\n")
        font = QFont("Verdana", 12)
        text_label.setFont(font)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("color: black")
        column_layout.addWidget(text_label)

        # Dodawanie kolumny do głównego układu
        layout.addWidget(column_widget)

        # Tworzenie drugiego widgetu z liniami przycisków i napisów
        lines_widget = QWidget()
        lines_layout = QVBoxLayout(lines_widget)

        # Dodawanie napisu "ECTS" nad liniami
        ects_label = QLabel("Budżet ECTS:")
        font = QFont("Verdana", 16)
        ects_label.setFont(font)
        ects_label.setStyleSheet("color: green; ")
        lines_layout.addWidget(ects_label)

        # Tworzenie linii przycisków i napisów
        for i in range(5):
            line_widget = QWidget()
            line_layout = QHBoxLayout(line_widget)

            line_widget.setStyleSheet("background-color: #434343;border: 2px solid black;")

            label1 = QLabel(f'   Kurs {i}   ')
            font = QFont("Verdana", 10)
            label1.setFont(font)
            label1.setAlignment(Qt.AlignCenter)
            label1.setStyleSheet("color: white;")
            line_layout.addWidget(label1)

            # Tworzenie przycisków w linii
            buttons = []
            for j in range(4):
                button = QPushButton()
                buttons.append(button)  # Dodanie przycisku do listy
                button.setStyleSheet("background-color: white;")
                line_layout.addWidget(button)

            label2 = QLabel(f'{(i + 1) * 100} ECT$')
            font = QFont("Verdana", 10)
            label2.setFont(font)
            label2.setStyleSheet("color: white;")
            line_layout.addWidget(label2)

            lines_layout.addWidget(line_widget)

            # Dodawanie obrazka na wybrane przyciski
            buttons_to_add_image = [1, 5, 9, 13, 17]
            for button_number in buttons_to_add_image:
                if button_number <= len(buttons):
                    button = buttons[button_number - 1]
                    button.setIcon(QIcon('click.png'))
                    button.setIconSize(QSize(60, 60))

            # Dodawanie obrazka na wybrane przyciski
            buttons_to_add_image = [2, 6, 10, 14, 18]
            for button_number in buttons_to_add_image:
                if button_number <= len(buttons):
                    button = buttons[button_number - 1]
                    button.setIcon(QIcon('buy.png'))
                    button.setIconSize(QSize(60, 60))

            # Dodawanie obrazka na wybrane przyciski
            buttons_to_add_image = [3, 7, 10, 13, 16, 19]
            for button_number in buttons_to_add_image:
                if button_number <= len(buttons):
                    button = buttons[button_number - 1]
                    button.setIcon(QIcon('upgrade.png'))
                    button.setIconSize(QSize(60, 60))

            # Dodawanie obrazka na wybrane przyciski
            buttons_to_add_image = [4, 8, 12, 16, 20]
            for button_number in buttons_to_add_image:
                if button_number <= len(buttons):
                    button = buttons[button_number - 1]
                    button.setIcon(QIcon('auto.png'))
                    button.setIconSize(QSize(60, 60))

        # Dodawanie drugiego widgetu do głównego układu
        layout.addWidget(lines_widget)

        # Ustawianie głównego widżetu w głównym oknie
        self.setCentralWidget(widget)

        # Ustawianie tła na ciemnoszare
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(50, 50, 50))
        self.setPalette(palette)

        # Tworzenie stopki
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)

        # Dodawanie napisu w stopce
        copyright_label = QLabel("\n© Pogromcy - rights reserved.")
        font = QFont("Verdana", 10)
        copyright_label.setFont(font)
        footer_layout.addWidget(copyright_label)

        # Dodawanie stopki
        lines_layout.addWidget(footer_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
