import threading
import time
import sys

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt


class Business:
    # Creating business with own name, basic upgrade cost, basic earnings and time needed for revenue
    def __init__(self, name, cost, earnings, bus_delay):
        self.name = name
        self.cost = cost
        self.earnings = earnings
        self.bus_delay = bus_delay
        self.level = 1
        self.is_running = False
        self.start_cost = cost
        self.automatic = False
        self.bought = False

    # Increasing upgrade cost at every level
    def upgrade_cost(self):
        return int(self.cost * 1.5)

    # Increasing revenue at every level
    def upgrade_earnings(self):
        return int(self.earnings * 1.2)

    # Starting automatic earning
    def start(self):
        self.is_running = True
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while self.is_running:
            time.sleep(self.bus_delay)
            self.earn()

    def stop(self):
        self.is_running = False

    # Function with earning mechanism and unlocking upgrades
    def earn(self):
        earnings = self.earnings * self.level
        game.total += earnings
        window.ects_label.setText(str(game.total))
        print(f"Earned {earnings} from {self.name}!")
        print(f"Now you have {game.total}!")
        i = 0
        for business in game.businesses:
            if game.total >= business.cost:
                if business.bought:
                    window.upgrade_buttons[i].setEnabled(True)
                else:
                    window.buy_buttons[i].setEnabled(True)
            if game.total >= 10 * business.start_cost and not business.automatic:
                window.auto_buttons[i].setEnabled(True)
            i += 1

    # Function with upgrading businesses and updating current total money value
    def upgrade(self):
        if game.total >= self.cost:
            game.total -= self.cost
            self.cost = self.upgrade_cost()
            self.earnings = self.upgrade_earnings()
            self.level += 1
            print(f"Upgraded {self.name} to level {self.level}!")
            i = 0
            for business in game.businesses:
                if game.total < business.cost:
                    if business.bought:
                        window.upgrade_buttons[i].setEnabled(False)
                    else:
                        window.buy_buttons[i].setEnabled(False)
                if game.total < 10 * business.start_cost:
                    window.auto_buttons[i].setEnabled(False)
                i += 1


# Function that checks if it is possible to buy a new business
def buy_business(business):
    if game.total > game.businesses[j].cost:
        game.total -= business.cost
        business.start()
    i = 0
    for business in game.businesses:
        if game.total <= business.cost:
            if business.bought:
                window.upgrade_buttons[i].setEnabled(False)
            else:
                window.buy_buttons[i].setEnabled(False)
        i += 1


# TODO - move elements from main to run
def run():
    time.sleep(1)


class Game:
    # Creating game with list of businesses and total amount of money
    def __init__(self):
        self.total = 0
        self.businesses = [
            Business("OiAK", 10, 1, 1),
            Business("JP", 100, 10, 2),
            Business("PPS", 1000, 100, 3),
            Business("PEA", 5000, 500, 5),
            Business("SDIZO", 10000, 1000000000000, 10)
        ]
        self.is_running = False

    def start(self):
        self.is_running = True
        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        self.is_running = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POGROMCA ECTS")
        # self.setGeometry(200, 200, 400, 300)

        self.widget = QWidget()
        self.layout = QHBoxLayout(self.widget)

        # -------------------------------------- zmiany time

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
        self.layout.addWidget(column_widget)

        # Tworzenie drugiego widgetu z liniami przycisków i napisów
        lines_widget = QWidget()
        lines_layout = QVBoxLayout(lines_widget)

        # Dodawanie napisu "ECTS" nad liniami
        ects_label = QLabel("Budżet ECTS:")
        font = QFont("Verdana", 16)
        ects_label.setFont(font)
        ects_label.setStyleSheet("color: green; ")
        lines_layout.addWidget(ects_label)


        # ----------------------------------------- koniec zmian

        self.ects_label = QLabel("0")
        self.lines_layout.addWidget(self.ects_label)

        self.buttons = []
        self.buy_buttons = []
        self.upgrade_buttons = []
        self.auto_buttons = []

        for i, business in enumerate(game.businesses):
            # -----------------------------------------------zmiany2
            line_widget = QWidget()
            line_layout = QHBoxLayout(line_widget)

            line_widget.setStyleSheet("background-color: #434343;border: 2px solid black;")

            label1 = QLabel(f'   Kurs {i}   ')
            font = QFont("Verdana", 10)
            label1.setFont(font)
            label1.setAlignment(Qt.AlignCenter)
            label1.setStyleSheet("color: white;")
            line_layout.addWidget(label1)
            # -----------------------------------------------zmiany2 end

            # reszte wrzucic do line_layoutu z formatowaniem z front.py
            button = QPushButton(f"Click {i}")
            button.clicked.connect(self.on_click)
            self.buttons.append(button)
            self.layout.addWidget(button)

            buy_button = QPushButton(f"Buy {business.name}")
            buy_button.clicked.connect(self.on_buy)
            buy_button.setEnabled(False)
            self.buy_buttons.append(buy_button)
            self.layout.addWidget(buy_button)

            upgrade_button = QPushButton(f"Upgrade {business.name}")
            upgrade_button.clicked.connect(self.on_upgrade)
            upgrade_button.setEnabled(False)
            self.upgrade_buttons.append(upgrade_button)
            self.layout.addWidget(upgrade_button)

            auto_button = QPushButton(f"Buy auto {business.name}")
            auto_button.clicked.connect(self.on_auto)
            auto_button.setEnabled(False)
            self.auto_buttons.append(auto_button)
            self.layout.addWidget(auto_button)

        self.setCentralWidget(self.widget)

    def on_click(self):
        index = self.buttons.index(self.sender())
        game.businesses[index].earn()

    def on_buy(self):
        index = self.buy_buttons.index(self.sender())
        if game.total >= game.businesses[index].cost:
            game.businesses[index].bought = True
            self.buy_buttons[index].setEnabled(False)
            self.buttons[index].setEnabled(True)
            self.ects_label.setText(str(game.total))

    def on_upgrade(self):
        index = self.upgrade_buttons.index(self.sender())
        if game.total >= game.businesses[index].cost:
            game.businesses[index].upgrade()
            self.upgrade_buttons[index].setEnabled(False)
            self.ects_label.setText(str(game.total))

    def on_auto(self):
        index = self.auto_buttons.index(self.sender())
        if game.total >= 10 * game.businesses[index].start_cost:
            self.buttons[index].setEnabled(False)
            buy_business(game.businesses[index])
            self.auto_buttons[index].setEnabled(False)
            game.businesses[index].automatic = True


if __name__ == "__main__":
    game = Game()
    game.start()
    command = 0
    game.businesses[0].bought = True
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
