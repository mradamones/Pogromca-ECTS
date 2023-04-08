import threading
import time
import PySimpleGUI as sg


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
        window['ects'].update(f'{game.total}')
        print(f"Earned {earnings} from {self.name}!")
        print(f"Now you have {game.total}!")
        i = 0
        for business in game.businesses:
            if game.total >= business.cost:
                if business.bought:
                    window[f'upg{i}'].update(disabled=False)
                else:
                    window[f'buy{i}'].update(disabled=False)
            if game.total >= 10 * business.start_cost and not business.automatic:
                window[f'aut{i}'].update(disabled=False)
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
            # TODO - Can create thread to check money and enable and disable options
            for business in game.businesses:
                if game.total < business.cost:
                    if business.bought:
                        window[f'upg{i}'].update(disabled=True)
                    else:
                        window[f'buy{i}'].update(disabled=True)
                if game.total < 10 * business.start_cost:
                    window[f'aut{i}'].update(disabled=True)
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
                window[f'upg{i}'].update(disabled=True)
            else:
                window[f'buy{i}'].update(disabled=True)
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


if __name__ == "__main__":
    game = Game()
    game.start()
    command = 0
    game.businesses[0].bought = True
    sg.theme('DarkAmber')
    # TODO - add timer
    # TODO - change layout
    # TODO - add context menu
    # TODO - add icon
    layout = [[sg.Text('', key='ects'), sg.Text('ECTS')],
              [sg.Button('Click', key='cli0'), sg.Button('buy OiAK', key='buy0', disabled=True),
               sg.Button('Upgrade OiAK', key='upg0', disabled=True), sg.Button("Buy auto", key='aut0', disabled=True),
               sg.Text('OiAK'),
               sg.Text(game.businesses[0].cost, key='cost0')],
              [sg.Button('Click', key='cli1', disabled=True), sg.Button('buy JP', key='buy1', disabled=True),
               sg.Button('Upgrade JP', key='upg1', disabled=True), sg.Button("Buy auto", key='aut1', disabled=True),
               sg.Text('JP'), sg.Text(game.businesses[1].cost, key='cost1')],
              [sg.Button('Click', key='cli2', disabled=True), sg.Button('buy PPS', key='buy2', disabled=True),
               sg.Button('Upgrade PPS', key='upg2', disabled=True), sg.Button("Buy auto", key='aut2', disabled=True),
               sg.Text('PPS'), sg.Text(game.businesses[2].cost, key='cost2')],
              [sg.Button('Click', key='cli3', disabled=True), sg.Button('buy PEA', key='buy3', disabled=True),
               sg.Button('Upgrade PEA', key='upg3', disabled=True), sg.Button("Buy auto", key='aut3', disabled=True),
               sg.Text('PEA'), sg.Text(game.businesses[3].cost, key='cost3')],
              [sg.Button('Click', key='cli4', disabled=True), sg.Button('buy SDIZO', key='buy4', disabled=True),
               sg.Button('Upgrade SDIZO', key='upg4', disabled=True), sg.Button("Buy auto", key='aut4', disabled=True),
               sg.Text('SDIZO'), sg.Text(game.businesses[4].cost, key='cost4')]]
    window = sg.Window('Window Title', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            exit(0)
        command = event[0:3:1]
        j = int(event[3:5:1])
        if command == "buy":
            if game.total >= game.businesses[j].cost:
                game.businesses[j].bought = True
                window[f'buy{j}'].update(disabled=True)
                window[f'cli{j}'].update(disabled=False)
                window['ects'].update(f'{game.total}')
        elif command == "upg":
            if game.total >= game.businesses[j].cost:
                game.businesses[j].upgrade()
                window[f'cost{j}'].update(game.businesses[j].cost)
                window['ects'].update(f'{game.total}')
        elif command == "cli":
            game.businesses[j].earn()
            # TODO - make clicks slower
        elif command == "aut":
            if game.total >= 10 * game.businesses[j].start_cost:
                window[f'cli{j}'].update(disabled=True)
                buy_business(game.businesses[j])
                window[f'aut{j}'].update(disabled=True)
                game.businesses[j].automatic = True
