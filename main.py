import threading
import time
import PySimpleGUI as sg


class Business:
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

    def upgrade_cost(self):
        return int(self.cost * 1.5)

    def upgrade_earnings(self):
        return int(self.earnings * 1.2)

    def start(self):
        self.is_running = True
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while self.is_running:
            time.sleep(self.bus_delay)
            self.earn()

    def stop(self):
        self.is_running = False

    def auto_earn(self):
        while self.is_running:
            time.sleep(self.bus_delay)
            self.earn()

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
                        window[f'upg{i}'].update(disabled=True)
                    else:
                        window[f'buy{i}'].update(disabled=True)
                if game.total < 10 * business.start_cost:
                    window[f'aut{i}'].update(disabled=True)
                i += 1


class Game:
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
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        time.sleep(1)

    def stop(self):
        self.is_running = False

    def buy_business(self, business):
        if game.total > game.businesses[iter].cost:
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

    def upgrade_business(self, business):
        business.upgrade()


if __name__ == "__main__":
    game = Game()
    game.start()
    command = 0
    game.businesses[0].bought = True
    sg.theme('DarkAmber')
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
        iter = int(event[3:5:1])
        if command == "buy":
            if game.total >= game.businesses[iter].cost:
                game.businesses[iter].bought = True
                window[f'buy{iter}'].update(disabled=True)
                window[f'cli{iter}'].update(disabled=False)
                window['ects'].update(f'{game.total}')
        elif command == "upg":
            if game.total >= game.businesses[iter].cost:
                game.upgrade_business(game.businesses[iter])
                window[f'cost{iter}'].update(game.businesses[iter].cost)
                window['ects'].update(f'{game.total}')
        elif command == "cli":
            game.businesses[iter].earn()
            # TODO - make clicks slower
        elif command == "aut":
            if game.total >= 10 * game.businesses[iter].start_cost:
                window[f'cli{iter}'].update(disabled=True)
                game.buy_business(game.businesses[iter])
                window[f'aut{iter}'].update(disabled=True)
                game.businesses[iter].automatic = True
