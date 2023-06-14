# Pogromca-ECTS
Simple clicker game for Systemy Operacyjne 2 project (PWr)

### Description
Pogromca-ECTS (ECTS-Slayer) is a clicker game based on popular ones like AdVenture Capitalist, Cookie Clicker etc. 
Program uses threads to manage different businesses (courses) when player buys option to automatically earn ECTS points.
Player can buy locked courses and upgrades (cost of future upgrade and revenue increases). Game can be played in 
free mode (no limits of levels or points), but it is possible to add limit and achievements.
### Mockup
![Layout of game will be similar to AdVenture Capitalist and will allow player to buy businesses and upgrades.](/szablon.png)
### Actual Screen
![Layout of game will be similar to AdVenture Capitalist and will allow player to buy businesses and upgrades.](/gameplay.png)
### Threads
- **buy_auto(business)** - Every business (course) is another thread. It collects ECTS points automatically after unlocking automatic earning.
- **check_buy()** - Checking amount of points to enable/disable buttons will be made in another thread.
- **timer()** - Timers for every business has its own thread. Number of seconds left to collect points displays on the main screen.
### Critical sections
- **game.total** - access to this variable have two different threads: one with auto earning and second with checking possible buys. Only first one changes value of variable, so this function handles critical section by using *lock*
>with self.lock:  (...)

Check_buy function only checks amount of ECTS points so there is no need to use locks.
### Authors
[mradamones](https://github.com/mradamones/) <br>
[ebronx](https://github.com/ebronx/)