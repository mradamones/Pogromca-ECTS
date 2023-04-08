# Pogromca-ECTS
Simple clicker game for Systemy Operacyjne 2 project (PWr)

### Description
Pogromca-ECTS (ECTS-Slayer) is a clicker game based on popular ones like AdVenture Capitalist, Cookie Clicker etc. 
Program uses threads to manage different businesses (courses) when player buys option to automatically earn ECTS points.
Player can buy locked courses and upgrades (cost of future upgrade and revenue increases). Game can be played in 
free mode (no limits of levels or points), but it is possible to add limit and achievements.
### Mockup
![Layout of game will be similar to AdVenture Capitalist and will allow player to buy businesses and upgrades.](/szablon.png)
### Threads
- Every business (course) is another thread
- Entire game is ran on other thread
- (in process) Checking amount of points to enable/disable buttons will be made in another thread
### Critical sections

### Authors <br>
@github/mradamones <br>
@github/ebronx