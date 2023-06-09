''' Simple clicker game '''
import threading
import time
import sys
import math
# pylint: disable=no-name-in-module
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QColor
# pylint: disable=no-name-in-module
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QPushButton, QVBoxLayout, QWidget, QHBoxLayout)
# pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt, QTimer, QSize

# pylint: disable=too-many-instance-attributes
class Business:
    ''' Creating a business with name, base upgrade cost,
    base earnings, and time required to generate income '''

    # pylint: disable=too-many-arguments
    def __init__(self, name, cost, earnings, bus_delay, lock, index):
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
        self.dur_time = self.bus_delay
        self.index = index

    def upgrade_cost(self):
        ''' Increasing the upgrade cost with each level '''
        return int(self.cost * 1.5)

    def upgrade_earnings(self):
        ''' Increasing the earnings with each level '''
        return math.ceil(self.earnings * 1.2)

    def start(self):
        ''' Starting automatic income generation '''
        self.is_running = True
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        ''' Thread that automatically generates income '''
        while self.is_running:
            threading.Thread(target=timer,
                             args=(window.timer_labels[self.index],
                             self.dur_time)).start()
            time.sleep(self.bus_delay)
            self.earn()

    def earn(self):
        ''' Income generation mechanism and unlocking upgrades '''
        with self.lock:
            game.total += self.earnings
            window.ects_label.setText(str(game.total))


def timer(label, dur_time):
    '''Thread for every business timer'''
    temp = dur_time
    while temp > 0:
        time.sleep(1)
        temp -= 1
        label.setText(f"Time: {temp}")
    label.setText(f"Time: {dur_time}")
    # Jeżeli dur_time osiągnie zero, zabij wątek
    #threading.currentThread()._stop()

def check_buy():
    ''' Thread checking if any button should be activated or deactivated '''
    while True:
        time.sleep(0.1)
        for i, business in enumerate(game.businesses):
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
            if (game.total >= 10 * business.start_cost
                    and not business.automatic and business.bought):
                window.auto_buttons[i].setEnabled(True)
            else:
                window.auto_buttons[i].setEnabled(False)


def buy_new(business):
    ''' Setting up new bought business '''
    if game.total >= business.cost:
        game.total -= business.cost
        business.bought = True


def upgrade(bus):
    ''' Editing upgraded business by increasing upgrade cost and income '''
    if game.total >= bus.cost:
        game.total -= bus.cost
        bus.cost = bus.upgrade_cost()
        bus.earnings = bus.upgrade_earnings()
        bus.level += 1


def buy_auto(bus):
    ''' Function to check if a new business can be purchased '''
    if game.total >= 10 * bus.start_cost:
        game.total -= 10 * bus.start_cost
        bus.start()
        bus.automatic = True

# pylint: disable=too-few-public-methods

class Game:
    ''' Creating the game with a list of businesses and the total amount of money '''
    def __init__(self):
        self.total = 100000
        self.lock = threading.Lock()
        self.businesses = [
            Business("OiAK", 10, 1, 1, self.lock, 0),
            Business("JP", 100, 10, 2, self.lock, 1),
            Business("PPS", 1000, 100, 3, self.lock, 2),
            Business("PEA", 5000, 500, 5, self.lock, 3),
            Business("SDIZO", 10000, 1000000000000, 10, self.lock, 4)
        ]


# pylint: disable=too-many-instance-attributes
class MainWindow(QMainWindow):
    ''' Class for window design '''
    # TODO - make score more visible
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POGROMCA ECTS")
        self.setWindowIcon(QIcon('ikonka.png'))
        self.widget = QWidget()
        layout = QHBoxLayout(self.widget)

        # Creating column widget at left side
        column_widget = QWidget()
        column_layout = QVBoxLayout(column_widget)

        # Adding that big text on the top of page
        text_label = QLabel("POGROMCA ECTS")
        font = QFont("Verdana", 16)  # Setting Verdana font
        text_label.setFont(font)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("color: WHITE")  # Setting text color
        column_layout.addWidget(text_label)

        # Adding image to column
        image_label = QLabel()
        pixmap = QPixmap('student.png')
        scaled_pixmap = pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2)  # Scaling image
        image_label.setPixmap(scaled_pixmap)
        # Adding black border to image
        image_label.setStyleSheet("border: 2px solid black")
        column_layout.addWidget(image_label)

        # Adding description to image
        text_label = QLabel("Twoja postać: Student\n\n\n\n\n\n\n")
        font = QFont("Verdana", 12)
        text_label.setFont(font)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("color: black")
        column_layout.addWidget(text_label)

        # Adding column to main widget
        layout.addWidget(column_widget)

        # Creating second widget with buttons
        lines_widget = QWidget()
        lines_layout = QVBoxLayout(lines_widget)

        # Adding 'ECTS' label on top of widget
        ects_label = QLabel("Budżet ECTS:")
        font = QFont("Verdana", 16)
        ects_label.setFont(font)
        ects_label.setStyleSheet("color: #0e6926; ")
        lines_layout.addWidget(ects_label)

        self.ects_label = QLabel("0")
        font = QFont("Verdana", 16)
        self.ects_label.setFont(font)
        self.ects_label.setStyleSheet("color: #94e0a9; ")
        lines_layout.addWidget(self.ects_label)

        space_label = QLabel("\n")
        lines_layout.addWidget(space_label)

        self.level_labels = []
        self.cost_labels = []
        self.earnings_labels = []
        self.timer_labels = []
        self.buttons = []
        self.buy_buttons = []
        self.upgrade_buttons = []
        self.auto_buttons = []

        for business in game.businesses:
            line_widget = QWidget()
            line_layout = QHBoxLayout(line_widget)

            line_widget.setStyleSheet("background-color: #434343;border: 2px solid black;")

            label1 = QLabel(f'   Kurs {business.name}   ')
            font = QFont("Verdana", 10)
            label1.setFont(font)
            label1.setFixedWidth(100)
            label1.setAlignment(Qt.AlignCenter)
            label1.setStyleSheet("color: white;")
            line_layout.addWidget(label1)

            level_label = QLabel(f'Level: {business.level}')
            level_label.setStyleSheet("color: white;")
            font = QFont("Verdana", 10)
            level_label.setFont(font)
            level_label.setAlignment(Qt.AlignCenter)
            level_label.setFixedWidth(80)
            line_layout.addWidget(level_label)
            self.level_labels.append(level_label)

            cost_label = QLabel(f'Cost: {business.cost}')
            cost_label.setStyleSheet("color: white;")
            cost_label.setFixedWidth(110)
            font = QFont("Verdana", 10)
            cost_label.setFont(font)
            cost_label.setAlignment(Qt.AlignCenter)
            line_layout.addWidget(cost_label)
            self.cost_labels.append(cost_label)

            earnings_label = QLabel(f'Earnings/sec: '
                                    f'{round(business.earnings / business.bus_delay)}')
            earnings_label.setStyleSheet("color: white;")
            earnings_label.setFixedWidth(200)
            font = QFont("Verdana", 10)
            earnings_label.setFont(font)
            earnings_label.setAlignment(Qt.AlignCenter)
            line_layout.addWidget(earnings_label)
            self.earnings_labels.append(earnings_label)

            timer_label = QLabel(f'Time: {business.dur_time}')
            timer_label.setStyleSheet("color: white;")
            timer_label.setFixedWidth(80)
            font = QFont("Verdana", 10)
            timer_label.setFont(font)
            timer_label.setAlignment(Qt.AlignCenter)
            line_layout.addWidget(timer_label)
            self.timer_labels.append(timer_label)

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

            # Adding column to main widget
            lines_layout.addWidget(line_widget)

        # Adding main widget to page
        layout.addWidget(lines_widget)

        self.setCentralWidget(self.widget)
        self.buttons[0].setEnabled(True)

        # Setting up background
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(50, 50, 50))
        self.setPalette(palette)

        # Setting up footer
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)

        # Adding text to footer
        copyright_label = QLabel("\n                            © Pogromcy - rights reserved.")
        font = QFont("Verdana", 10)
        copyright_label.setFont(font)
        footer_layout.addWidget(copyright_label)

        # Adding footer to main widget
        lines_layout.addWidget(footer_widget)

    def on_click(self):
        ''' Defines actions after click on earn button '''
        index = self.buttons.index(self.sender())
        threading.Thread(target=timer,
                         args=(window.timer_labels[index],
                         game.businesses[index].dur_time)).start()
        self.buttons[index].setEnabled(False)
        QTimer.singleShot(1000 * game.businesses[index].bus_delay,
                          lambda: self.buttons[index].setEnabled
                          (not game.businesses[index].automatic))
        game.businesses[index].earn()

    def on_buy(self):
        ''' Defines actions after click on buy button '''
        index = self.buy_buttons.index(self.sender())
        if game.total >= game.businesses[index].cost:
            self.buy_buttons[index].setEnabled(False)
            self.buttons[index].setEnabled(True)
            buy_new(game.businesses[index])
            self.ects_label.setText(str(game.total))

    def on_upgrade(self):
        ''' Defines actions after click on upgrade button '''
        index = self.upgrade_buttons.index(self.sender())
        if game.total >= game.businesses[index].cost:
            upgrade(game.businesses[index])
            self.ects_label.setText(str(game.total))
            self.level_labels[index].setText(f'Level: {game.businesses[index].level}')
            self.cost_labels[index].setText(f'Cost: {game.businesses[index].cost}')
            earnings_per_sec = \
                round(game.businesses[index].earnings / game.businesses[index].bus_delay)
            self.earnings_labels[index].setText(f'Earnings/sec: {earnings_per_sec}')

    def on_auto(self):
        ''' Defines actions after click on autobuy button '''
        index = self.auto_buttons.index(self.sender())
        if game.total >= 10 * game.businesses[index].start_cost:
            self.buttons[index].setEnabled(False)
            buy_auto(game.businesses[index])
            self.auto_buttons[index].setEnabled(False)


if __name__ == "__main__":
    game = Game()
    game.businesses[0].bought = True
    buy_thread = threading.Thread(target=check_buy, daemon=True)
    buy_thread.start()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
