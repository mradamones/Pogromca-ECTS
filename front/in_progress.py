import threading
import time
import sys

from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QSize


class Business:
    # Tworzenie biznesu z nazwą, kosztem podstawowej aktualizacji, podstawowym zyskiem i czasem potrzebnym na generowanie przychodu
    def __init__(self, name, cost, earnings, bus_delay, lock):
        self.name = name
        self.cost = cost
        self.earnings = earnings
        self.bus_delay = bus_delay
        self.level = 1
        self.is_running = False
        self.start_cost = cost
        self.automatic = False
        self.bought = False
        self.lock = lock

    # Zwiększanie kosztu aktualizacji wraz z poziomem
    def upgrade_cost(self):
        return int(self.cost * 1.5)

    # Zwiększanie przychodu wraz z poziomem
    def upgrade_earnings(self):
        return int(self.earnings * 1.2)

    # Uruchamianie automatycznego generowania przychodu
    def start(self):
        self.is_running = True
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while self.is_running:
            time.sleep(self.bus_delay)
            self.earn()

    def stop(self):
        self.is_running = False

    # Mechanizm generowania przychodu i odblokowywania aktualizacji
    def earn(self):
        earnings = self.earnings * self.level
        with self.lock:
            game.total += earnings
            window.ects_label.setText(str(game.total))


def check_buy():
    while True:
        time.sleep(0.1)
        i = 0
        for business in game.businesses:
            if game.total >= business.cost:
                if business.bought:
                    window.upgrade_buttons[i].setEnabled(True)
                else:
                    window.buy_buttons[i].setEnabled(True)
            else:
                if business.bought:
                    window.upgrade_buttons[i].setEnabled(False)
                    window.auto_buttons[i].setEnabled(False)
                else:
                    window.buy_buttons[i].setEnabled(False)
            if game.total >= 10 * business.start_cost and not business.automatic and business.bought:
                window.auto_buttons[i].setEnabled(True)
            i += 1


def buy_new(business):
    if game.total >= business.cost:
        game.total -= business.cost
        business.bought = True


def upgrade(bus):
    if game.total >= bus.cost:
        game.total -= bus.cost
        bus.cost = bus.upgrade_cost()
        bus.earnings = bus.upgrade_earnings()
        bus.level += 1
        print(f"Upgraded {bus.name} to level {bus.level}!")


# Funkcja sprawdzająca, czy możliwe jest kupienie nowego biznesu
def buy_auto(bus):
    if game.total >= 10 * bus.start_cost:
        game.total -= 10 * bus.start_cost
        bus.start()
        bus.automatic = True


# TODO - przenieś elementy z funkcji main do run
def run():
    while game.is_running:
        time.sleep(1)


class Game:
    # Tworzenie gry z listą biznesów i całkowitą ilością pieniędzy
    def __init__(self):
        self.total = 0
        self.lock = threading.Lock()
        self.businesses = [
            Business("OiAK", 10, 1, 1, self.lock),
            Business("JP", 100, 10, 2, self.lock),
            Business("PPS", 1000, 100, 3, self.lock),
            Business("PEA", 5000, 500, 5, self.lock),
            Business("SDIZO", 10000, 1000000000000, 10, self.lock)
        ]
        self.is_running = False

    def start(self):
        self.is_running = True
        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        self.is_running = False


class MainWindow(QMainWindow):
    # TODO - add level number for every business (label)
    # TODO - add buy/upgrade and autobuy price for every business (label)
    # TODO - add earnings per second from every business (labels?)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POGROMCA ECTS")
        # self.setGeometry(200, 200, 400, 300)

        self.widget = QWidget()
        layout = QHBoxLayout(self.widget)

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

        self.ects_label = QLabel("0")
        lines_layout.addWidget(self.ects_label)

        self.buttons = []
        self.buy_buttons = []
        self.upgrade_buttons = []
        self.auto_buttons = []

        for i, business in enumerate(game.businesses):
            line_widget = QWidget()
            line_layout = QHBoxLayout(line_widget)

            line_widget.setStyleSheet("background-color: #434343;border: 2px solid black;")

            label1 = QLabel(f'   Kurs {business.name}   ')
            font = QFont("Verdana", 10)
            label1.setFont(font)
            label1.setAlignment(Qt.AlignCenter)
            label1.setStyleSheet("color: white;")
            line_layout.addWidget(label1)

            button = QPushButton()
            button.clicked.connect(self.on_click)
            button.setEnabled(False)
            button.setIcon(QIcon('click.png'))
            button.setIconSize(QSize(60, 60))
            self.buttons.append(button)
            line_layout.addWidget(button)

            buy_button = QPushButton()
            buy_button.clicked.connect(self.on_buy)
            buy_button.setEnabled(False)
            buy_button.setIcon(QIcon('buy.png'))
            buy_button.setIconSize(QSize(60, 60))
            self.buy_buttons.append(buy_button)
            line_layout.addWidget(buy_button)

            upgrade_button = QPushButton()
            upgrade_button.clicked.connect(self.on_upgrade)
            upgrade_button.setEnabled(False)
            upgrade_button.setIcon(QIcon('upgrade.png'))
            upgrade_button.setIconSize(QSize(60, 60))
            self.upgrade_buttons.append(upgrade_button)
            line_layout.addWidget(upgrade_button)

            auto_button = QPushButton()
            auto_button.clicked.connect(self.on_auto)
            auto_button.setEnabled(False)
            auto_button.setIcon(QIcon('auto.png'))
            auto_button.setIconSize(QSize(60, 60))
            self.auto_buttons.append(auto_button)
            line_layout.addWidget(auto_button)

            # Dodawanie kolumny do głównego układu
            lines_layout.addWidget(line_widget)

        # Dodawanie lines do głównego układu
        layout.addWidget(lines_widget)

        self.setCentralWidget(self.widget)
        self.buttons[0].setEnabled(True)

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

    def on_click(self):
        index = self.buttons.index(self.sender())
        game.businesses[index].earn()
        self.buttons[index].setEnabled(False)
        QTimer.singleShot(1000 * game.businesses[index].bus_delay, lambda: self.buttons[index].setEnabled(True))

    def on_buy(self):
        index = self.buy_buttons.index(self.sender())
        if game.total >= game.businesses[index].cost:
            self.buy_buttons[index].setEnabled(False)
            self.buttons[index].setEnabled(True)
            buy_new(game.businesses[index])
            self.ects_label.setText(str(game.total))

    def on_upgrade(self):
        index = self.upgrade_buttons.index(self.sender())
        if game.total >= game.businesses[index].cost:
            upgrade(game.businesses[index])
            self.ects_label.setText(str(game.total))

    def on_auto(self):
        index = self.auto_buttons.index(self.sender())
        if game.total >= 10 * game.businesses[index].start_cost:
            self.buttons[index].setEnabled(False)
            buy_auto(game.businesses[index])
            self.auto_buttons[index].setEnabled(False)


if __name__ == "__main__":
    lock = threading.Lock()
    game = Game()
    game.start()
    command = 0
    game.businesses[0].bought = True

    buy_thread = threading.Thread(target=check_buy, daemon=True)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    buy_thread.start()
    sys.exit(app.exec_())
